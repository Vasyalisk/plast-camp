#! /usr/bin/bash

uvicorn main:app --host 0.0.0.0 --proxy-headers --forwarded-allow-ips='*'