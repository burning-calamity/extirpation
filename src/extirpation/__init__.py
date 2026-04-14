"""extirpation package."""

from .online_loader import (
    LoadReport,
    ModuleFilter,
    ModuleLoadError,
    describe_loaded_modules,
    invoke_module_function,
    list_online_modules,
    load_online_modules,
    load_online_modules_with_report,
    module_catalog_stats,
    search_catalog,
    validate_module_contracts,
)

__version__ = "1.7.0"

__all__ = [
    "load_online_modules",
    "load_online_modules_with_report",
    "list_online_modules",
    "describe_loaded_modules",
    "module_catalog_stats",
    "search_catalog",
    "validate_module_contracts",
    "invoke_module_function",
    "ModuleLoadError",
    "LoadReport",
    "ModuleFilter",
    "__version__",
]
