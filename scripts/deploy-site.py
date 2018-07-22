import os
import shutil
from subprocess import call
import git
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--push', action='store_true')
args = parser.parse_args()

script_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.join(script_dir,'..')
thumbnail_dir = os.path.join(root_dir, 'images/photography/thumbnails')
site_dir = os.path.join(root_dir,'_site')
setup_photos_script = os.path.join(root_dir, 'scripts/setup-photos.py')

os.chdir(root_dir)
shutil.rmtree(thumbnail_dir, ignore_errors=True)
execfile(setup_photos_script)

if args.push:
    call(['jekyll', 'build', '--destination','_site'])
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha
    os.chdir(site_dir)
    git_commit_ret = call(['git','cma','deploying from '+sha])
    if git_commit_ret is 0:
        if call(['git','push']) is 0:
            print 'Deployment success'
        else:
            print 'Deployment failed, could not push'
    else:
        print 'Deployment failed, could not commit _site'
else:
    print 'Deployment not requested'

