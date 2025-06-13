# File name ends in plugin to exclude from git repository e.g. omzet_service_plugin.py
from decimal import Decimal

# Called by plugin loader
def get_omzet():
    # Expected to be in Decimal object
    return Decimal("1000.5")