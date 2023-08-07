#!/bin/sh
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $SCRIPT_DIR/..

if [ -z ${DJANGO_SUPERUSER_USERNAME+x} ]; then
  echo "DJANGO_SUPERUSER_USERNAME is unset";
else
  echo "DJANGO_SUPERUSER_USERNAME is set, creating superuser...";
  python manage.py createsuperuser \
	  --username "${DJANGO_SUPERUSER_USERNAME}" \
	  --email "${DJANGO_SUPERUSER_EMAIL}" \
	  --noinput
fi
if [ -z ${DJANGO_SUPERUSER_PASSWORD+x} ]; then
  echo "DJANGO_SUPERUSER_PASSWORD is unset";
else
  echo "DJANGO_SUPERUSER_PASSWORD is set, changing password...";
  python manage.py shell << EOF
from django.contrib.auth.models import User
usr = User.objects.get(username='${DJANGO_SUPERUSER_USERNAME}')
usr.set_password('${DJANGO_SUPERUSER_PASSWORD}')
usr.save()
EOF
fi

## Add VAST AUTH 2.0 site...
if [ -z ${VASTAUTH_SECRET+x} ]; then
  echo "VASTAUTH_SECRET is unset";
else
  echo "VASTAUTH_SECRET is set, registering site...";
  python manage.py shell << EOF
from allauth.socialaccount.models import *
from django.contrib.sites.models import *
sites = Site.objects.all()
obj = SocialApp.objects.create(provider='vastauth2', name='VAST Authentication', client_id='${VASTAUTH_CLIENTID}', secret='${VASTAUTH_SECRET}')
obj.save()
obj.sites.set(sites)
EOF
fi

exit 0
