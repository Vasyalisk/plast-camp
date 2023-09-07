#! /usr/bin/bash

pybabel compile -d translations/locales
python manage.py upgrade-zero-migration
aerich upgrade
python manage.py create-default-superadmin
uvicorn main:app --host ${HOST:-0.0.0.0} --port ${PORT:-8000} --proxy-headers --forwarded-allow-ips='*'