
import sys
import shutil
import buildsystem


####################################################################################################
# Clean
####################################################################################################

def clean(config, build):
    shutil.rmtree(build, ignore_errors=True)


####################################################################################################
# Generate
####################################################################################################

def generate(config, src, source, temp, os, aol, packaging, dependances):

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
            print('    aol = ' + aol)

        buildsystem.downloadArtifact(config, mavenGroupId, mavenArtifactId, version, packaging)
        buildsystem.expandArtifact(config, mavenGroupId, mavenArtifactId, version, packaging, dependances)


####################################################################################################
# Configure
####################################################################################################

def configure(config, output, dist, operatingSystem, sourcesrc):
    pass

####################################################################################################
# Make
####################################################################################################

def make(config, src, source, sourcesrc, output, operatingSystem, aol):

    if not os.path.exists(output):
        os.makedirs(output)

    if operatingSystem == 'Windows':
        environ = os.environ
        environ['BUILD_TYPE'] = 'normal'
        environ['SOURCE_DIR'] = src
        environ['BUILD_DIR'] = build
        makefile = os.path.abspath(src + '/make/' + aol + '.makefile')
        print('makefile = ' + makefile)

        buildsystem.runProgram(config, output, environ, ['make', '-f', makefile, 'all'])

    else:     # Linux or MinGW or CygWin
        buildsystem.runProgram(config, source, os.environ, ['make', 'clean'])
        buildsystem.runProgram(config, source, os.environ, ['make'])
        buildsystem.runProgram(config, source, os.environ, ['make', 'install'])


####################################################################################################
# Dist
####################################################################################################

def distribution(config, build, aol, localfile, packaging):

    artifactDir = os.path.abspath(build + '/artifact')
    if not os.path.exists(artifactDir):
        os.makedirs(artifactDir)

    artifactId = config["artifactId"]
    localfile = os.path.abspath(artifactDir + '/' + artifactId + '-' + aol)
    packaging = 'zip'
    shutil.make_archive(localfile, packaging, build + '/dist')


####################################################################################################
# Deploy
####################################################################################################

def deploy(config, build, aol, packaging):

    groupId = config["groupId"]
    artifactId = config["artifactId"]
    version = multipleReplace(config["version"], config["properties"])
    packaging = 'zip'

    reposArtifactId = artifactId.replace('-', '/')
    reposArtifactId = reposArtifactId.replace('.', '-')

    mavenGroupId = groupId + '.' + reposArtifactId
    mavenArtifactId = artifactId + '-' + aol

    artifactDir = os.path.abspath(build + '/artifact')
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