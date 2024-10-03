#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import put, run, env
from os.path import exists

# Define the web servers' IP addresses
env.hosts = ['52.23.237.49', '54.205.189.207']

def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    
    # Check if the archive exists
    if not exists(archive_path):
        return False

    try:
        # Extract the filename and its name without the extension
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"

        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Create the release directory
        run('mkdir -p {}{}/'.format(path, no_ext))

        # Uncompress the archive to the release directory
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))

        # Remove the archive from the web server
        run('rm /tmp/{}'.format(file_n))

        # Move the contents from web_static to the release directory
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))

        # Remove the now-empty web_static directory
        run('rm -rf {}{}/web_static'.format(path, no_ext))

        # Delete the existing symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))

        return True

    except Exception as e:
        print(f"Error: {e}")  # Print the error message for debugging
        return False
