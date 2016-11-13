#
# Name:          windows_amd64.makefile
#
# Description: Windows makefile for the notifier program
#
# <N_OCO_COPYRIGHT> 
# Licensed Materials - Property of IBM 
# 04L1830, 5639-B43
# (C) Copyright IBM Corp. 2010,2015
#
# US Government Users Restricted Rights - Use, duplication or       
# disclosure restricted by GSA ADP Schedule Contract with   
# IBM Corp.    
# <NOC_COPYRIGHT>
#

CC = cl
LD = link

MQM_INC = $(MQ_INST_DIR)\tools\c\include
MQM_LIB = $(MQ_INST_DIR)\tools\lib
MQM_EXITS = $(MQ_DATA_DIR)\exits64

CFLAGS_BASE = -c -W3 -Gs -nologo
CFLAGS_DEBUG = -Zi -Od 
LINKFLAGS_BASE = -nod -nologo
LINKFLAGS_DEBUG = -debug
DEFINES_BASE = -DbuildLabel=$(buildLabel) -DMQ_LIB_DIR=lib64 -D_MT -D_DLL -D_CRT_SECURE_NO_WARNINGS -D_CRT_SECURE_NO_DEPRECATE -D_CRT_NONSTDC_NO_DEPRECATE -D_CRT_NON_CONFORMING_SWPRINTFS -DHAVE_CONFIG_H
DEFINES_DEBUG = -DCLOUD_DEBUG

ifeq ($(BUILD_TYPE),debug)
  CFLAGS = $(CFLAGS_BASE) $(CFLAGS_DEBUG)
  LINKFLAGS = $(LINKFLAGS_BASE) $(LINKFLAGS_DEBUG)
  DEFINES = $(DEFINES_BASE) $(DEFINES_DEBUG)
else
  CFLAGS = $(CFLAGS_BASE)
  LINKFLAGS = $(LINKFLAGS_BASE)
  DEFINES = $(DEFINES_BASE)
endif   

INCLUDES = -I $(SOURCE_DIR) -I $(UTILS_DIR) -I $(UTILS_DIR)/windows_amd64 -I $(JANSSON_DIR)/windows_amd64 -I $(JANSSON_DIR) -I "$(MQM_INC)" -I $(CURL_DIR)/include -I $(CURL_DIR)/include/windows

SOURCES = $(SOURCE_DIR)/Notifier.c \
          $(UTILS_DIR)/Logger.c $(UTILS_DIR)/Utils.c $(UTILS_DIR)/CommonServices.c $(UTILS_DIR)/FileLock.c $(UTILS_DIR)/JsonUtils.c \
          $(UTILS_DIR)/Users.c $(UTILS_DIR)/Account.c $(UTILS_DIR)/Exception.c $(UTILS_DIR)/windows_amd64/Exception2.c $(wildcard $(JANSSON_DIR)/*.c)

HEADERS = $(UTILS_DIR)/Logger.h $(UTILS_DIR)/Utils.h $(UTILS_DIR)/CommonServices.h $(UTILS_DIR)/FileLock.h $(UTILS_DIR)/JsonUtils.h \
          $(UTILS_DIR)/Users.h $(UTILS_DIR)/Account.h $(UTILS_DIR)/Exception.h $(UTILS_DIR)/windows_amd64/Exception2.h \
          $(JANSSON_DIR)/linux_amd64/jansson_config.h $(wildcard $(JANSSON_DIR)/*.h)

PROGRAM_NAME = notifier
PROGRAM = $(PROGRAM_NAME).exe

all : $(PROGRAM)

$(PROGRAM): $(SOURCES) $(HEADERS)
	del $(LIBRARY_NAME).link $(LIBRARY_NAME).def
	echo msvcrt.lib oldnames.lib kernel32.lib user32.lib advapi32.lib dbghelp.lib >> $(PROGRAM_NAME).link
	echo $(CURL_DIR)/windows_ia64/libcurl.lib                                     >> $(PROGRAM_NAME).link
	$(CC) $(CFLAGS) $(DEFINES) $(INCLUDES) $(SOURCES)
	lib -nologo -out:$(PROGRAM_NAME).exe
	$(LD) $(LINKFLAGS) *.obj @$(PROGRAM_NAME).link -out:$(PROGRAM)
	copy $(PROGRAM) $(subst /,\,$(DIST_DIR))
	copy $(PROGRAM) "$(MQM_EXITS)"	

clean::
	-del *.exe *.obj *.pdb *.ilk *.link

