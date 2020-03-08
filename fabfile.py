from fabric.api import *
from contextlib import contextmanager as _contextmanager
import os, logging, time
import fabconfig

@_contextmanager
def virtualenv():
    with cd(env.venv_path), prefix(env.activate), cd(env.base_directory):
        yield

def set_debug():
    logging.basicConfig(level=logging.DEBUG)

def pwd():
  run("pwd")

def prod():
    env.env_code = 'prod'
    env.hosts = ['tools.biggercake.com']    
    env.base_directory = '/home/ubuntu/Narrative-AB/NarrativeABTesting'
    env.uwsgi_ini_file = '/etc/uwsgi/apps-enabled/narrative-ab.ini'
    env.venv_path = '/home/ubuntu/Narrative-AB/venv'
    env.activate = 'source %(venv_path)s/bin/activate' % env

def _restart_uwsgi(uwsgi_ini_file):
    sudo('touch {}'.format(uwsgi_ini_file))

def _pull_new_version():
    print('CDing to: {}'.format(env.base_directory))
    with cd(env.base_directory):
        run('pwd')
        run('git pull')

def _restart_uwsgi():
    sudo('touch {}'.format(env.uwsgi_ini_file))

def _pipfreeze():
  local("pip freeze > pip.txt")

def _pipinstall():
    with virtualenv():
        run("pip install -r pip.txt")

def _makemigrations():
    with virtualenv():
        run('python manage.py makemigrations')
        run('python manage.py migrate')

def deploy():
    _pipfreeze()
    _pull_new_version()
    _pipinstall()
    _makemigrations()
    _restart_uwsgi()