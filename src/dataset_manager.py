"""
Dataset Manager for AWI SQL Combined Repository
Handles all 72 datasets without pagination limits
"""

import os
import json
import sqlite3
import glob
from typing import List, Dict, Any, Optional
from pathlib import Path


class DatasetManager:
    """Manages all datasets and provides search functionality across all of them"""
    
    def __init__(self, datasets_dir: str = "datasets"):
        self.datasets_dir = Path(datasets_dir)
        self.datasets_dir.mkdir(exist_ok=True)
        self.datasets = {}
        self._load_datasets()
    
    def _load_datasets(self):
        """Load all datasets from the datasets directory"""
        dataset_files = glob.glob(str(self.datasets_dir / "*.json"))
        sql_files = glob.glob(str(self.datasets_dir / "*.sql"))
        
        # Load JSON datasets
        for file_path in dataset_files:
            dataset_name = Path(file_path).stem
            try:
                with open(file_path, 'r') as f:
                    self.datasets[dataset_name] = json.load(f)
            except Exception as e:
                print(f"Error loading dataset {dataset_name}: {e}")
        
        # Load SQL datasets
        for file_path in sql_files:
            dataset_name = Path(file_path).stem
            try:
                with open(file_path, 'r') as f:
                    self.datasets[dataset_name] = {"sql_content": f.read(), "type": "sql"}
            except Exception as e:
                print(f"Error loading SQL dataset {dataset_name}: {e}")
    
    def search_all_datasets(self, query: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Search across ALL datasets without default pagination limits
        Args:
            query: Search term or pattern
            limit: Optional limit (if None, returns all matches across all 72 datasets)
        Returns:
            List of search results from all matching datasets
        """
        results = []
        
        for dataset_name, dataset_content in self.datasets.items():
            dataset_results = self._search_single_dataset(dataset_name, dataset_content, query)
            results.extend(dataset_results)
        
        # Sort by relevance (could be improved with proper scoring)
        results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        # Apply limit only if specified (no default limit of 10)
        if limit is not None:
            results = results[:limit]
            
        return results
    
    def _search_single_dataset(self, dataset_name: str, dataset_content: Any, query: str) -> List[Dict[str, Any]]:
        """Search within a single dataset"""
        results = []
        query_lower = query.lower()
        
        if isinstance(dataset_content, dict):
            if dataset_content.get("type") == "sql":
                # Search in SQL content
                sql_content = dataset_content.get("sql_content", "")
                if query_lower in sql_content.lower():
                    results.append({
                        "dataset": dataset_name,
                        "type": "sql",
                        "match": sql_content,
                        "relevance_score": sql_content.lower().count(query_lower)
                    })
            else:
                # Search in JSON data structure
                matches = self._search_json_content(dataset_content, query_lower)
                for match in matches:
                    results.append({
                        "dataset": dataset_name,
                        "type": "json",
                        "match": match,
                        "relevance_score": str(match).lower().count(query_lower)
                    })
        
        return results
    
    def _search_json_content(self, data: Any, query: str) -> List[Any]:
        """Recursively search through JSON data structure"""
        matches = []
        
        if isinstance(data, dict):
            for key, value in data.items():
                if query in str(key).lower() or query in str(value).lower():
                    matches.append({key: value})
                if isinstance(value, (dict, list)):
                    matches.extend(self._search_json_content(value, query))
        
        elif isinstance(data, list):
            for item in data:
                if query in str(item).lower():
                    matches.append(item)
                if isinstance(item, (dict, list)):
                    matches.extend(self._search_json_content(item, query))
        
        return matches
    
    def get_all_datasets(self) -> Dict[str, Any]:
        """Return all loaded datasets"""
        return self.datasets
    
    def get_dataset_count(self) -> int:
        """Return the total number of datasets"""
        return len(self.datasets)
    
    def add_dataset(self, name: str, content: Any, dataset_type: str = "json"):
        """Add a new dataset"""
        if dataset_type == "sql":
            # Store SQL content with proper structure
            self.datasets[name] = {"sql_content": content, "type": "sql"}
        else:
            self.datasets[name] = content
        
        # Save to file
        if dataset_type == "json":
            file_path = self.datasets_dir / f"{name}.json"
            with open(file_path, 'w') as f:
                json.dump(content, f, indent=2)
        elif dataset_type == "sql":
            file_path = self.datasets_dir / f"{name}.sql"
            with open(file_path, 'w') as f:
                f.write(content)
    
    def get_dataset_info(self) -> Dict[str, Any]:
        """Get information about all datasets"""
        info = {
            "total_datasets": self.get_dataset_count(),
            "target_capacity": 72,
            "datasets": []
        }
        
        for name, content in self.datasets.items():
            dataset_info = {
                "name": name,
                "type": "sql" if isinstance(content, dict) and content.get("type") == "sql" else "json",
                "size": len(str(content)) if content else 0
            }
            info["datasets"].append(dataset_info)
        
        return info