@echo off
setlocal


rem DELETE /nexus/service/local/metadata/repositories/snapshots/content/com/rsmaxwell/jansson/2-9/jansson-2.9-x86_64-Windows-msvc/
rem DELETE /nexus/service/local/metadata/repositories/snapshots/content/com/rsmaxwell/jansson-test/jansson-test-x86_64-Windows-msvc/

set URL=http://www.rsmaxwell.co.uk/nexus/service/local/metadata/repositories/snapshots/content/com/rsmaxwell/jansson-test/jansson-test-x86_64-Windows-msvc/

@echo on

curl -v --request DELETE  --user "%MAXWELLHOUSE_ADMIN_USER%:%MAXWELLHOUSE_ADMIN_PASS%"  %URL%
