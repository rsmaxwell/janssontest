@echo off
setlocal


rem REPOSITORY=snapshots
set REPOSITORY=releases
set PACKAGING=zip
set GROUPID=com.rsmaxwell.jansson.2-9
set ARTIFACTID=jansson-2.9-x86_64-Windows-msvc
rem VERSION=0.0.1-SNAPSHOT
set VERSION=1


set URL=http://www.rsmaxwell.co.uk/nexus/service/local/repositories/%REPOSITORY%/content


@echo on
mvn dependency:get -DgroupId=%GROUPID:.=/% -DartifactId=%ARTIFACTID% -Dversion=%VERSION% -Dpackaging=%PACKAGING% -DremoteRepositories=%URL%

dir %USERPROFILE%\.m2\repository
