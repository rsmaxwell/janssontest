@echo off
setlocal


set SOURCE_DIR=C:\Users\rmaxwell\git\home\jansson-test\src\jansson-test\c
set buildLabel=8
set DEPENDANCES_HEADERS_DIR=C:\Users\rmaxwell\git\home\jansson-test\dependances\headers
set DEPENDANCES_LIBS_DIR=C:\Users\rmaxwell\git\home\jansson-test\dependances\libs
set DIST_DIR=C:\Users\rmaxwell\git\home\jansson-test\build\dist

cd C:\Users\rmaxwell\git\home\jansson-test
rd /q /s build
mkdir build\output
mkdir build\dist
cd build\output

echo on
make -f C:\Users\rmaxwell\git\home\jansson-test\src\jansson-test\make\x86_64-Windows-msvc.makefile
