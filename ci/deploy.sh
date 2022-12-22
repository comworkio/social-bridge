#!/usr/bin/env bash

source ./ci/compute-env.sh

ENV_FILE="twitter_slack.env"

echo "" > ${ENV_FILE}
echo "LOG_LEVEL=${LOG_LEVEL}" >> ${ENV_FILE}
echo "WAIT_TIME=${WAIT_TIME}" >> ${ENV_FILE}
echo "KEYWORD_WAIT_TIME=${KEYWORD_WAIT_TIME}" >> ${ENV_FILE}
echo "SOCIAL_BRIDGE_VERSION=${SOCIAL_BRIDGE_VERSION}" >> ${ENV_FILE}
echo "STREAM_PRIMARY_SRC=${STREAM_PRIMARY_SRC}" >> ${ENV_FILE}

env|grep -E "^(TWITTER_|DISCORD_|SLACK_|REDIS_|MASTODON_|UPRODIT_|PROD_DOMAIN_MATCH_)"|while read -r; do
  echo "${REPLY}" >> "${ENV_FILE}"
done

docker rmi -f "comworkio/social-bridge:${SOCIAL_BRIDGE_VERSION}" || :
docker ps|awk '($0 ~ "(twitter-slack|cross)"){system("docker rm -f "$1)}' || :
docker-compose -f docker-compose-intra.yml up -d --force-recreate
