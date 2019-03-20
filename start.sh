rm /etc/nginx/sites-enabled/lostfound_djangoservice.conf
ln -s /data/app/LostFoundDjangoService/lostfound_djangoservice.conf /etc/nginx/sites-enabled/lostfound_djangoservice.conf
uwsgi --ini uwsgi.ini  
nginx -s reload  