#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""
from fabric.api import put, run, env
from os import path

env.hosts = ["100.25.139.50", "54.172.110.198"]


def do_deploy(archive_path):
    """
    Uploads and unpacks an archive on the server
    Args:
        archive_path (str): The path to the archived static files.
    """
    if not path.exists(archive_path):
       return False

    archive_name = path.basename(archive_path)
    folder_name = archive_name.replace(".tgz", "")
    folder_path = f"/data/web_static/releases/{folder_name}/"
    try:
        put(archive_path, f"/tmp/")
        run(f"sudo mkdir -p {folder_path}")
        run(f"sudo tar -xzf /tmp/{archive_name} -C {folder_path}")
        run(f"sudo rm /tmp/{archive_name}")
        run(f"sudo mv {folder_path}web_static/* {folder_path}")
        run(f"sudo rm -rf {folder_path}web_static")
        run(f"sudo rm -rf /data/web_static/current")
        run(f"sudo ln -s {folder_path} /data/web_static/current")
        print('New version deployed!')
        return True
    except Exception:
        return False
