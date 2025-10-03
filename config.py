"""
Configuration for AWI SQL Combined Dataset Search
"""

# Dataset configuration
DATASET_CONFIG = {
    # Maximum number of datasets the system is designed to handle
    "MAX_DATASETS": 72,
    
    # Default dataset directory
    "DATASETS_DIR": "datasets",
    
    # Search configuration - NO DEFAULT LIMITS
    "SEARCH_CONFIG": {
        # No default limit - search all datasets
        "DEFAULT_LIMIT": None,
        
        # Maximum limit that can be applied (safety measure)
        "MAX_LIMIT": 10000,
        
        # Enable unlimited search by default
        "UNLIMITED_SEARCH": True,
        
        # Search options
        "CASE_SENSITIVE_DEFAULT": False,
        "REGEX_ENABLED": True,
        "SEARCH_TYPES": ["all", "sql", "json"]
    },
    
    # Performance settings
    "PERFORMANCE": {
        # Enable result caching (future enhancement)
        "ENABLE_CACHING": False,
        
        # Maximum result size before warnings
        "LARGE_RESULT_THRESHOLD": 1000
    },
    
    # File format support
    "SUPPORTED_FORMATS": {
        "json": {
            "extensions": [".json"],
            "description": "JSON dataset files"
        },
        "sql": {
            "extensions": [".sql"],
            "description": "SQL script files"
        }
    }
}

# Validation rules
VALIDATION_RULES = {
    "dataset_name": {
        "max_length": 100,
        "allowed_chars": "alphanumeric_underscore_dash"
    },
    "search_query": {
        "max_length": 1000,
        "min_length": 0  # Allow empty queries
    }
}

# Logging configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "log_search_queries": True,
    "log_performance_metrics": True
}