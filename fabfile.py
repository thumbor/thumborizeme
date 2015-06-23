import requests
from fabric.api import * # NOQA

HOSTS = {
    #'thumbor': [
        #{
            #'host': '192.241.167.88',
            #'username': 'root'
        #}
    #],
    'thumbor': [
        {
            'host': '104.236.46.59',
            'username': 'root'
        }
    ]
}


@task
def deploy():
    for host in HOSTS['thumbor']:
        with settings(host_string='%s@%s' % (
                host['username'],
                host['host'])):

            run('mkdir -p /var/logs/')
            run('mkdir -p /var/run/')
            run('mkdir -p /tmp/thumbor/')

            run('sudo aptitude update')
            r = requests.get('https://raw.githubusercontent.com/thumbor/thumbor/master/requirements')
            deps = r.content.replace('\n', ' ')
            run('sudo aptitude install -y unzip python python-dev python-setuptools supervisor nginx wget python-lxml libssl-dev redis-server libhiredis-dev ffmpeg %s' % deps)
            run('sudo easy_install pip')
            run('sudo pip install --upgrade setuptools')
            run('sudo pip install -U thumbor cssselect toredis')

            put('./supervisor.conf', '/etc/supervisor/supervisord.conf', use_sudo=True)
            put('./thumbor.conf', '/etc/thumbor.conf', use_sudo=True)
            put('./nginx.conf', '/etc/nginx/sites-available/default', use_sudo=True)

            run('mkdir -p /tmp/current')
            run('rm -rf /tmp/master*')
            run('cd /tmp && wget https://github.com/heynemann/thumborizeme/archive/master.zip')
            run('cd /tmp && unzip master.zip')
            run('rm -rf /tmp/current && mv /tmp/thumborizeme-master /tmp/current')

            with settings(warn_only=True):
                run('sudo /etc/init.d/nginx stop')
                run("ps aux | egrep supervisor | egrep -v egrep | awk ' { print $2 } ' | xargs kill -9")
                run("ps aux | egrep thumbor | egrep -v egrep | awk ' { print $2 } ' | xargs kill -9")
                run("ps aux | egrep app.py  | egrep -v egrep | awk ' { print $2 } ' | xargs kill -9")
                run('sudo /etc/init.d/supervisor stop')
                run('sudo /etc/init.d/supervisor start')
                run('sudo /etc/init.d/nginx stop')
                run('sudo /etc/init.d/nginx start')
