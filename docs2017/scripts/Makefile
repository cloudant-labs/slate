# Makefile for Cloudant documentation
#

# You can set these variables from the command line.
BUILDDIR      = ../build
MAINSRCDIR    = ../src
CONFIGDIR     = ../tools/
TOOLDIR       = $(HOME)/git/github.ibm.com/Grant-Gayed
BUILDTOOLDIR  = $(TOOLDIR)/marked-it-cli
BUILDTOOL     = $(BUILDTOOLDIR)/bin/marked-it-cli
WEBCONTENTDIR = /var/www/html

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  clean      to clean the build environment"
	@echo "  html       to make all standalone (local) files, in the 'BUILDDIR' directory"
	@echo "  debughtml  to do a verbose build of all standalone (local) files"
	@echo "  publish    to copy the locally-built HTML content to a local web server, which delivers files from 'WEBCONTENTDIR'."
	@echo "The defined variables are:"
	@echo "  BUILDDIR      = $(BUILDDIR)"
	@echo "  BUILDTOOL     = $(BUILDTOOL)"
	@echo "  TOOLDIR       = $(TOOLDIR)"
	@echo "  WEBCONTENTDIR = $(WEBCONTENTDIR)"

.PHONY: clean
clean:
	rm -rf $(BUILDDIR)
	@rm -f linkcheck.txt

.PHONY: html
html:
	make clean
	mkdir $(BUILDDIR)
	node $(BUILDTOOL) $(MAINSRCDIR) --output=$(BUILDDIR) --extension-file=$(CONFIGDIR)/headerFooterExt.js --conref-file=$(CONFIGDIR)/cloudoeconrefs.yml --toc-xml

.PHONY: pdf
pdf:
	make clean
	mkdir $(BUILDDIR)
	node $(BUILDTOOL) $(MAINSRCDIR) --output=$(BUILDDIR) --extension-file=$(CONFIGDIR)/headerFooterExt.js --conref-file=$(CONFIGDIR)/cloudoeconrefs.yml --toc-xml --gen-pdf --verbose

.PHONY: debughtml
debughtml:
	make clean
	mkdir $(BUILDDIR)
	node $(BUILDTOOL) $(MAINSRCDIR) --output=$(BUILDDIR) --extension-file=$(CONFIGDIR)/headerFooterExt.js --conref-file=$(CONFIGDIR)/cloudoeconrefs.yml --toc-xml --verbose

.PHONY: publish
publish:
	rm -rf $(WEBCONTENTDIR)/*
	cp -R $(BUILDDIR) $(WEBCONTENTDIR)/docs

.PHONY: linkcheck
linkcheck:
	@rm -f linkcheck.txt
	wget --spider -r -nd -nv -H -l 10 -D localhost -o linkcheck.txt http://localhost/docs/ 2>/dev/null; true

