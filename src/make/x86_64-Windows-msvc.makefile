
CC = cl
LD = link

CFLAGS_BASE = -c -W3 -Gs -nologo
CFLAGS_DEBUG = -Zi -Od
LINKFLAGS_BASE = -nod -nologo
LINKFLAGS_DEBUG = -debug
DEFINES_BASE = -DbuildLabel=$(buildLabel) -D_MT -D_CRT_SECURE_NO_WARNINGS -D_CRT_SECURE_NO_DEPRECATE -D_CRT_NONSTDC_NO_DEPRECATE -D_CRT_NON_CONFORMING_SWPRINTFS
DEFINES_DEBUG = -DDEBUG

ifeq ($(BUILD_TYPE),debug)
  CFLAGS = $(CFLAGS_BASE) $(CFLAGS_DEBUG)
  LINKFLAGS = $(LINKFLAGS_BASE) $(LINKFLAGS_DEBUG)
  DEFINES = $(DEFINES_BASE) $(DEFINES_DEBUG)
else
  CFLAGS = $(CFLAGS_BASE)
  LINKFLAGS = $(LINKFLAGS_BASE)
  DEFINES = $(DEFINES_BASE)
endif

INCLUDES = -I $(SOURCE_DIR) -I $(subst /,\,$(BUILD_DIR)/dependances/CUnit/headers/CUnit) -I $(subst /,\,$(BUILD_DIR)/dependances/jansson/headers)

SOURCES = $(wildcard $(SOURCE_DIR)/c/*.c)

HEADERS = $(wildcard $(SOURCE_DIR)/headers/*.h) $(wildcard $(BUILD_DIR)/dependances/CUnit/headers/CUnit/*.h)  $(wildcard $(BUILD_DIR)/dependances/jansson/headers/*.h)

PROGRAM_NAME = jansson-test
PROGRAM = $(PROGRAM_NAME).exe

all : $(BUILD_DIR)/dist/$(PROGRAM)

$(BUILD_DIR)/dist/$(PROGRAM): $(SOURCES) $(HEADERS)
	echo $(SOURCES)
	echo $(SOURCE_DIR)/c/*.c
	del $(PROGRAM_NAME).link $(PROGRAM_NAME).def 1>nul 2>nul
	echo msvcrt.lib oldnames.lib kernel32.lib user32.lib advapi32.lib dbghelp.lib >> $(PROGRAM_NAME).link
	echo $(wildcard $(BUILD_DIR)/dependances/CUnit/libs/static/*.lib) >> $(PROGRAM_NAME).link
	echo $(wildcard $(BUILD_DIR)/dependances/jansson/libs/static/*.lib) >> $(PROGRAM_NAME).link
	$(CC) $(CFLAGS) $(DEFINES) $(INCLUDES) $(SOURCES)
	$(LD) $(LINKFLAGS) *.obj @$(PROGRAM_NAME).link -out:$(PROGRAM)
	mkdir $(subst /,\,$(BUILD_DIR)/dist/bin)
	copy $(PROGRAM) $(subst /,\,$(BUILD_DIR)/dist/bin)

clean::
	-del *.exe *.obj *.pdb *.ilk *.link

