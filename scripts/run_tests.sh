#! /bin/bash

PYTEST_OPTS="$* ${PYTEST_OPTS}"

export TEST=true
export REDIS_DB=10

# fakeredis issue with authed connections
export REDIS_PASSWORD=

pytest ${PYTEST_OPTS} -vv -n auto
