"""Test startup module: configure global test settings executed at import time.

Unittest discovery will import this module (it matches test_*.py), so placing
global test setup here lets us configure logging to reduce noisy INFO logs.
"""
import logging

# By default tests should be quiet: only warnings and errors are shown.
logging.basicConfig(level=logging.WARNING)
