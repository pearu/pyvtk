# Makefile for installing Python package under Python 1.x.
# Use GNU make for making.
# $Revision: 1.1 $
# $Date: 2001/05/20 12:51:29 $
# Pearu Peterson <pearu@ioc.ee>

PYTHON = python
PREFIX=$(shell $(PYTHON) -c "import sys;print sys.prefix")
VERSION=$(shell $(PYTHON) -c "import sys;print sys.version[:3]")

PACKAGE = pyvtk
LIBDIR=$(shell $(PYTHON) -c "import sys;print{'1':'lib152','2':'lib'}[sys.version[0]]")

INSTALLDIRECTORY = $(PREFIX)/lib/python$(VERSION)/site-packages/$(PACKAGE)
INSTALLDIR = install -d
INSTALLEXEC = install -m 755
INSTALLDATA = install -m 644

.PHONY: install
all:
	@echo "Use 'make install' to install $(PACKAGE) (in $(LIBDIR)) to" $(INSTALLDIRECTORY)
install:
	rm -f $(INSTALLDIRECTORY)/*.pyc $(INSTALLDIRECTORY)/*.pyo
	$(INSTALLDIR) $(INSTALLDIRECTORY)
	$(INSTALLDATA) $(LIBDIR)/*.py $(INSTALLDIRECTORY)
	cd $(INSTALLDIRECTORY) && echo "$(PACKAGE)" > ../$(PACKAGE).pth
	@echo "***********"
	@echo "$(PACKAGE) is installed succesfully to" $(INSTALLDIRECTORY)
