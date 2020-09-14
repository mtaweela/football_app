# FootBall App

Simple app showing all football players and enabling you to compose teams.

[Live preview](https://football.dev01.dev/)

## Application Components

### Back End

Composed of two parts.

- Simple server Implementation
- Simple two API endpoints (using the server upove)

You could find

#### Server Implementation

In the folder `backend_app/web_server` you you find the `wsgi_handler.py` module that contains different classes for handling the Server requests. Like:

- `WSGIHandler`
- `Router`
- `MiddlewareHandler`
- `Request`
- `JsonResponse`
- `Logger`
- `ExciptoinsHandler`

WSGIHandler is called by `uwsgi` command line and handles the request cycle after that.

#### API Endpoints App

You could find this in `backend_app/app` in `index.py` module.

There are two API endpoints for handling two different requests:

1. List players and search in them including handling pagination
2. Team builder end point

#### Team Builder Module

Team Builder class could be found in the module `backend_app/app/utils.py`.

This class implements kind of greedy algorithm for grtting the best team giving a money amount.

### Front End

Vue Single page Application caliing the APIs and presenting the data.

## Installation and developing

make a copy of .docker.env.example and call it .docker.env
make sure to change the credentials inside by you own.

then run:

```bash
make install_front
make dev
```

then you could access the frontend on `localhost:80`

## User Docker

first time run:

```bash
make install_front
make build_front
make prod
```
