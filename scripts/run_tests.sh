#! /usr/bin/bash

export TEST=true
export DB_HOST=test_db

pytest tests ${PYTEST_OPTS}