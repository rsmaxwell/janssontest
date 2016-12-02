
import sys
import shutil
import buildsystem
from distutils.dir_util import copy_tree


####################################################################################################
# Clean
####################################################################################################

def clean(config, dirs, aol, packaging):
    shutil.rmtree(dirs.build, ignore_errors=True)


####################################################################################################
# Generate
####################################################################################################

def generate(config, dirs, aol, packaging):

    copy_tree(src, source)

    for dependency in config['dependencies']:

        groupId = dependency.get('groupId')
        artifactId = dependency.get('artifactId')
        version = dependency.get('version')
        packaging = dependency.get('packaging', 'zip')

        reposArtifactId = artifactId.replace('-', '/')
        reposArtifactId = reposArtifactId.replace('.', '-')

        mavenGroupId = groupId + '.' + reposArtifactId
        mavenArtifactId = artifactId + '-' + aol

        if buildsystem.info(config):
            print('dependency:')
            print('    groupId = ' + groupId)
            print('    artifactId = ' + artifactId)
            print('    mavenGroupId = ' + mavenGroupId)
            print('    mavenArtifactId = ' + mavenArtifactId)
            print('    version = ' + version)
            print('    aol = ' + aol.name)

        buildsystem.downloadArtifact(config, mavenGroupId, mavenArtifactId, version, packaging)
        buildsystem.expandArtifact(config, mavenGroupId, mavenArtifactId, version, packaging, dependances)


####################################################################################################
# Configure
####################################################################################################

def configure(config, dirs, aol, packaging):
    pass

####################################################################################################
# Make
####################################################################################################

def make(config, dirs, aol, packaging):

    if buildsystem.info(config):
        print('make:')
        print('    source = ' + dirs.source)
        print('    sourcesrc = ' + dirs.sourcesrc)
        print('    output = ' + dirs.output)
        print('    operatingSystem = ' + operatingSystem)
        print('    aol = ' + aol)

    if not os.path.exists(dirs.output):
        os.makedirs(dirs.output)

    environ = buildsystem.getBuildInfo(config, os.environ)
    environ['BUILD_TYPE'] = 'normal'
    environ['SOURCE_DIR'] = os.path.abspath(src + '/c')
    environ['BUILD_DIR'] = dirs.build

    makefile = os.path.abspath(dirs.src + '/make/' + aol + '.makefile')
    print('makefile = ' + makefile)

    buildsystem.runProgram(config, dirs.output, environ, ['make', '-f', makefile, 'all'])


####################################################################################################
# Dist
####################################################################################################

def distribution(config, dirs, aol, packaging):

    dist = os.path.abspath(dirs.build + '/dist')
    if not os.path.exists(dirs.dist):
        os.makedirs(dirs.dist)

    artifactDir = os.path.abspath(dirs.build + '/artifact')
    if not os.path.exists(artifactDir):
        os.makedirs(artifactDir)

    artifactId = config["artifactId"]
    localfile = os.path.abspath(artifactDir + '/' + artifactId + '-' + aol)
    packaging = 'zip'
    shutil.make_archive(localfile, packaging, dirs.dist)


####################################################################################################
# Deploy
####################################################################################################

def deploy(config, dirs, aol, packaging):

    groupId = config["groupId"]
    artifactId = config["artifactId"]
    version = buildsystem.multipleReplace(config["version"], config["properties"])
    packaging = 'zip'

    reposArtifactId = artifactId.replace('-', '/')
    reposArtifactId = reposArtifactId.replace('.', '-')

    mavenGroupId = groupId + '.' + reposArtifactId
    mavenArtifactId = artifactId + '-' + aol

    artifactDir = os.path.abspath(dirs.build + '/artifact')
    filename = os.path.abspath(artifactDir + '/' + mavenArtifactId + '.' + packaging)

    if buildsystem.debug(config):
        print('main: deploy')
        print('    groupId = ' + groupId)
        print('    artifactId = ' + artifactId)
        print('    mavenGroupId = ' + mavenGroupId)
        print('    mavenArtifactId = ' + mavenArtifactId)
        print('    aol = ' + aol)
        print('    version = ' + version)
        print('    packaging = ' + packaging)
        print('    filename = ' + filename)

    buildsystem.uploadArtifact(config, mavenGroupId, mavenArtifactId, version, packaging, filename)


####################################################################################################
# Call main routine
####################################################################################################

if __name__ == "__main__":
    buildsystem.main(sys.argv, clean, generate, configure, make, distribution, deploy)
