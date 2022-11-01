#!/usr/bin/env bash

source ./ci/compute-env.sh

ENV_FILE="twitter_slack.env"

echo "" > ${ENV_FILE}
echo "LOG_LEVEL=${LOG_LEVEL}" >> ${ENV_FILE}
echo "WAIT_TIME=${WAIT_TIME}" >> ${ENV_FILE}
echo "KEYWORD_WAIT_TIME=${KEYWORD_WAIT_TIME}" >> ${ENV_FILE}

env|grep -E "^(TWITTER_|DISCORD_|SLACK_|REDIS_|MASTODON_|UPRODIT_)"|while read -r; do
  echo "${REPLY}" >> "${ENV_FILE}"
done

CROSS_ENV_FILE="cross_slack.env"
echo "" > ${CROSS_ENV_FILE}
echo "LOG_LEVEL=${LOG_LEVEL}" >> ${CROSS_ENV_FILE}
echo "WAIT_TIME=${WAIT_TIME}" >> ${CROSS_ENV_FILE}
echo "KEYWORD_WAIT_TIME=${KEYWORD_WAIT_TIME}" >> ${CROSS_ENV_FILE}

env|grep -E "^(MASTODON_|CROSS_)"|while read -r; do
  echo "${REPLY//CROSS_}" >> "${CROSS_ENV_FILE}"
done

docker rmi -f "comworkio/twitter-slack:${TWITTER_SLACK_VERSION}" || :
docker-compose -f docker-compose-intra.yml up -d --force-recreate
