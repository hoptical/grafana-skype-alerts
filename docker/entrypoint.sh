#!/bin/sh
exec gunicorn -b 0.0.0.0:8080 --limit-request-line 0 --chdir skype_notifier  --log-level=info app:app
