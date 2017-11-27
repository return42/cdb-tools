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
	@echo  '  docs     - build documentation'
	@echo  '  clean    - remove most generated files'
	@echo  '  cdbtools - bootstrap & build CDB-Tools'
	@echo  ''
	@$(MAKE) -s -f utils/makefile.sphinx docs-help

PHONY += docs
docs:  sphinx-doc slides
	$(call cmd,sphinx,html,docs,docs)

PHONY += slides
slides: cdb-slide
	cd $(DOCS_DIST)/slides; python -m zipfile -c cdb_comp.zip cdb_comp

PHONY += cdb-slide
cdb-slide:  sphinx-doc
	$(call cmd,sphinx,html,$(SLIDES)/cdb_comp,$(SLIDES)/cdb_comp,slides/cdb_comp)

PHONY += clean
clean: docs-clean pyclean
	$(call cmd,cdbtools_clean)
	$(call cmd,common_clean)

# FIXME: works only on Windows ...
PHONY += cdbtools
cdbtools:
	winShortcuts\upkeep.bat

.PHONY: $(PHONY)
