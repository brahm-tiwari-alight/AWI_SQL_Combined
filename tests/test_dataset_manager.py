#!/usr/bin/env python3
"""
Tests for DatasetManager class
Validates that all 72 datasets can be managed without limits
"""

import unittest
import tempfile
import shutil
import os
import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from dataset_manager import DatasetManager


class TestDatasetManager(unittest.TestCase):
    """Test cases for DatasetManager"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.dataset_manager = DatasetManager(self.test_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_initialization(self):
        """Test DatasetManager initialization"""
        self.assertTrue(os.path.exists(self.test_dir))
        self.assertEqual(self.dataset_manager.get_dataset_count(), 0)
    
    def test_add_json_dataset(self):
        """Test adding JSON datasets"""
        test_data = {"test": "data", "value": 123}
        self.dataset_manager.add_dataset("test_json", test_data, "json")
        
        self.assertEqual(self.dataset_manager.get_dataset_count(), 1)
        self.assertIn("test_json", self.dataset_manager.datasets)
        self.assertEqual(self.dataset_manager.datasets["test_json"], test_data)
    
    def test_add_sql_dataset(self):
        """Test adding SQL datasets"""
        sql_content = "SELECT * FROM test_table;"
        self.dataset_manager.add_dataset("test_sql", sql_content, "sql")
        
        self.assertEqual(self.dataset_manager.get_dataset_count(), 1)
        self.assertIn("test_sql", self.dataset_manager.datasets)
    
    def test_search_without_limits(self):
        """Test that search works without default limits"""
        # Add multiple datasets
        for i in range(20):  # Simulate having many datasets
            test_data = {"name": f"dataset_{i}", "content": f"searchable_term_{i}"}
            self.dataset_manager.add_dataset(f"dataset_{i}", test_data, "json")
        
        # Search without specifying limit - should return all matches
        results = self.dataset_manager.search_all_datasets("searchable_term")
        
        # Should find matches in all 20 datasets (no limit applied)
        self.assertEqual(len(results), 20)
    
    def test_search_with_explicit_limit(self):
        """Test that search respects explicit limits when provided"""
        # Add multiple datasets
        for i in range(15):
            test_data = {"name": f"dataset_{i}", "content": "common_term"}
            self.dataset_manager.add_dataset(f"dataset_{i}", test_data, "json")
        
        # Search with explicit limit
        results = self.dataset_manager.search_all_datasets("common_term", limit=5)
        
        # Should respect the explicit limit
        self.assertEqual(len(results), 5)
    
    def test_large_dataset_capacity(self):
        """Test handling of large number of datasets (up to 72)"""
        # Create datasets up to the target capacity
        target_count = 72
        
        for i in range(target_count):
            if i % 2 == 0:
                # JSON dataset
                data = {"id": i, "type": "json", "data": f"content_{i}"}
                self.dataset_manager.add_dataset(f"json_dataset_{i}", data, "json")
            else:
                # SQL dataset  
                sql = f"CREATE TABLE table_{i} (id INT, name VARCHAR(50));"
                self.dataset_manager.add_dataset(f"sql_dataset_{i}", sql, "sql")
        
        # Verify all datasets are loaded
        self.assertEqual(self.dataset_manager.get_dataset_count(), target_count)
        
        # Search across all datasets - use a term that should be found
        results = self.dataset_manager.search_all_datasets("table")
        
        # Should search all 72 datasets without limitation
        self.assertGreater(len(results), 0)
        
        # Verify dataset info
        info = self.dataset_manager.get_dataset_info()
        self.assertEqual(info["total_datasets"], target_count)
        self.assertEqual(info["target_capacity"], 72)
    
    def test_dataset_info(self):
        """Test dataset information retrieval"""
        # Add some test datasets
        json_data = {"test": "json"}
        sql_data = "SELECT 1;"
        
        self.dataset_manager.add_dataset("test_json", json_data, "json")
        self.dataset_manager.add_dataset("test_sql", sql_data, "sql")
        
        info = self.dataset_manager.get_dataset_info()
        
        self.assertEqual(info["total_datasets"], 2)
        self.assertEqual(info["target_capacity"], 72)
        self.assertEqual(len(info["datasets"]), 2)
        
        # Check dataset types are correctly identified
        dataset_types = [d["type"] for d in info["datasets"]]
        self.assertIn("json", dataset_types)
        self.assertIn("sql", dataset_types)
    
    def test_file_persistence(self):
        """Test that datasets are persisted to files"""
        json_data = {"persistent": "data"}
        sql_data = "CREATE TABLE persistent_table (id INT);"
        
        self.dataset_manager.add_dataset("persistent_json", json_data, "json")
        self.dataset_manager.add_dataset("persistent_sql", sql_data, "sql")
        
        # Verify files were created
        json_file = Path(self.test_dir) / "persistent_json.json"
        sql_file = Path(self.test_dir) / "persistent_sql.sql"
        
        self.assertTrue(json_file.exists())
        self.assertTrue(sql_file.exists())
        
        # Verify file contents
        with open(json_file, 'r') as f:
            loaded_json = json.load(f)
            self.assertEqual(loaded_json, json_data)
        
        with open(sql_file, 'r') as f:
            loaded_sql = f.read()
            self.assertEqual(loaded_sql, sql_data)
    
    def test_reload_from_files(self):
        """Test loading datasets from existing files"""
        # Create files directly
        json_file = Path(self.test_dir) / "file_dataset.json"
        sql_file = Path(self.test_dir) / "file_sql.sql"
        
        json_data = {"loaded": "from_file"}
        with open(json_file, 'w') as f:
            json.dump(json_data, f)
        
        with open(sql_file, 'w') as f:
            f.write("SELECT * FROM file_table;")
        
        # Create new manager to test loading
        new_manager = DatasetManager(self.test_dir)
        
        self.assertEqual(new_manager.get_dataset_count(), 2)
        self.assertIn("file_dataset", new_manager.datasets)
        self.assertIn("file_sql", new_manager.datasets)


if __name__ == '__main__':
    unittest.main()