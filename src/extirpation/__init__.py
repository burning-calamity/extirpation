"""extirpation package."""

from .online_loader import (
    LoadReport,
    ModuleFilter,
    ModuleLoadError,
    describe_loaded_modules,
    clear_online_loader_cache,
    invoke_module_function,
    list_online_modules,
    list_online_modules_cached,
    load_online_modules,
    load_online_modules_with_report,
    load_online_modules_with_report_cached,
    module_catalog_stats,
    search_catalog,
    validate_module_contracts,
)
from .setup import SetupResult, populate_online_directory, setup

__version__ = "2.6.1"

__all__ = [
    "load_online_modules",
    "load_online_modules_with_report",
    "load_online_modules_with_report_cached",
    "clear_online_loader_cache",
    "list_online_modules",
    "list_online_modules_cached",
    "describe_loaded_modules",
    "module_catalog_stats",
    "search_catalog",
    "validate_module_contracts",
    "populate_online_directory",
    "setup",
    "SetupResult",
    "invoke_module_function",
    "ModuleLoadError",
    "LoadReport",
    "ModuleFilter",
    "__version__",
]
