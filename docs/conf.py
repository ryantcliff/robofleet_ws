from __future__ import annotations

import os
from datetime import datetime

project = "RoboFleet"
author = "University at Buffalo RoboFleet Team"
copyright = f"{datetime.now().year}, University at Buffalo RoboFleet Team"
release = "2026-2027"

extensions = ["sphinx_rtd_theme"]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_title = "RoboFleet Documentation"

html_theme_options = {
    "collapse_navigation": False,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}

html_context = {
    "display_github": True,
    "github_user": "ryantcliff",
    "github_repo": "roboflock_ws",
    "github_version": os.environ.get("READTHEDOCS_GIT_IDENTIFIER", "robofleet-documentation"),
    "conf_py_path": "/docs/",
}

rst_prolog = """
.. role:: inherited
.. role:: ready
.. role:: planned
"""
