#!/usr/bin/env bash

export LOG_LEVEL=INFO
export WAIT_TIME=60
export KEYWORD_WAIT_TIME=2
export TWITTER_MAX_RESULTS=20
export TWITTER_KEYWORD_1=techwatch
export TWITTER_USERNAME_1=IdrissNeumann
export SLACK_TRIGGER=on
export SLACK_CHANNEL="#techno-radar"
export UNIQ_VERSION="${CI_COMMIT_BRANCH}-${CI_COMMIT_SHORT_SHA}"
export REDIS_HOST="twitter-slack-redis"
export REDIS_PORT=6379
export REDIS_TTL=86400
