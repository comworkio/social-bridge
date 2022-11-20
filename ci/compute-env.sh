#!/usr/bin/env bash

export LOG_LEVEL=INFO
export WAIT_TIME=60
export KEYWORD_WAIT_TIME=2
export TWITTER_MAX_RESULTS=100
export TWITTER_KEYWORD_1=techwatch
export TWITTER_KEYWORD_2=mirrortw
export TWITTER_USERNAME_1=IdrissNeumann
export TWITTER_OWNER_1=IdrissNeumann
export SLACK_CHANNEL="#techno-radar"
export SLACK_TRIGGER=on
export SOCIAL_BRIDGE_VERSION="${CI_COMMIT_BRANCH}-${CI_COMMIT_SHORT_SHA}"
export REDIS_HOST="social-bridge-redis"
export REDIS_PORT=6379
export REDIS_TTL=172800
export TWITTER_RETENTION_DAYS=2
export STREAM_PRIMARY_SRC=mastodon
