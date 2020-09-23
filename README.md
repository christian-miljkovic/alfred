# Name
description

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Build Status](https://alfred.community.com/alfred/v1/teams/main/pipelines/intake/jobs/build-publish/badge)](http://concourse.uw2.dev.sms.community:8080/teams/main/pipelines/intake)

## Next Steps
1. Use Twilio auto-pilot to take in the user information if they haven't registered before
  - Else say `welcome back`
  - get the payload from twilio by doing ngrok
2. Create conversation flow to save birthdays

## Architecture
```mermaid
sequenceDiagram
```

## Setup
#### Install [Poetry](https://poetry.eustace.io)
```
curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
```

#### Install dependencies
```
poetry install
```

#### Configure poetry to install dependencies in `.venv` directory of the project
```
poetry config settings.virtualenvs.in-project true
```

#### Intialize Alembic
1. `source .venv/bin/activate`
2. `alembic init alembic`
3. `alembic revision -m "create user table"`

## Usage
#### Run the service
```
make up
```

#### Clean up the service
```
make down
```

#### Run tests
```
make ci/test
```

#### Clean up tests
```
make ci/down
```

## Deploying
#### Steps
1. Configure a `heroku.yml` file 
2. Provision any add-ons and add them to the `heroku.yml` file
  - For example get the `DATABASE_URL` and add it to `heroku.yml` as a config
3. Build and push the image to heroku's image registry

How to deploy images to heroku image registry [link](https://devcenter.heroku.com/articles/container-registry-and-runtime)

How to setup a `heroku.yml` file [here](https://devcenter.heroku.com/articles/build-docker-images-heroku-yml#creating-your-app-from-setup)

How to include add-ons such as Postgres [here](https://devcenter.heroku.com/articles/heroku-postgresql)

## Configuration
#### Required
`DATABASE_URL` - URL for the postgres database
`WEBFLOW_SECRET_TOKEN` - Authenticate webhook requests with a secret token in the query parameter

## Third Party Integrations
#### <Name>
[Name](url-link) Description

### Additional Reading
- [Twilio-AutoPilot](https://www.twilio.com/docs/autopilot/actions)