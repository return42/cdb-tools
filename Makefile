# -*- coding: utf-8; mode: makefile-gmake -*-

include utils/makefile.include
include utils/makefile.python
include utils/makefile.sphinx

GIT_URL   = https://github.com/return42/cdb-tools.git
SLIDES    = docs/slides

all: clean docs

PHONY += help
help:
	@echo  '  docs   - build documentation'
	@echo  '  clean  - remove most generated files'
	@echo  ''
	@$(MAKE) -s -f utils/makefile.sphinx docs-help

PHONY += docs
docs:  sphinx-doc slides
	$(call cmd,sphinx,html,docs,docs)

PHONY += slides
slides: cdb-slide
	cd $(DOCS_DIST)/slides; zip -r cdb_comp.zip cdb_comp

PHONY += cdb-slide
cdb-slide:  sphinx-doc
	$(call cmd,sphinx,html,$(SLIDES)/cdb_comp,$(SLIDES)/cdb_comp,slides/cdb_comp)

PHONY += clean
clean: pyclean docs-clean
	$(call cmd,common_clean)

.PHONY: $(PHONY)
