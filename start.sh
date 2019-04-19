rm /etc/nginx/sites-enabled/lostfound.yiwangchunyu.wang.conf
ln -s /data/app/LostFoundDjangoService/lostfound.yiwangchunyu.wang.conf /etc/nginx/sites-enabled/lostfound.yiwangchunyu.wang.conf
python manage.py collectstatic
mkdir uwsgi
uwsgi --ini uwsgi.ini
nginx -s reload  