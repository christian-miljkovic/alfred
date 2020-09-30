# Alfred
description

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

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

## Initializing Infrastructure
#### [Set-up] Steps
1. Build a local image and deploy it to a docker repo
2. `heroku create <app_name>` to initialize the project from your current repo
3. For container projects follow the container deploy instructions
4. If the project has a db add the postgres heroku addon

#### [WIP] Steps 
1. Configure a `heroku.yml` file 
2. Provision any add-ons and add them to the `heroku.yml` file
  - For example get the `DATABASE_URL` and add it to `heroku.yml` as a config
3. Build and push the image to heroku's image registry


## Deploying
As long as you are logged in you only need to follow the Heroku steps

### Docker
* Login into docker account jarvis2
* `$ git add` to repo
* run cmd inside directory 
`$ docker push jarvis2/argon:latest`

### Heroku 
* Log in to Container Registry
You must have Docker set up locally to continue. You should see output when you run this command.

```$ docker ps```

Now you can sign into Container Registry.

```$ heroku container:login```

Push your Docker-based app
Build the Dockerfile in the current directory and push the Docker image.

```$ heroku container:push web```

Deploy the changes
Release the newly pushed images to deploy your app.

```$ heroku container:release web```


#### Local Hosting
1. make up
2. make logs
3. ngrok http 8000 (in a new tab)

## Configuration
#### Required
`DATABASE_URL` - URL for the postgres database
`WEBFLOW_SECRET_TOKEN` - Authenticate webhook requests with a secret token in the query parameter

## Third Party Integrations
#### Twilio
[Twilio Auto Pilot Setup](https://www.twilio.com/docs/autopilot/channels/sms) How to set up autopilot with a new phone number

### Additional Reading
- [Twilio Auto Pilot](https://www.twilio.com/docs/autopilot/actions) More info about Autopilot actions 
- [Twilio Verify Phone Number](https://support.twilio.com/hc/en-us/articles/223180048-Adding-a-Verified-Phone-Number-or-Caller-ID-with-Twilio) How to verify people's phone numbers
- [How to deploy images to heroku image registry](https://devcenter.heroku.com/articles/container-registry-and-runtime)
- [How to setup a heroku.yml file](https://devcenter.heroku.com/articles/build-docker-images-heroku-yml#creating-your-app-from-setup)
- [How to include add-ons such as Postgres](https://devcenter.heroku.com/articles/heroku-postgresql)