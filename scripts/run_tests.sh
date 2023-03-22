#! /usr/bin/bash

export TEST=true
export REDIS_DB=10

# fakeredis issue with authed connections
export REDIS_PASSWORD=

pytest tests ${PYTEST_OPTS} -vv