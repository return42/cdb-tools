# -*- coding: utf-8; mode: makefile-gmake -*-

include utils/makefile.include
include utils/makefile.python
include utils/makefile.sphinx

GIT_URL   = https://github.com/return42/cdb-tools.git
SLIDES    = docs/slides

quiet_cmd_cdbtools_clean = CLEAN     cdbtools-clean
      cmd_cdbtools_clean = rm -rf ./.cache ./dist ./build ./py27 ./win_bin/ConEmu

all: clean cdbtools docs

PHONY += help
help:
	@echo  '  docs      - build documentation'
	@echo  '  docs-live - autobuild HTML documentation while editing'
	@echo  '  slides    - build reveal.js slide presentation / use e.g.'
	@echo  '              cdb-slide-live to autobuild a presentation'
	@echo  '  clean     - remove most generated files'
	@echo  '  cdbtools  - bootstrap & build CDB-Tools'
	@echo  ''
	@$(MAKE) -s -f utils/makefile.sphinx docs-help

PHONY += docs
docs:  sphinx-doc slides
	$(call cmd,sphinx,html,docs,docs)

PHONY += doc-live
docs-live: sphinx-live
	$(call cmd,sphinx_autobuild,html,docs,docs)

PHONY += slides
slides: cdb-slide
	cd $(DOCS_DIST)/slides; python -m zipfile -c cdb_comp.zip cdb_comp

PHONY += cdb-slide
cdb-slide:  sphinx-doc
	$(call cmd,sphinx,html,$(SLIDES)/cdb_comp,$(SLIDES)/cdb_comp,slides/cdb_comp)

PHONY += cdb-slide-live
cdb-slide-live: sphinx-live
	$(call cmd,sphinx_autobuild,html,$(SLIDES)/cdb_comp,$(SLIDES)/cdb_comp,slides/cdb_comp)

PHONY += clean
clean: docs-clean pyclean
	$(call cmd,cdbtools_clean)
	$(call cmd,common_clean)

purge:  clean
	git clean -xfd
	git gc --aggressive --prune=all


# FIXME: works only on Windows ...
PHONY += cdbtools
cdbtools:
	winShortcuts\upkeep.bat

PHONY += bootstrap download dist
bootstrap:
	winShortcuts\upkeep.bat bootstrap
download:
	winShortcuts\upkeep.bat download
dist:
	winShortcuts\upkeep.bat dist

.PHONY: $(PHONY)
