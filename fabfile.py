from contextlib import contextmanager as _contextmanager

from fabric.api import env, run, cd, prefix
from fabric.colors import green, red, yellow

# Set deploy env before deployment

env.directory = 'project/family'
env.activate = 'source ~/project/djapp/bin/activate' #virualenv path on server

env.user = "webadmin"
DEPLOY_ENV = input("Provide env (dev/prod): ")
if DEPLOY_ENV not in ['dev', 'prod']:
    print(red("Wrong env provided, aborting"))
    exit()

if DEPLOY_ENV == 'dev':
    env.hosts = ['x.x.x.x']
elif DEPLOY_ENV == 'prod':
    env.hosts = ['x.x.x.x']


def deploy():
    print(yellow("DEPLOYING to [%s]- %s" % (DEPLOY_ENV, env.hosts)))
    print("\n\n")
    go_ahead = input("Deployment to [%s] Type yes to confirm deployment: " % DEPLOY_ENV.upper())
    if go_ahead.upper() == "YES":
        with virtualenv():
            update_code()
            update_pip_requirements()
            #migarte()
            reload_application_on_server()
        print(green("Successfull"))
    else:
        print(red("Aborted deployment"))


def update_code():
    print("\n\n")
    print("========================================")
    print(yellow("UPDATING CODE"))
    run("git pull")
    print(green("Done"))
    print("\n")


def update_pip_requirements():
    print("\n\n")
    print("========================================")
    print(yellow("UPDATING PIP PACKAGES"))
    run("pip install -r settings/requirements.pip")
    print(green("Done"))
    print("\n")


def migarte():
    print("\n\n")
    print("========================================")
    print(yellow("Migrating"))
    run("python manage.py migrate")
    print(green("Done"))
    print("\n")


def reload_application_on_server():
    print("\n\n")
    print("========================================")
    print(yellow("RELOADING APPLICATION ON SERVER"))
    run("sudo service supervisor stop")
    run("sudo service supervisor start")
    print(green("Done"))
    print("\n")


@_contextmanager
def virtualenv():
    with cd(env.directory):
        with prefix(env.activate):
            yield
