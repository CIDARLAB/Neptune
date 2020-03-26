#!/bin/sh
git submodule update --recursive

cd ./Fluigi-Cloud
git fetch origin dev
git checkout dev
npm install
sudo chown -R $USER:$GROUP jobs/

cd ..

cd ./Neptune-UI
git fetch origin dev
git checkout origin dev
npm install
npm run build

cp -vr ./dist ../Fluigi-Cloud/dist
 