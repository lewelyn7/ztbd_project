FROM node:18-alpine AS angular-build
WORKDIR /usr/src/app
COPY frontend/db-perf-tester/*.json ./
RUN npx npm install
RUN npx npm install @angular/cli
COPY frontend/db-perf-tester/src ./src
RUN ls -al
RUN npx ng build --build-optimizer --base-href="/static/"

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
ENV PYTHONPATH "${PYTHONPATH}:/"
ENV PORT=8000
RUN pip install --upgrade pip
COPY ./backend/requirements.txt /app/
RUN pip install -r requirements.txt
COPY ./backend/app /app
COPY ./backend/.env /app/.env
COPY --from=angular-build /usr/src/app/dist/db-perf-tester/* /app/static/
