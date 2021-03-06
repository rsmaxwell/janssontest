
import sys
import shutil
import os
import subprocess
import glob
import buildsystem
from distutils.dir_util import copy_tree


####################################################################################################
# Make
####################################################################################################

def compile(config, aol):

    buildsystem.writeCompileTimeMetadata(config, aol)

    buildsystem.mkdir(config, aol, buildsystem.BUILD_OUTPUT_MAIN_DIR)

    makefile = os.path.relpath(buildsystem.SRC_MAIN_MAKE_DIR, buildsystem.BUILD_OUTPUT_MAIN_DIR) + '/' + str(aol) + '.makefile'
    source = os.path.relpath(buildsystem.SRC_MAIN_C_DIR, buildsystem.BUILD_OUTPUT_MAIN_DIR)
    dist = os.path.relpath(buildsystem.DIST_DIR, buildsystem.BUILD_OUTPUT_MAIN_DIR)

    if aol.linker.startswith('mingw'):
        sep = '/'
    else:
        sep = os.sep

    makefile = makefile.replace('/', sep).replace('\\', sep)
    source = source.replace('/', sep).replace('\\', sep)
    dist = dist.replace('/', sep).replace('\\', sep)

    env = os.environ
    env['BUILD_TYPE'] = 'static'
    env['SOURCE'] = source
    env['DIST'] = dist
    env['INSTALL'] = buildsystem.INSTALL_DIR

    p = subprocess.Popen(['make', '-f', makefile, 'clean', 'all'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, cwd=buildsystem.BUILD_OUTPUT_MAIN_DIR)
    buildsystem.checkProcessCompletesOk(config, p, 'Error: Compile failed')




####################################################################################################
# Make check
####################################################################################################

def check(config, aol):
    pass


####################################################################################################
# Distribution
####################################################################################################

def distribution(config, aol):

    buildsystem.mkdir(config, aol, buildsystem.BUILD_ARTIFACT_DIR)
    buildsystem.mkdir(config, aol, buildsystem.BUILD_OUTPUT_MAIN_DIR)
    buildsystem.mkdir(config, aol, buildsystem.DIST_DIR)
    buildsystem.mkdir(config, aol, buildsystem.DIST_BIN_DIR)

    for file in glob.iglob(buildsystem.BUILD_OUTPUT_MAIN_DIR + 'janssontest*.exe'):
        shutil.copy2(file, buildsystem.DIST_BIN_DIR)

    artifactId = config["artifactId"]
    localfile = buildsystem.BUILD_ARTIFACT_DIR + artifactId + '-' + str(aol)
    shutil.make_archive(localfile, buildsystem.PACKAGING, buildsystem.DIST_DIR)


####################################################################################################
# Call main routine
####################################################################################################

if __name__ == "__main__":
    buildsystem.main(compile=compile, check=check, distribution=distribution)
