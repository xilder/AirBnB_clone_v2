#!/usr/bin/python3
"""
generates a .tgz archive from the contents of the
web_static folder of your AirBnB Clone repo
"""
from fabric.api import local, run, put, env
from datetime import datetime
from os import path

env.hosts = ["100.25.139.50", "54.172.110.198"]


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
    try:
        if not path.exists(archive_path):
            return False

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
