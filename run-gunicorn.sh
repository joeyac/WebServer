#!/bin/bash

NAME="OJ"                                  # Name of the application
DJANGODIR=/home/rhyme/code/DEV/oj-master           # Django project directory
SOCKFILE=/home/rhyme/code/DEV/run/gunicorn.sock  # we will communicte using this unix socket
LOGFILE=/home/rhyme/code/DEV/run/gunicorn.log
USER=rhyme                                        # the user to run as
NUM_WORKERS=4                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=oj.settings             # which settings file should Django use
DJANGO_WSGI_MODULE=oj.wsgi                     # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec /usr/local/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=LOGFILE