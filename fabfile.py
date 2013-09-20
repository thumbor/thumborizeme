from fabric.api import *

HOSTS = {
    'thumbor': [
        {
            'host': '192.241.167.88',
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

            #run('sudo aptitude update')
            run('sudo aptitude install -y python python-dev python-setuptools supervisor libwebp4 webp libcurl3-openssl-dev libjpeg-dev libpng-dev nginx')
            run('sudo easy_install pip')
            run('sudo pip install --upgrade setuptools')
            run('sudo pip install -U pillow thumbor tornado')

            put('./supervisor.conf', '/etc/supervisord.conf', use_sudo=True)
            put('./thumbor.conf', '/etc/thumbor.conf', use_sudo=True)
            put('./nginx.conf', '/etc/nginx/sites-available/default', use_sudo=True)

            put('./thumborizeme', '/tmp/thumborizeme')
            run('mv /tmp/thumborizeme /tmp/current')

            with settings(warn_only=True):
                run('sudo /etc/init.d/nginx stop')
                run("ps aux | egrep thumbor | egrep -v egrep | awk ' { print $2 } ' | xargs kill -9")
                run("ps aux | egrep supervisor | egrep -v egrep | awk ' { print $2 } ' | xargs kill -9")
                run('sudo /etc/init.d/supervisor start')
                run('sudo /etc/init.d/nginx start')
