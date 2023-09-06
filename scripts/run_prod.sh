#! /usr/bin/bash

pybabel compile -d translations/locales
python -c 'from migrations import utils; utils.command.upgrade_zero_sync()'
aerich upgrade
python -c 'from admin import utils; utils.create_superadmin(email="${ADMIN_EMAIL}", password="${ADMIN_PASSWORD}")'
uvicorn main:app --host ${HOST:-0.0.0.0} --port ${PORT:-8000} --proxy-headers --forwarded-allow-ips='*'