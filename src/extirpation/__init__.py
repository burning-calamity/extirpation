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
from .easy import ensure_online_modules, quick_transform
from .key_autoguesser import (
    KeyGuess,
    LanguageScore,
    autoguess_keys,
    list_supported_autoguessers,
    load_language_wordsets,
    score_plaintext_language_cohesion,
)

__version__ = "2.6.3"

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
    "ensure_online_modules",
    "quick_transform",
    "KeyGuess",
    "LanguageScore",
    "autoguess_keys",
    "list_supported_autoguessers",
    "load_language_wordsets",
    "score_plaintext_language_cohesion",
    "__version__",
]
