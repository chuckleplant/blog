import os
import shutil
from subprocess import call
import git


script_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.join(script_dir,'..')
thumbnail_dir = os.path.join(root_dir, 'images/photography/thumbnails')
site_dir = os.path.join(root_dir,'_site')
setup_photos_script = os.path.join(root_dir, 'scripts/setup-photos.py')



os.chdir(root_dir)
#shutil.rmtree(thumbnail_dir, ignore_errors=True)
#execfile(setup_photos_script)
#call(['jekyll', 'build', '--destination','_site'])

repo = git.Repo(search_parent_directories=True)
sha = repo.head.object.hexsha

os.chdir(site_dir)
call(['git','cma','"'+sha+' deployment requested"'])
