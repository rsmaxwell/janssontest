
import sys
import shutil
import os
import glob
import buildsystem
from distutils.dir_util import copy_tree


####################################################################################################
# Make
####################################################################################################

def compile(config, aol):

    buildsystem.mkdir_p(buildsystem.BUILD_OUTPUT_MAIN_DIR)

    makefile = os.path.relpath(buildsystem.SRC_MAIN_MAKE_DIR, buildsystem.BUILD_OUTPUT_MAIN_DIR) + '\\' + str(aol) + '.makefile'

    env = buildsystem.getBuildInfo(config, os.environ)
    env['BUILD_TYPE'] = 'normal'
    env['SOURCE'] = os.path.relpath(buildsystem.SRC_MAIN_C_DIR, buildsystem.BUILD_OUTPUT_MAIN_DIR)
    env['OUTPUT'] = '.'
    stdout, stderr, returncode = buildsystem.runProgram(config, buildsystem.BUILD_OUTPUT_MAIN_DIR, env, ['make', '-f', makefile, 'clean', 'all'])
    if returncode != 0:
        print('Error running make')
        sys.exit(3)


####################################################################################################
# Distribution
####################################################################################################

def distribution(config, aol):

    buildsystem.mkdir_p(buildsystem.BUILD_ARTIFACT_DIR)
    buildsystem.mkdir_p(buildsystem.BUILD_OUTPUT_MAIN_DIR)
    buildsystem.mkdir_p(buildsystem.DIST_DIR)
    buildsystem.mkdir_p(buildsystem.DIST_BIN_DIR)

    for file in glob.iglob(buildsystem.BUILD_OUTPUT_MAIN_DIR + 'janssontest*.exe'):
        shutil.copy2(file, buildsystem.DIST_BIN_DIR)

    artifactId = config["artifactId"]
    localfile = buildsystem.BUILD_ARTIFACT_DIR + artifactId + '-' + str(aol)
    shutil.make_archive(localfile, buildsystem.PACKAGING, buildsystem.DIST_DIR)


####################################################################################################
# Call main routine
####################################################################################################

if __name__ == "__main__":
    buildsystem.main(compile=compile, distribution=distribution)
