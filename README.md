SimpleTTS
===========

The application is built to convert text into audio format. It uses Streamlit and Coqui TTS libraries.

## Setup

This project uses [uv](https://github.com/astral-sh/uv) for fast and reliable dependency management.

### Install uv

If you don't have uv installed, install it with:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Install Dependencies

```bash
# Install all dependencies (creates .venv and installs packages)
uv sync
```

This will create a virtual environment in `.venv` and install all required packages with compatible versions (including numpy 1.24.4 which fixes binary incompatibility issues with pandas).

## Run

Before running the application, please download the ML models.

### Quick Start with Makefile

The easiest way to work with this project is using the provided Makefile:

```bash
# See all available commands
make help

# Install dependencies
make sync

# Run the application
make run

# Run in development mode (with auto-reload)
make dev
```

### Start the Application Manually

```bash
# Activate the virtual environment and run streamlit
uv run streamlit run main.py
```

Or manually activate the environment:

```bash
# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate   # On Windows

# Run the application
streamlit run main.py
```

## Makefile Commands

Common tasks available through the Makefile:

```bash
make help          # Show all available commands
make sync          # Install/sync dependencies
make run           # Run the application
make dev           # Run with auto-reload
make clean         # Clean output files and cache
make clean-all     # Clean everything including venv
make add PACKAGE=name       # Add a new dependency
make add-dev PACKAGE=name   # Add a dev dependency
make update        # Update all dependencies
make info          # Show project information
make check-deps    # Check dependency compatibility
make models        # List available voice models
```

## Adding New Dependencies

Using the Makefile:
```bash
make add PACKAGE=package-name
make add-dev PACKAGE=dev-package-name
```

Or directly with uv:
```bash
uv add package-name
uv add --dev dev-package-name
```

## Notes

- The project requires Python 3.11+
- Dependencies are locked in `uv.lock` for reproducible builds
- The `pyproject.toml` file contains all project configuration
