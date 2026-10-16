# RoboFleet Read the Docs source

This directory is the Sphinx source for the 2026–2027 RoboFleet documentation.

## Local preview

```bash
python3 -m venv .venv-docs
source .venv-docs/bin/activate
pip install -r docs/requirements.txt
sphinx-build -b html docs docs/_build/html
python3 -m http.server -d docs/_build/html 8000
```

Open http://localhost:8000.

## Read the Docs

The repository root contains `.readthedocs.yaml`. Import the GitHub repository
into Read the Docs once; afterward GitHub webhook builds can update the site
automatically on pushes to the configured branch/version.
