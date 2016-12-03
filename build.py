
import sys
import shutil
import buildsystem
from distutils.dir_util import copy_tree


####################################################################################################
# Clean
####################################################################################################

def clean(config, location, aol, packaging):
    shutil.rmtree(location.build, ignore_errors=True)


####################################################################################################
# Generate
####################################################################################################

def generate(config, location, aol, packaging):

    copy_tree(src, location.source)

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
            print('    aol = ' + str(aol))

        buildsystem.downloadArtifact(config, mavenGroupId, mavenArtifactId, version, packaging)
        buildsystem.expandArtifact(config, mavenGroupId, mavenArtifactId, version, packaging, dependances)


####################################################################################################
# Configure
####################################################################################################

def configure(config, location, aol, packaging):
    pass

####################################################################################################
# Make
####################################################################################################

def make(config, location, aol, packaging):

    if buildsystem.info(config):
        print('make:')
        print('    source = ' + location.source)
        print('    sourcesrc = ' + location.sourcesrc)
        print('    output = ' + location.output)

    if not os.path.exists(location.output):
        os.makedirs(location.output)

    environ = buildsystem.getBuildInfo(config, os.environ)
    environ['BUILD_TYPE'] = 'normal'
    environ['SOURCE_DIR'] = os.path.abspath(src + '/c')
    environ['BUILD_DIR'] = location.build

    makefile = os.path.abspath(location.src + '/make/' + str(aol) + '.makefile')
    print('makefile = ' + makefile)

    buildsystem.runProgram(config, location.output, environ, ['make', '-f', makefile, 'all'])


####################################################################################################
# Dist
####################################################################################################

def distribution(config, location, aol, packaging):

    dist = os.path.abspath(location.build + '/dist')
    if not os.path.exists(location.dist):
        os.makedirs(location.dist)

    artifactDir = os.path.abspath(location.build + '/artifact')
    if not os.path.exists(artifactDir):
        os.makedirs(artifactDir)

    artifactId = config["artifactId"]
    localfile = os.path.abspath(artifactDir + '/' + artifactId + '-' + str(aol))
    packaging = 'zip'
    shutil.make_archive(localfile, packaging, location.dist)


####################################################################################################
# Deploy
####################################################################################################

def deploy(config, location, aol, packaging):

    groupId = config["groupId"]
    artifactId = config["artifactId"]
    version = buildsystem.multipleReplace(config["version"], config["properties"])

    reposArtifactId = artifactId.replace('-', '/')
    reposArtifactId = reposArtifactId.replace('.', '-')

    mavenGroupId = groupId + '.' + reposArtifactId
    mavenArtifactId = artifactId + '-' + str(aol)

    artifactDir = os.path.abspath(location.build + '/artifact')
    filename = os.path.abspath(artifactDir + '/' + mavenArtifactId + '.' + packaging)

    if buildsystem.debug(config):
        print('main: deploy')
        print('    groupId = ' + groupId)
        print('    artifactId = ' + artifactId)
        print('    mavenGroupId = ' + mavenGroupId)
        print('    mavenArtifactId = ' + mavenArtifactId)
        print('    aol = ' + str(aol))
        print('    version = ' + version)
        print('    packaging = ' + packaging)
        print('    filename = ' + filename)

    buildsystem.uploadArtifact(config, mavenGroupId, mavenArtifactId, version, packaging, filename)


####################################################################################################
# Call main routine
####################################################################################################

if __name__ == "__main__":
    buildsystem.main(sys.argv, clean, generate, configure, make, distribution, deploy)
