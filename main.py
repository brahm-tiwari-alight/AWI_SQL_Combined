#!/usr/bin/env python3
"""
Main entry point for AWI SQL Combined Dataset Search
Demonstrates searching across all 72 datasets without limits
"""

import sys
import os
import json
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.dataset_manager import DatasetManager
from src.search_engine import SearchEngine


def create_sample_datasets(dataset_manager: DatasetManager, count: int = 15):
    """Create sample datasets to demonstrate the functionality"""
    
    # Create sample SQL datasets
    for i in range(1, count//2 + 1):
        sql_content = f"""
-- Sample SQL Dataset {i}
CREATE TABLE dataset_{i} (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    value DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO dataset_{i} (name, value) VALUES 
    ('Sample Record A', {i * 10.5}),
    ('Sample Record B', {i * 15.3}),
    ('Test Data {i}', {i * 7.8});

SELECT * FROM dataset_{i} WHERE value > {i * 5};
"""
        dataset_manager.add_dataset(f"sql_dataset_{i}", sql_content, "sql")
    
    # Create sample JSON datasets
    for i in range(count//2 + 1, count + 1):
        json_content = {
            "dataset_id": f"json_dataset_{i}",
            "metadata": {
                "version": "1.0",
                "created": "2024-01-01",
                "description": f"Sample JSON dataset number {i}",
                "tags": ["sample", "test", f"dataset_{i}"]
            },
            "data": [
                {
                    "id": j,
                    "name": f"Record {j} from dataset {i}",
                    "value": i * j * 2.5,
                    "category": "sample_data",
                    "attributes": {
                        "searchable": True,
                        "priority": "normal" if j % 2 == 0 else "high"
                    }
                }
                for j in range(1, 6)
            ],
            "summary": {
                "total_records": 5,
                "avg_value": i * 7.5,
                "categories": ["sample_data"],
                "searchable_fields": ["name", "category", "attributes"]
            }
        }
        dataset_manager.add_dataset(f"json_dataset_{i}", json_content, "json")


def main():
    """Main function demonstrating the search functionality"""
    print("AWI SQL Combined Dataset Search")
    print("=" * 50)
    
    # Initialize dataset manager and search engine
    dataset_manager = DatasetManager("datasets")
    search_engine = SearchEngine(dataset_manager)
    
    # Check current dataset count
    current_count = dataset_manager.get_dataset_count()
    print(f"Current datasets loaded: {current_count}")
    
    # Create sample datasets if none exist
    if current_count == 0:
        print("No datasets found. Creating sample datasets...")
        create_sample_datasets(dataset_manager, 15)
        current_count = dataset_manager.get_dataset_count()
        print(f"Created {current_count} sample datasets")
    
    print(f"\nDataset Information:")
    info = dataset_manager.get_dataset_info()
    print(f"- Total datasets: {info['total_datasets']}")
    print(f"- Target capacity: {info['target_capacity']} datasets")
    print(f"- Capacity used: {(info['total_datasets']/info['target_capacity']*100):.1f}%")
    
    # Get search statistics
    stats = search_engine.get_search_statistics()
    print(f"\nSearch Engine Statistics:")
    print(f"- SQL datasets: {stats['sql_datasets']}")
    print(f"- JSON datasets: {stats['json_datasets']}")
    print(f"- Unlimited search: {stats['search_unlimited']}")
    print(f"- Supports regex: {stats['supports_regex']}")
    
    # Demonstrate search functionality
    print(f"\n" + "=" * 50)
    print("SEARCH DEMONSTRATIONS")
    print("=" * 50)
    
    # Search 1: Simple search across all datasets (no limit)
    print("\n1. Searching for 'sample' across ALL datasets (no limit):")
    results = search_engine.search("sample")
    print(f"   - Query: '{results['query']}'")
    print(f"   - Datasets searched: {results['datasets_searched']}")
    print(f"   - Total results: {results['total_results']}")
    print(f"   - Results returned: {results['results_returned']}")
    print(f"   - Limited: {results['limited']}")
    
    # Search 2: SQL-only search
    print(f"\n2. Searching for 'SELECT' in SQL datasets only:")
    sql_results = search_engine.search("SELECT", search_type="sql")
    print(f"   - Total results: {sql_results['total_results']}")
    print(f"   - Results returned: {sql_results['results_returned']}")
    
    # Search 3: JSON-only search with case sensitivity
    print(f"\n3. Case-sensitive search for 'Record' in JSON datasets:")
    json_results = search_engine.search("Record", search_type="json", case_sensitive=True)
    print(f"   - Total results: {json_results['total_results']}")
    print(f"   - Results returned: {json_results['results_returned']}")
    
    # Search 4: Demonstrate that we can search ALL datasets without limit
    print(f"\n4. Comprehensive search across all {current_count} datasets:")
    comprehensive_results = search_engine.search("data")
    print(f"   - Datasets searched: {comprehensive_results['datasets_searched']}")
    print(f"   - Total matches found: {comprehensive_results['total_results']}")
    print(f"   - No artificial limits applied: {not comprehensive_results['limited']}")
    
    # Show sample results
    if comprehensive_results['results']:
        print(f"\n   Sample results:")
        for i, result in enumerate(comprehensive_results['results'][:3]):
            print(f"     {i+1}. Dataset: {result['dataset']}, Type: {result['type']}")
    
    print(f"\n" + "=" * 50)
    print("KEY FEATURES IMPLEMENTED:")
    print("- ✓ Searches across ALL datasets (no 10-item limit)")
    print("- ✓ Supports up to 72 datasets as required") 
    print("- ✓ No default pagination/limits")
    print("- ✓ Handles both SQL and JSON datasets")
    print("- ✓ Advanced search options (regex, case sensitivity)")
    print("- ✓ Comprehensive result metadata")
    print("=" * 50)
    
    # Interactive search mode
    print(f"\nEntering interactive search mode...")
    print("Enter search queries (or 'quit' to exit):")
    
    while True:
        try:
            query = input("\nSearch query: ").strip()
            if query.lower() in ['quit', 'exit', 'q']:
                break
            
            if query:
                results = search_engine.search(query)
                print(f"Found {results['total_results']} results across {results['datasets_searched']} datasets")
                
                if results['results']:
                    print("Top results:")
                    for i, result in enumerate(results['results'][:5]):
                        print(f"  {i+1}. {result['dataset']} ({result['type']})")
        
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()