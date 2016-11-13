rem @echo off
setlocal


set REPOSITORY=snapshots
set PACKAGING=zip
set GROUPID=com.rsmaxwell.jansson.2-9
set ARTIFACTID=jansson-2.9-x86_64-Windows-msvc
set VERSION=0.0.1-SNAPSHOT

set REPOSITORY=releases
set VERSION=1




set URL=http://www.rsmaxwell.co.uk/nexus/service/local/repositories/%REPOSITORY%/content

set FILE=%ARTIFACTID%-%VERSION%
set FILENAME=%FILE%.zip

set ROOT=C:\Users\rmaxwell\git\home\jansson
cd %ROOT%\build\dist

@echo on

mvn deploy:deploy-file -DgroupId=%GROUPID% -DartifactId=%ARTIFACTID% -Dversion=%VERSION% -Dpackaging=%PACKAGING% -Dfile=%FILENAME% -DrepositoryId=%REPOSITORYID% -Durl=%URL%

