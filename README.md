# AWI SQL Combined Dataset Search

A comprehensive dataset management and search system designed to handle up to 72 datasets with **unlimited search capabilities** - no default pagination limits.

## Key Features

- 🚀 **Unlimited Search**: Search across ALL datasets without default limits (addresses the 10-item limitation)
- 📊 **Multi-format Support**: Handles both SQL (.sql) and JSON (.json) datasets
- 🔍 **Advanced Search**: Regex support, case sensitivity options, type filtering
- 📈 **Scalable**: Designed for up to 72 datasets as required
- 🎯 **Comprehensive Results**: Detailed search metadata and relevance scoring
- ⚡ **Fast Performance**: Efficient search across large dataset collections

## Problem Solved

This repository addresses the specific requirement: *"when it searches the repo it should search for all 72 datasets and not limit itself to 10."*

### Key Improvements:
- ✅ Removes default pagination limits
- ✅ Searches ALL available datasets by default
- ✅ Only applies limits when explicitly requested
- ✅ Handles up to 72 datasets efficiently
- ✅ Provides comprehensive search results

## Quick Start

```bash
# Clone and run
git clone <repository-url>
cd AWI_SQL_Combined
python main.py
```

## Usage

### Basic Search (No Limits)
```python
from src.dataset_manager import DatasetManager
from src.search_engine import SearchEngine

# Initialize
manager = DatasetManager("datasets")
engine = SearchEngine(manager)

# Search ALL datasets (no limit)
results = engine.search("your_search_term")
print(f"Found {results['total_results']} results across {results['datasets_searched']} datasets")
```

### Advanced Search Options
```python
# Search with specific options
results = engine.search(
    query="SELECT",
    search_type="sql",        # "all", "sql", or "json"
    case_sensitive=True,      # Case sensitive search
    use_regex=True,          # Enable regex patterns
    limit=None               # No limit (default)
)
```

### Adding Datasets
```python
# Add JSON dataset
json_data = {"key": "value", "data": [...]}
manager.add_dataset("my_dataset", json_data, "json")

# Add SQL dataset
sql_content = "CREATE TABLE example (id INT, name VARCHAR(50));"
manager.add_dataset("my_sql", sql_content, "sql")
```

## Architecture

```
AWI_SQL_Combined/
├── src/
│   ├── dataset_manager.py    # Dataset loading and management
│   └── search_engine.py      # Advanced search functionality
├── datasets/                 # Dataset storage directory
├── tests/                    # Comprehensive test suite
├── main.py                   # Demo and interactive usage
└── config.py                 # Configuration settings
```

## Search Capabilities

### No Default Limits
- **Default behavior**: Search ALL datasets without limits
- **Explicit limits**: Only applied when specifically requested
- **Scalability**: Handles all 72 datasets efficiently

### Search Types
- **All datasets**: Search across both SQL and JSON datasets
- **SQL only**: Search within SQL scripts and queries
- **JSON only**: Search within JSON data structures

### Advanced Features
- **Regex support**: Use regular expressions for complex patterns
- **Case sensitivity**: Control case-sensitive matching
- **Relevance scoring**: Results sorted by relevance
- **Detailed metadata**: Comprehensive result information

## API Reference

### DatasetManager
```python
manager = DatasetManager("datasets")

# Load existing datasets
manager._load_datasets()

# Add new dataset
manager.add_dataset(name, content, dataset_type)

# Search all datasets (no limits)
manager.search_all_datasets(query, limit=None)

# Get dataset statistics
manager.get_dataset_info()
```

### SearchEngine
```python
engine = SearchEngine(dataset_manager)

# Main search method (unlimited by default)
engine.search(query, search_type="all", case_sensitive=False, 
              use_regex=False, limit=None)

# Get search statistics
engine.get_search_statistics()
```

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
python -m unittest discover tests/

# Run specific test file
python -m unittest tests.test_search_engine

# Test with 72 datasets
python tests/test_search_engine.py
```

### Test Coverage

- ✅ Unlimited search functionality
- ✅ Search across all 72 datasets
- ✅ Advanced search options
- ✅ Dataset management
- ✅ File persistence
- ✅ Error handling
- ✅ Performance with large datasets

## Configuration

Configure system behavior in `config.py`:

```python
DATASET_CONFIG = {
    "MAX_DATASETS": 72,
    "SEARCH_CONFIG": {
        "DEFAULT_LIMIT": None,        # No default limit
        "UNLIMITED_SEARCH": True,     # Enable unlimited search
    }
}
```

## Performance

- **Dataset Capacity**: Up to 72 datasets
- **Search Speed**: Optimized for large dataset collections
- **Memory Usage**: Efficient dataset loading and caching
- **Result Processing**: Fast relevance scoring and sorting

## Examples

### Example 1: Search All Datasets
```python
# This searches ALL datasets without any limits
results = engine.search("customer_data")
print(f"Searched {results['datasets_searched']} datasets")
print(f"Found {results['total_results']} total matches")
print(f"No limits applied: {not results['limited']}")
```

### Example 2: Demonstrate Scalability
```python
# Add datasets up to capacity
for i in range(72):
    data = {"id": i, "content": f"dataset_{i}"}
    manager.add_dataset(f"dataset_{i}", data, "json")

# Search across all 72 datasets
results = engine.search("dataset")
print(f"Successfully searched all {results['datasets_searched']} datasets")
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

[Add your license information here]

---

**Key Achievement**: This implementation ensures that searches are performed across ALL available datasets (up to 72) without artificial limits, directly addressing the requirement to "search for all 72 datasets and not limit itself to 10."