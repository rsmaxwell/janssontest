
import sys
import shutil
import os
import buildsystem
from distutils.dir_util import copy_tree


####################################################################################################
# Clean
####################################################################################################

def clean(config, aol):
    buildsystem.defaultClean(config, aol)


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

    makefile = os.path.relpath(buildsystem.MAKE_DIR, buildsystem.OUTPUT_DIR) + '\\' + str(aol) + '.makefile'

    environ = os.environ
    environ['BUILD_TYPE'] = 'normal'
    environ['SOURCE'] = os.path.relpath(buildsystem.SOURCESRC_DIR, buildsystem.OUTPUT_DIR)
    environ['OUTPUT'] = '.'
    buildsystem.runProgram(config, buildsystem.OUTPUT_DIR, os.environ, ['make', '-f', makefile, 'clean', 'all'])


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
# Deploy
####################################################################################################

def deploy(config, aol):

    groupId = config["groupId"]
    artifactId = config["artifactId"]
    version = buildsystem.multipleReplace(config["version"], config["properties"])

    reposArtifactId = artifactId.replace('-', '/')
    reposArtifactId = reposArtifactId.replace('.', '-')

    mavenGroupId = groupId + '.' + reposArtifactId
    mavenArtifactId = artifactId + '-' + str(aol)

    filename = buildsystem.ARTIFACT_DIR + mavenArtifactId + '.' + buildsystem.PACKAGING

    if buildsystem.debug(config):
        print('main: deploy')
        print('    groupId = ' + groupId)
        print('    artifactId = ' + artifactId)
        print('    mavenGroupId = ' + mavenGroupId)
        print('    mavenArtifactId = ' + mavenArtifactId)
        print('    aol = ' + str(aol))
        print('    version = ' + version)
        print('    filename = ' + filename)

    buildsystem.uploadArtifact(config, mavenGroupId, mavenArtifactId, version, filename)


####################################################################################################
# Call main routine
####################################################################################################

if __name__ == "__main__":
    buildsystem.main(sys.argv, clean, generate, configure, make, distribution, deploy)
