CURRENT=`pwd`
cd frontend/db-perf-tester
npx npm install
npx ng build --build-optimizer --base-href="/static/"
cd $CURRENT
rm -r backend/static/*
cp -r frontend/db-perf-tester/dist/db-perf-tester/* backend/static/
