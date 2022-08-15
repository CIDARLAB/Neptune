#!/bin/sh
git submodule update --recursive

cd ./Fluigi-Cloud
git fetch origin dev
git checkout dev
npm install --legacy-peer-deps
sudo chown -R $USER:$GROUP jobs/

cd ..

cd ./Neptune-UI
git fetch origin dev
git checkout origin dev
npm install --legacy-peer-deps
npm run build

cp -vr ./dist ../Fluigi-Cloud/dist
 