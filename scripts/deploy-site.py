import os, sys
import shutil
from subprocess import call
import git
import argparse
from distutils.dir_util import copy_tree

def remove(path):
    """ param <path> could either be relative or absolute. """
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)  # remove the file
    elif os.path.isdir(path):
        shutil.rmtree(path)  # remove dir and all contains
    else:
        raise ValueError("file {} is not a file or dir.".format(path))

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
with open(setup_photos_script, 'r') as f:
    exec(f.read())

if args.push:
    print("\nBuild Jekyll site")
    if sys.platform != "win32":
        call(['bundle','exec','jekyll', 'build', '--destination','_site'])
    else:
        os.system('bundle exec jekyll build --destination _site')
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha
    os.chdir(site_dir)

    print("\nAdd to git repo and commit")
    git_commit_ret = call(['git','commit', '-am', 'deploying from '+sha])
    if git_commit_ret == 0:
        if call(['git','push']) == 0:
            print ('Blog push success')
            web_repo = git.Repo(search_parent_directories=True)
            web_sha = web_repo.head.object.hexsha
            web_dir = os.path.join(root_dir,'../website')
            os.chdir(web_dir)
            old_content = os.listdir(web_dir)
            for clean_up in old_content:
                if not clean_up.endswith('.git'):    
                    remove(clean_up)
            copy_tree(site_dir, web_dir)
            web_commit_ret = call(['git','commit', '-am','deploying from '+web_sha])
            if web_commit_ret == 0:
                if call(['git','push']) == 0:
                    print ('Web Deployment succes')
        else:
            print ('Deployment failed, could not push')
    else:
        print ('Deployment failed, could not commit _site')
else:
    print ('Deployment not requested')

