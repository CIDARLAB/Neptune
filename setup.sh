#!/bin/sh
git submodule update --recursive

cd ./Fluigi-Cloud
git fetch origin dev
git checkout dev
CXX=clang npm install
sudo chown -R $USER:$GROUP jobs/

cd ..

cd ./Neptune-UI
git fetch origin dev
git checkout dev
CXX=clang npm install
CXX=clang npm run build

cp -vr ./dist ../Fluigi-Cloud/dist
 