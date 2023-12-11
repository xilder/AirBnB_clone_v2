#!/usr/bin/python3
"""
generates a .tgz archive from the contents of the
web_static folder of your AirBnB Clone repo
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """generates a tgz archive"""
    try:
        time = datetime.now().strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        file_name = f"versions/web_static_{time}"
        local(f"tar -czvf {file_name}.tgz web_static/")
        return f"{file_name}"
    except exception as e:
        return None
