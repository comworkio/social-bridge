# Twitter slack

A python asynchronous worker which subscribe to twitter account and hashtags and Slack them.

![slack](./img/slack.png)

It pulls the twitter API every minutes (you can configure the pool period in the [environment variables](./.env.dist)) and filter the result to a list of twitter accounts and hashtags.

It also uses redis for storing tweets already processed during 24h (you can configure the TTL in the [environment variables](./.env.dist)).

## Git repositories

* Main repo: https://gitlab.comwork.io/oss/twitter-slack
* Github mirror: https://github.com/idrissneumann/twitter-slack.git
* Gitlab mirror: https://gitlab.com/ineumann/twitter-slack.git
* Froggit mirror: https://lab.frogg.it/ineumann/twitter-slack.git

## Image on the dockerhub

The image is available and versioned here: https://hub.docker.com/r/comworkio/twitter-slack

## Getting started locally

```shell
$ cp .env.dist .env # replace the environment values in this file
$ docker-compose -f docker-compose-local.yml up --force-recreate
```

And if you want to change the python sources, don't forget to rebuild:

```shell
$ cp .env.dist .env # replace the environment values in this file
$ docker-compose -f docker-compose-local.yml up --force-recreate --build
```
