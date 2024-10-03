#!/usr/bin/python3
"""Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers."""

from fabric.api import put, run, env
from os.path import exists

# Define the web server hosts
env.hosts = ['52.23.237.49', '54.205.189.207']


def do_deploy(archive_path):
    """Distributes an archive to the web servers.

    Args:
        archive_path (str): The path to the archive to be deployed.

    Returns:
        bool: True if all operations are successful, otherwise False.
    """
    if not exists(archive_path):
        return False

    try:
        # Extract the file name and name without extension
        file_name = archive_path.split("/")[-1]
        no_ext = file_name.split(".")[0]

        # Define the release path
        path = "/data/web_static/releases/"

        # Upload the archive to /tmp/
        put(archive_path, '/tmp/')

        # Create the release directory
        run('mkdir -p {}{}/'.format(path, no_ext))

        # Uncompress the archive
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, path, no_ext))

        # Clean up the uploaded archive
        run('rm /tmp/{}'.format(file_name))

        # Move the contents of web_static
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))

        # Remove the empty web_static directory
        run('rm -rf {}{}/web_static'.format(path, no_ext))

        # Remove the current symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))

        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False
