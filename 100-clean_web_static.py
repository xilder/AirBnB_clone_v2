#!/usr/bin/python3
"""
generates a .tgz archive from the contents of the
web_static folder of your AirBnB Clone repo
"""
from fabric.api import local, run, put, env, runs_once
from datetime import datetime
from os import path

env.hosts = ["100.25.139.50", "54.172.110.198"]

@runs_once
def do_pack():
    """generates a tgz archive"""
    try:
        time = datetime.now().strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        file_name = f"versions/web_static_{time}"
        local(f"tar -czvf {file_name}.tgz web_static/")
        return f"{file_name}.tgz"
    except exception as e:
        return None


def do_deploy(archive_path):
    """
    Uploads and unpacks an archive on the server
    Args:
        archive_path (str): The path to the archived static files.
    """
    
    if not path.exists(archive_path):
        return False
    try:
        archive_name = path.basename(archive_path)
        folder_name = archive_name.replace(".tgz", "")
        folder_path = f"/data/web_static/releases/{folder_name}/"
        put(archive_path, f"/tmp/{archive_name}")
        run(f"sudo mkdir -p {folder_path}")
        run(f"sudo tar -xzf /tmp/{archive_name} -C {folder_path}")
        run(f"sudo rm /tmp/{archive_name}")
        run(f"sudo mv {folder_path}web_static/* {folder_path}")
        run(f"sudo rm -rf {folder_path}web_static")
        run(f"sudo rm -rf /data/web_static/current")
        run(f"sudo ln -sf {folder_path} /data/web_static/current")
        print('New version deployed!')
        return True
    except Exception:
        return False


def deploy():
    "creates and deploys site"
    file_d = do_pack()
    if file_d is None:
        return False
    return do_deploy(file_d)


def do_clean(number=0):
    """Deletes out-of-date archives"""

    archives = os.listdir('versions/')
    archives.sort(reverse=True)
    idx = int(number)
    if not idx:
        idx += 1
        if idx < len(archives):
            archives = archives[idx:]
        else:
            archives = []
        for archive in archives:
            os.unlink(f"./versions/{archive}")
        cmd_parts = [
                "rm -rf $(",
                "find /data/web_static/releases/ -maxdepth 1 -type d -iregex",
                " '/data/web_static/releases/web_static_.*'",
                " | sort -r | tr '\\n' ' ' | cut -d ' ' -f{}-)".format(idx + 1)
                ]
        run(''.join(cmd_parts))
