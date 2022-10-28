#!/usr/bin/env bash

export WAIT_TIME=20
export LOG_LEVEL=INFO
export TWITTER_MAX_RESULTS=20
export TWITTER_KEYWORD_1=techwatch
export TWITTER_KEYWORD_2=veilletechno
export TWITTER_USERNAME_1=IdrissNeumann
export SLACK_TRIGGER=on
export SLACK_CHANNEL="#techno-radar"
export UNIQ_VERSION="${CI_COMMIT_BRANCH}-${CI_COMMIT_SHORT_SHA}"
export REDIS_HOST="twitter-slack-redis"
export REDIS_PORT=6379
