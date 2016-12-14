
CC = cl
LD = link

CFLAGS_BASE = /c /GS /W2 /Zc:wchar_t /sdl /Zc:inline /fp:precise /WX- /Zc:forScope /RTC1 /Gd /EHsc /nologo /wd4090
CFLAGS_NODEBUG = /MD
CFLAGS_DEBUG = /MDd /Gm /Zi /Od 

DEFINES_BASE = /D_MT /DbuildLabel=$(buildLabel) /D_CRT_SECURE_NO_WARNINGS /D_CRT_SECURE_NO_DEPRECATE /D_CRT_NONSTDC_NO_DEPRECATE /D_CRT_NON_CONFORMING_SWPRINTFS
DEFINES_DEBUG = /D_DEBUG

LINKFLAGS_BASE = /MANIFEST /NXCOMPAT /MACHINE:X64 /INCREMENTAL /SUBSYSTEM:CONSOLE /MANIFESTUAC:"level='asInvoker' uiAccess='false'" /NOLOGO /TLBID:1 
LINKFLAGS_NODEBUG =
LINKFLAGS_DEBUG = /DEBUG 

# Visual Studio 2015 Compiler properties
# /GS /W3 /Zc:wchar_t /ZI /Gm /Od /sdl /Fd"x64\Debug\vc140.pdb" /Zc:inline /fp:precise 
# /D "_DEBUG" /D "_CONSOLE" /D "_UNICODE" /D "UNICODE" /D "_CRT_SECURE_NO_WARNINGS" 
# /WX- /Zc:forScope /RTC1 /Gd /MDd /EHsc /nologo 
# /Fa"x64\Debug\" /Fo"x64\Debug\" 




# Visual Studio 2015 Linker properties
# /MANIFEST /NXCOMPAT /DEBUG /MACHINE:X64 /INCREMENTAL /SUBSYSTEM:CONSOLE /MANIFESTUAC:"level='asInvoker' uiAccess='false'" /NOLOGO /TLBID:1 

# /ManifestFile:"x64\Debug\ConsoleApplication1.exe.intermediate.manifest" 
# /DYNAMICBASE "kernel32.lib" "user32.lib" "gdi32.lib" "winspool.lib" "comdlg32.lib" "advapi32.lib" "shell32.lib" "ole32.lib" "oleaut32.lib" "uuid.lib" "odbc32.lib" "odbccp32.lib" 
# /OUT:"C:\Users\Richard\Documents\Visual Studio 2015\Projects\ConsoleApplication1\x64\Debug\ConsoleApplication1.exe" 
# /PDB:"C:\Users\Richard\Documents\Visual Studio 2015\Projects\ConsoleApplication1\x64\Debug\ConsoleApplication1.pdb" 
# /PGD:"C:\Users\Richard\Documents\Visual Studio 2015\Projects\ConsoleApplication1\x64\Debug\ConsoleApplication1.pgd" 



ifeq ($(BUILD_TYPE),debug)
  DEFINES = $(DEFINES_BASE) $(DEFINES_DEBUG)
  CFLAGS = $(CFLAGS_BASE) $(CFLAGS_DEBUG)
  LINKFLAGS = $(LINKFLAGS_BASE) $(LINKFLAGS_DEBUG)
else
  DEFINES = $(DEFINES_BASE)
  CFLAGS = $(CFLAGS_BASE) $(CFLAGS_NODEBUG)
  LINKFLAGS = $(LINKFLAGS_BASE) $(LINKFLAGS_NODEBUG)
endif

INCLUDES = -I $(SOURCE_DIR) -I $(subst /,\,../dependencies/cunit/include) -I $(subst /,\,../dependencies/jansson/include)
SOURCES = $(wildcard $(SOURCE_DIR)/*.c)
HEADERS = $(wildcard $(SOURCE_DIR)/*.h) $(wildcard ../dependencies/cunit/include/*.h)  $(wildcard ../dependencies/jansson/include/*.h)

PROGRAM_NAME = janssontest
PROGRAM = $(PROGRAM_NAME).exe

all : $(BUILD_DIR)/dist/$(PROGRAM)

$(BUILD_DIR)/dist/$(PROGRAM): $(SOURCES) $(HEADERS)
	-del $(PROGRAM_NAME).link $(PROGRAM_NAME).def 1>nul 2>nul
	echo "kernel32.lib" "user32.lib" "gdi32.lib" "winspool.lib" "comdlg32.lib" "advapi32.lib"  >> $(PROGRAM_NAME).link
	echo "shell32.lib" "ole32.lib" "oleaut32.lib" "uuid.lib" "odbc32.lib" "odbccp32.lib"       >> $(PROGRAM_NAME).link
	echo $(wildcard ../dependencies/cunit/lib/static/*.lib)                                    >> $(PROGRAM_NAME).link
	echo $(wildcard ../dependencies/jansson/lib/static/*.lib)                                  >> $(PROGRAM_NAME).link
	$(CC) $(CFLAGS) $(DEFINES) $(INCLUDES) $(SOURCES)
	$(LD) $(LINKFLAGS) *.obj @$(PROGRAM_NAME).link -out:$(PROGRAM)
	if not exist ../dist/bin (mkdir $(subst /,\,../dist/bin) 1>nul 2>nul)
	copy $(PROGRAM) $(subst /,\,../dist/bin)

clean::
	-del *.exe *.obj *.pdb *.ilk *.link

