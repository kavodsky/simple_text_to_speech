.PHONY: help install sync run clean clean-cache clean-all test format lint check models info

# Default target
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "SimpleTTS - Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install uv if not already installed
	@command -v uv >/dev/null 2>&1 || { echo "Installing uv..."; curl -LsSf https://astral.sh/uv/install.sh | sh; }
	@echo "uv is installed ✓"

sync: ## Install/sync all dependencies
	uv sync

run: ## Run the Streamlit application
	uv run streamlit run main.py

dev: ## Run the app in development mode with auto-reload
	uv run streamlit run main.py --server.runOnSave true

clean: ## Clean output files and cache
	rm -rf output/*.wav
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

clean-cache: ## Clean uv cache
	uv cache clean

clean-venv: ## Remove virtual environment
	rm -rf .venv

clean-all: clean clean-venv ## Clean everything (output, cache, venv)
	@echo "All cleaned ✓"

add: ## Add a new dependency (usage: make add PACKAGE=package-name)
	@if [ -z "$(PACKAGE)" ]; then \
		echo "Error: Please specify PACKAGE=package-name"; \
		exit 1; \
	fi
	uv add $(PACKAGE)

add-dev: ## Add a new dev dependency (usage: make add-dev PACKAGE=package-name)
	@if [ -z "$(PACKAGE)" ]; then \
		echo "Error: Please specify PACKAGE=package-name"; \
		exit 1; \
	fi
	uv add --dev $(PACKAGE)

update: ## Update all dependencies
	uv sync --upgrade

lock: ## Update the lock file without installing
	uv lock

python: ## Open Python REPL with project dependencies
	uv run python

info: ## Show project information
	@echo "Project: SimpleTTS"
	@echo "Python version: $(shell uv run python --version)"
	@echo "Dependencies: $(shell uv pip list | wc -l | xargs) packages"
	@echo ""
	@echo "Key packages:"
	@uv run python -c "import streamlit; import torch; import numpy; import pandas; print(f'  streamlit: {streamlit.__version__}'); print(f'  torch: {torch.__version__}'); print(f'  numpy: {numpy.__version__}'); print(f'  pandas: {pandas.__version__}')"

check-deps: ## Check if all dependencies are compatible
	@echo "Checking numpy and pandas compatibility..."
	@uv run python -c "import numpy; import pandas; print('✓ All dependencies are compatible')"

models: ## List available models
	@echo "Available models:"
	@cat models.json | uv run python -c "import sys, json; data=json.load(sys.stdin); [print(f\"  - {v['name']}: {v['model']}\") for v in data['voices']]"

shell: ## Open a shell with the virtual environment activated
	@echo "Opening shell with virtual environment..."
	@bash -c "source .venv/bin/activate && exec bash"

