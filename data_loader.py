import argparse
import requests
from dataclasses import dataclass
import csv
import logging 
from progress.bar import Bar
import aiohttp
import asyncio
from pydantic import BaseModel, validator

BATCH_SIZE = 4000
ALL_RECORDS_COUNT = 48296895 / BATCH_SIZE
csv.field_size_limit(100000000)

class Record(BaseModel):
    app_id: int
    app_name: str
    review_id: int
    language: str
    review: str
    timestamp_created: str
    timestamp_updated: str
    recommended: bool
    votes_helpful: int
    votes_funny: int
    weighted_vote_score: float
    comment_count: int
    steam_purchase: bool
    received_for_free: bool
    written_during_early_access: bool
    author_steamid: str
    author_num_games_owned: int
    author_num_reviews: int 
    author_playtime_forever: int 
    author_playtime_last_two_weeks: int
    author_playtime_at_review: int
    author_last_played: str

    @validator('author_playtime_at_review', 'author_playtime_last_two_weeks', 'author_playtime_forever', pre=True)
    def to_int(cls, v):
        if len(v) == 0:
            return 0
        return int(float(v))

def handle_resp(resp: aiohttp.ClientResponse, record):
    if resp.status == 200:
        logging.info(f"added {record.app_name}") 
    elif resp.status == 409:
        logging.debug(f"already exists {record.app_name}")
    else:
        print(record)
        print()
        raise Exception(f"status code: {resp.status} body: {str(resp.json())}")

def add_game(record: Record, url: str, db: str):
    resp = requests.post(f"{url}/games/", params={"db": db}, json={
        "name": record.app_name,
        "id": record.app_id
    })
    if resp.status_code == 200:
        logging.info(f"added {record.app_name}") 
    elif resp.status_code == 409:
        logging.debug(f"already exists {record.app_name}")


async def add_game_async(session: aiohttp.ClientSession, record: Record, url: str, db: str):
    async with session.post(f"{url}/games/", params={"db": db}, json={
        "name": record.app_name,
        "id": record.app_id
    }) as resp:
        handle_resp(resp, record)

async def add_author_async(session: aiohttp.ClientSession, record: Record, url: str, db: str):
    json_data = {
        "num_of_games_owned": record.author_num_games_owned,
        "num_reviews": record.author_num_reviews,
        "playtime_forever": record.author_playtime_forever,
        "playtime_last_two_weeks": record.author_playtime_last_two_weeks,
        "id": record.author_steamid,
    }
    # print(json_data)
    async with session.post(f"{url}/authors/", params={"db": db}, json=json_data) as resp:
        handle_resp(resp, record)

async def add_review_async(session: aiohttp.ClientSession, record: Record, url: str, db: str):
    async with session.post(f"{url}/reviews/", params={"db": db}, json={
        "language": record.language,
        "content": record.review,
        "timestamp_created": record.timestamp_created,
        "timestampe_updated": record.timestamp_updated,
        "recommended": record.recommended,
        "votes_helpful": record.votes_helpful,
        "votes_funny": record.votes_funny,
        "weighted_vote_score": record.weighted_vote_score,
        "comment_count": record.comment_count,
        "steam_purchase": record.steam_purchase,
        "received_for_free": record.received_for_free,
        "written_during_early_access": record.written_during_early_access,
        "playtime_at_review": record.author_playtime_at_review,
        "author_id": record.author_steamid,
        "game_id": record.app_id,
        "id": record.review_id,

    }) as resp:
        handle_resp(resp, record)

games_set = set()
authors_set = set()
async def batch_process(records_batch, url: str, db: str):
    async with aiohttp.ClientSession() as session:
        tasks = []
        record: Record
        for record in records_batch:
            if not record.app_id in games_set:
                tasks.append(asyncio.ensure_future(add_game_async(session, record, url, db)))
                games_set.add(record.app_id)
            if not record.author_steamid in authors_set:
                tasks.append(asyncio.ensure_future(add_author_async(session, record, url, db)))
                authors_set.add(record.author_steamid)

            tasks.append(asyncio.ensure_future(add_review_async(session, record, url, db)))
        
        results = await asyncio.gather(*tasks)
        # print(results[0])

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--file")
    parser.add_argument("--url")
    parser.add_argument("--db")
    parser.add_argument("--skip", type=int, default="0")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    records_batch = []
    with open("info_file.txt", "a") as info_file:
        with open(args.file) as rfile:
            reader = csv.DictReader(rfile, delimiter=',', quotechar='"')

            with Bar('Processing', max=ALL_RECORDS_COUNT, suffix = '%(percent).1f%% - %(eta_td)s ') as bar:
                for db in [args.db]:
                    for i, row in enumerate(reader):
                        if i < args.skip:
                            continue
                        logging.debug(f"processing - {db} - {i}")
                        row.pop('')
                        row = {k.replace(".", "_"):v for k,v in row.items()}

                        record = Record(**row)
                        records_batch.append(record)
                        
                        if len(records_batch)%BATCH_SIZE == 0:
                            info_file.write(str(i))
                            info_file.write("\r\n")
                            logging.info(f"processing batch - {i}")
                            asyncio.run(batch_process(records_batch, args.url, db))
                            records_batch = []
                            bar.next()


                


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    main()
