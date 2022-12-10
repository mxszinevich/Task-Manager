#!/bin/sh
echo $HTPASSWD > /etc/nginx/.htpasswd
exec nginx -g 'daemon off;'
