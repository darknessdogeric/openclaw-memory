SKILL_NAME := audiobook
SKILL_TAR  := $(SKILL_NAME)-skill.tar.gz
STAGE      := .build/$(SKILL_NAME)
BACKUP_FMT := $(SKILL_NAME)-backup-$(shell date +%Y%m%d-%H%M%S).tar.gz

VENV   = venv
PYTHON = $(VENV)/bin/python
PIP    = $(VENV)/bin/pip
PYTEST = $(VENV)/bin/pytest

SRC := audiobook.py models.py extractor.py cleaner.py chapters.py \
       tts_piper.py assembler.py

TOP := SKILL.md $(SRC) requirements.txt VERSION

ALL := $(TOP)

# --- Production target -------------------------------------------------------
PROD_SSH_KEY  := ~/.ssh/id_ed25519
PROD_HOST     := ubuntu@poe.omelas.net
PROD_DEST     := $(PROD_HOST):~/.openclaw/workspace-jorge/skills
SSH_OPTS      := -i $(PROD_SSH_KEY) -o StrictHostKeyChecking=accept-new

# Piper model URLs (HuggingFace)
PIPER_BASE_URL := https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0
ES_MODEL       := es/es_ES/sharvard/medium/es_ES-sharvard-medium.onnx
ES_CONFIG      := es/es_ES/sharvard/medium/es_ES-sharvard-medium.onnx.json
EN_MODEL       := en/en_GB/cori/high/en_GB-cori-high.onnx
EN_CONFIG      := en/en_GB/cori/high/en_GB-cori-high.onnx.json

IS_REMOTE = $(if $(findstring :,$(DEST)),1,)

.PHONY: setup setup-models test test-quick clean skill deploy prod help

# --- Local dev ---------------------------------------------------------------

setup:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

setup-models:
	mkdir -p models
	@echo "Downloading piper voice models..."
	@[ -f models/es_ES-sharvard-medium.onnx ] || \
		wget -q --show-progress -O models/es_ES-sharvard-medium.onnx \
			"$(PIPER_BASE_URL)/$(ES_MODEL)"
	@[ -f models/es_ES-sharvard-medium.onnx.json ] || \
		wget -q --show-progress -O models/es_ES-sharvard-medium.onnx.json \
			"$(PIPER_BASE_URL)/$(ES_CONFIG)"
	@[ -f models/en_GB-cori-high.onnx ] || \
		wget -q --show-progress -O models/en_GB-cori-high.onnx \
			"$(PIPER_BASE_URL)/$(EN_MODEL)"
	@[ -f models/en_GB-cori-high.onnx.json ] || \
		wget -q --show-progress -O models/en_GB-cori-high.onnx.json \
			"$(PIPER_BASE_URL)/$(EN_CONFIG)"
	@echo "=> Models ready in models/"

test:
	$(PYTEST) tests/ -v

test-quick:
	$(PYTEST) tests/ -v -x --tb=short

clean:
	rm -rf $(SKILL_TAR) .build $(VENV) __pycache__ .pytest_cache
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -delete

# --- Build -------------------------------------------------------------------

skill: $(SKILL_TAR)

$(SKILL_TAR): $(ALL)
	rm -rf .build
	mkdir -p $(STAGE)
	cp $(TOP) $(STAGE)/
	@echo "$(shell date '+%Y-%m-%d %H:%M:%S %Z') ($(shell cat VERSION | tr -d '\n'))" > $(STAGE)/BUILD_INFO
	tar czf $@ -C .build $(SKILL_NAME)
	rm -rf .build
	@echo "=> $(SKILL_TAR) listo ($(shell du -h $@ | cut -f1))"

# --- Helpers -----------------------------------------------------------------

_require_dest:
	@if [ -z "$(DEST)" ]; then \
		echo "Error: DEST requerido"; \
		echo "  Local:  make deploy DEST=~/.openclaw/agents/<id>/workspace/skills"; \
		echo "  Remoto: make deploy DEST=user@host:/path/to/skills"; \
		echo "  Prod:   make prod"; \
		exit 1; \
	fi

# --- Deploy ------------------------------------------------------------------

deploy: skill _require_dest
	@if [ -n "$(IS_REMOTE)" ]; then \
		HOST=$${DEST%%:*}; DIR=$${DEST#*:}; \
		echo "Deploying to $$HOST:$$DIR/$(SKILL_NAME) ..."; \
		scp $(SSH_OPTS) $(SKILL_TAR) $$HOST:/tmp/$(SKILL_TAR); \
		ssh $(SSH_OPTS) $$HOST "cd $$DIR && tar xzf /tmp/$(SKILL_TAR) && rm /tmp/$(SKILL_TAR)"; \
		echo "Setting up venv and models on server..."; \
		ssh $(SSH_OPTS) $$HOST "cd $$DIR/$(SKILL_NAME) && \
			([ -d venv ] || python3 -m venv venv) && \
			venv/bin/pip install -q -r requirements.txt && \
			mkdir -p models && \
			([ -f models/es_ES-sharvard-medium.onnx ] || \
				wget -q -O models/es_ES-sharvard-medium.onnx '$(PIPER_BASE_URL)/$(ES_MODEL)') && \
			([ -f models/es_ES-sharvard-medium.onnx.json ] || \
				wget -q -O models/es_ES-sharvard-medium.onnx.json '$(PIPER_BASE_URL)/$(ES_CONFIG)') && \
			([ -f models/en_GB-cori-high.onnx ] || \
				wget -q -O models/en_GB-cori-high.onnx '$(PIPER_BASE_URL)/$(EN_MODEL)') && \
			([ -f models/en_GB-cori-high.onnx.json ] || \
				wget -q -O models/en_GB-cori-high.onnx.json '$(PIPER_BASE_URL)/$(EN_CONFIG)')"; \
	else \
		echo "Deploying to $(DEST)/$(SKILL_NAME) ..."; \
		tar xzf $(SKILL_TAR) -C "$(DEST)"; \
		cd "$(DEST)/$(SKILL_NAME)" && \
			([ -d venv ] || python3 -m venv venv) && \
			venv/bin/pip install -q -r requirements.txt; \
	fi
	@echo "=> $(SKILL_NAME) desplegado"

# --- Version bump ------------------------------------------------------------

bump-patch:
	@V=$$(cat VERSION | tr -d '\n'); \
	MAJOR=$$(echo $$V | cut -d. -f1); \
	MINOR=$$(echo $$V | cut -d. -f2); \
	PATCH=$$(echo $$V | cut -d. -f3); \
	NEW="$$MAJOR.$$MINOR.$$((PATCH + 1))"; \
	echo "$$NEW" > VERSION; \
	echo "=> Version: $$V -> $$NEW"

# --- Production shortcut -----------------------------------------------------

prod: bump-patch skill
	@$(MAKE) deploy DEST="$(PROD_DEST)"

# --- Build (alias for test) --------------------------------------------------

build:
	$(PYTEST) tests/ -v

# --- Help --------------------------------------------------------------------

help:
	@echo "Targets:"
	@echo "  make setup              Setup venv + deps"
	@echo "  make setup-models       Download piper voice models"
	@echo "  make test               Run all tests"
	@echo "  make test-quick         Run tests (stop on first failure)"
	@echo "  make skill              Build $(SKILL_TAR)"
	@echo "  make deploy DEST=...    Deploy to destination"
	@echo "  make prod               Deploy to production"
	@echo "  make clean              Clean artifacts"
