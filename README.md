# images-hosting

## env setup

copy `env.example` to `.env`:

```
cp env.example .env
```

open `.env` and set variables:

```
API_KEY=your_secret_key
```

## start app

build and start the containers with docker:

```
docker compose up -d --build
```
