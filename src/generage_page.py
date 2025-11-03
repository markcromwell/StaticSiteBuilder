
"""
Backward-compatible shim: expose generate_page(from_path, template_path, dest_path)
by delegating to the canonical `generate_page` module if present. This lets
other code import from `generage_page` (typo) or from `generate_page` and
still work regardless of which filename exists on disk.
"""

from importlib import import_module
import os

try:
    # Prefer the canonical module
    mod = import_module('generate_page')
except Exception:
    # Fallback to a local module if the canonical one isn't importable
    mod = import_module('generage_page_alt')

# Export generate_page from the resolved module
generate_page = getattr(mod, 'generate_page')
