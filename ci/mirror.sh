#!/bin/bash

REPO_PATH="${PROJECT_HOME}/twitter-slack/"

cd "${REPO_PATH}" && git pull origin main || :
git push github main -f
git push pgitlab main -f
git push froggit main -f
exit 0