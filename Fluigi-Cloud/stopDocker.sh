#!/bin/bash

#Stop FluigiCloud container
docker stop FluigiCloud
echo "[STATUS]		Stopped running Fluigi Cloud"

#Delete FluigiCloud container
docker rm FluigiCloud
echo "[STATUS]		Deleted container"

#Delete Fluigicloud image
docker rmi priyak/fluigicloud
echo "[STATUS]		Removed image"

#Display port for user
echo "[STATUS]		Fluigi Cloud is now removed"