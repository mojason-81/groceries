#!/usr/bin/bash
echo "Using python from ..."
which python

echo
echo "Don't forget to set your env vars wherever you're running your flask app and rq worker(s)"
echo
# echo "MAIL_SERVER should be set to localhost"
# echo "MAIL_PORT should be set to 8025"

echo
echo "Starting debugging server..."
export MAIL_SERVER='localhost'
export MAIL_PORT='8025'
python -m smtpd -n -c DebuggingServer localhost:8025
