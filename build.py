
import sys
import shutil
import os
import buildsystem
from distutils.dir_util import copy_tree


SOURCE_C_DIR       = './build/source/c/'
SOURCE_MAKE_DIR    = './build/source/make/'

####################################################################################################
# Generate
####################################################################################################

def generate(config, aol):

    copy_tree(buildsystem.SRC_DIR, buildsystem.SOURCE_DIR)

    for dependency in config['dependencies']:

        groupId = dependency.get('groupId')
        artifactId = dependency.get('artifactId')
        version = dependency.get('version')
        packaging = dependency.get('packaging', 'zip')

        reposArtifactId = artifactId.replace('-', '/')
        reposArtifactId = reposArtifactId.replace('.', '-')

        mavenGroupId = groupId + '.' + reposArtifactId
        mavenArtifactId = artifactId + '-' + str(aol)

        if buildsystem.info(config):
            print('dependency:')
            print('    groupId = ' + groupId)
            print('    artifactId = ' + artifactId)
            print('    mavenGroupId = ' + mavenGroupId)
            print('    mavenArtifactId = ' + mavenArtifactId)
            print('    version = ' + version)
            print('    aol = ' + str(aol))

        buildsystem.downloadArtifact(config, mavenGroupId, mavenArtifactId, version)
        buildsystem.expandArtifact(config, mavenGroupId, mavenArtifactId, version, buildsystem.DEPENDENCIES_DIR)


####################################################################################################
# Configure
####################################################################################################

def configure(config, aol):
    pass

####################################################################################################
# Make
####################################################################################################

def make(config, aol):

    buildsystem.mkdir_p(buildsystem.OUTPUT_DIR)

    makefile = os.path.relpath(SOURCE_MAKE_DIR, buildsystem.OUTPUT_DIR) + '\\' + str(aol) + '.makefile'

    print("**** make ****")

    env = buildsystem.getBuildInfo(config, os.environ)
    env['BUILD_TYPE'] = 'normal'
    env['SOURCE_DIR'] = os.path.relpath(SOURCE_C_DIR, buildsystem.OUTPUT_DIR)
    env['OUTPUT_DIR'] = '.'
    buildsystem.runProgram(config, buildsystem.OUTPUT_DIR, env, ['make', '-f', makefile, 'clean', 'all'])


####################################################################################################
# Dist
####################################################################################################

def distribution(config, aol):

    buildsystem.mkdir_p(buildsystem.DIST_DIR)
    buildsystem.mkdir_p(buildsystem.ARTIFACT_DIR)

    artifactId = config["artifactId"]
    localfile = buildsystem.ARTIFACT_DIR + artifactId + '-' + str(aol)
    shutil.make_archive(localfile, buildsystem.PACKAGING, buildsystem.DIST_DIR)


####################################################################################################
# Call main routine
####################################################################################################

if __name__ == "__main__":
    clean = None
    deploy = None
    run = None
    buildsystem.main(sys.argv, clean, generate, configure, make, distribution, run, deploy)
