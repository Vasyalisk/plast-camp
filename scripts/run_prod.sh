#! /usr/bin/bash

pybabel compile -d translations/locales
aerich upgrade
uvicorn main:app --host ${HOST:-0.0.0.0} --port ${PORT:-8000} --proxy-headers --forwarded-allow-ips='*'