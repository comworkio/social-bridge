# Twitter slack

A python asynchronous worker which subscribe to twitter account and hashtags and send them to Slack or Discord.

![slack](./img/slack.png)

It pulls the twitter API every minutes (you can configure the pool period in the environment's variables) and filter the result to a list of twitter accounts and hashtags.

It also uses redis for storing tweets already processed during 24h (you can configure the TTL in the environment variables).

## Environment's variables

The variables available are listed in the [.env.dist](./.env.dist) file.

Notes:
* The difference between `SLACK_TOKEN` and `SLACK_PUBLIC_TOKEN_X` is the following: the errors will also be published with `SLACK_TOKEN`.
* In order to use discord instead of slack, you just have to replace the variable `SLACK_TOKEN` by `DISCORD_TOKEN` or `SLACK_PUBLIC_TOKEN_X` by `DISCOVER_PUBLIC_TOKEN_X`. You can also use both (you'll have to define all variables).

## Git repositories

* Main repo: https://gitlab.comwork.io/oss/twitter-slack
* Github mirror: https://github.com/idrissneumann/twitter-slack.git
* Gitlab mirror: https://gitlab.com/ineumann/twitter-slack.git
* Froggit mirror: https://lab.frogg.it/ineumann/twitter-slack.git

## Image on the dockerhub

The image is available and versioned here: https://hub.docker.com/r/comworkio/twitter-slack

You'll find tags for arm32/aarch64 (optimized for raspberrypi) and x86/amd64 tags:

![tags](./img/tags.png)

## Getting started

```shell
$ cp .env.dist .env # replace the environment values in this file
$ docker-compose -f docker-compose-local.yml up --force-recreate
```

And if you want to change the python sources, don't forget to rebuild:

```shell
$ cp .env.dist .env # replace the environment values in this file
$ docker-compose -f docker-compose-local.yml up --force-recreate --build
```
