#!/usr/bin/env bash

source ./ci/compute-env.sh

ENV_FILE="twitter_slack.env"

echo "" > ${ENV_FILE}
echo "LOG_LEVEL=${LOG_LEVEL}" >> ${ENV_FILE}
echo "WAIT_TIME=${WAIT_TIME}" >> ${ENV_FILE}
echo "KEYWORD_WAIT_TIME=${KEYWORD_WAIT_TIME}" >> ${ENV_FILE}
echo "TWITTER_CONSUMER_KEY=${TWITTER_CONSUMER_KEY}" >> ${ENV_FILE}
echo "TWITTER_CONSUMER_SECRET=${TWITTER_CONSUMER_SECRET}" >> ${ENV_FILE}
echo "TWITTER_ACCESS_TOKEN=${TWITTER_ACCESS_TOKEN}" >> ${ENV_FILE}
echo "TWITTER_ACCESS_TOKEN_SECRET=${TWITTER_ACCESS_TOKEN_SECRET}" >> ${ENV_FILE}
echo "TWITTER_MAX_RESULTS=${TWITTER_MAX_RESULTS}" >> ${ENV_FILE}

env|grep -E "^(TWITTER_KEYWORD|TWITTER_USERNAME|SLACK_PUBLIC_TOKEN|DISCORD_|SLACK_|REDIS_)"|while read -r; do
  echo "${REPLY}" >> "${ENV_FILE}"
done

docker rmi -f "comworkio/twitter-slack:${UNIQ_VERSION}" || :
docker-compose -f docker-compose-intra.yml up -d --force-recreate
