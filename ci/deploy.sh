#!/usr/bin/env bash

## TODO environment file to compute

docker rmi -f "comworkio/twitter-slack:latest" || :
docker-compose -f docker-compose-intra.yml up -d --force-recreate
