#!/usr/bin/env python3
"""
Tests for SearchEngine class
Validates unlimited search across all datasets
"""

import unittest
import tempfile
import shutil
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from dataset_manager import DatasetManager
from search_engine import SearchEngine


class TestSearchEngine(unittest.TestCase):
    """Test cases for SearchEngine"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.dataset_manager = DatasetManager(self.test_dir)
        self.search_engine = SearchEngine(self.dataset_manager)
        
        # Add sample datasets for testing
        self._create_test_datasets()
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def _create_test_datasets(self):
        """Create test datasets for search testing"""
        # JSON datasets
        for i in range(10):
            json_data = {
                "id": i,
                "name": f"test_dataset_{i}",
                "description": f"This is test dataset number {i}",
                "tags": ["test", "sample", f"dataset_{i}"],
                "searchable_content": f"unique_term_{i}",
                "common_field": "searchable_value"
            }
            self.dataset_manager.add_dataset(f"json_test_{i}", json_data, "json")
        
        # SQL datasets
        for i in range(10):
            sql_content = f"""
            CREATE TABLE test_table_{i} (
                id INTEGER PRIMARY KEY,
                name VARCHAR(100),
                description TEXT
            );
            
            INSERT INTO test_table_{i} VALUES 
                ({i}, 'test_record_{i}', 'searchable_description_{i}');
            
            SELECT * FROM test_table_{i} WHERE name LIKE '%search%';
            """
            self.dataset_manager.add_dataset(f"sql_test_{i}", sql_content, "sql")
    
    def test_unlimited_search(self):
        """Test that search returns all results without default limits"""
        # Search for common term that appears in all datasets
        results = self.search_engine.search("test")
        
        # Should find results in all 20 datasets (10 JSON + 10 SQL)
        self.assertEqual(results['datasets_searched'], 20)
        self.assertGreater(results['total_results'], 0)
        self.assertFalse(results['limited'])  # No limit applied
        self.assertEqual(results['total_results'], results['results_returned'])
    
    def test_search_with_explicit_limit(self):
        """Test that explicit limits are respected"""
        results = self.search_engine.search("test", limit=5)
        
        self.assertEqual(results['datasets_searched'], 20)
        self.assertEqual(results['results_returned'], 5)
        self.assertTrue(results['limited'])
        self.assertGreater(results['total_results'], results['results_returned'])
    
    def test_search_type_filtering(self):
        """Test filtering by dataset type"""
        # Search only SQL datasets
        sql_results = self.search_engine.search("SELECT", search_type="sql")
        
        self.assertGreater(sql_results['total_results'], 0)
        for result in sql_results['results']:
            self.assertEqual(result['type'], 'sql')
        
        # Search only JSON datasets
        json_results = self.search_engine.search("searchable_value", search_type="json")
        
        self.assertGreater(json_results['total_results'], 0)
        for result in json_results['results']:
            self.assertEqual(result['type'], 'json')
    
    def test_case_sensitivity(self):
        """Test case sensitive and insensitive search"""
        # Case insensitive (default)
        results_insensitive = self.search_engine.search("TEST", case_sensitive=False)
        
        # Case sensitive
        results_sensitive = self.search_engine.search("TEST", case_sensitive=True)
        
        # Should find more results with case insensitive search
        self.assertGreaterEqual(
            results_insensitive['total_results'], 
            results_sensitive['total_results']
        )
    
    def test_regex_search(self):
        """Test regex pattern matching"""
        # Simple regex pattern that should match our test data
        results = self.search_engine.search(r"test.*\d+", use_regex=True)
        
        self.assertGreater(results['total_results'], 0)
        self.assertTrue(results['search_parameters']['use_regex'])
    
    def test_search_statistics(self):
        """Test search statistics functionality"""
        stats = self.search_engine.get_search_statistics()
        
        self.assertEqual(stats['total_datasets'], 20)
        self.assertEqual(stats['sql_datasets'], 10)
        self.assertEqual(stats['json_datasets'], 10)
        self.assertEqual(stats['target_capacity'], 72)
        self.assertTrue(stats['search_unlimited'])
        self.assertTrue(stats['supports_regex'])
        self.assertTrue(stats['supports_case_sensitive'])
    
    def test_large_scale_search(self):
        """Test search performance with many datasets"""
        # Add more datasets to simulate the 72 dataset target
        for i in range(20, 72):
            if i % 2 == 0:
                json_data = {"id": i, "content": f"bulk_data_{i}", "search_term": "bulk"}
                self.dataset_manager.add_dataset(f"bulk_json_{i}", json_data, "json")
            else:
                sql_content = f"CREATE TABLE bulk_table_{i} (id INT); -- bulk comment"
                self.dataset_manager.add_dataset(f"bulk_sql_{i}", sql_content, "sql")
        
        # Verify we have 72 datasets
        self.assertEqual(self.dataset_manager.get_dataset_count(), 72)
        
        # Search across all 72 datasets
        results = self.search_engine.search("bulk")
        
        self.assertEqual(results['datasets_searched'], 72)
        self.assertEqual(results['total_datasets_available'], 72)
        self.assertGreater(results['total_results'], 0)
        self.assertFalse(results['limited'])  # No default limit
    
    def test_search_result_structure(self):
        """Test the structure of search results"""
        results = self.search_engine.search("test", limit=3)
        
        # Check result structure
        required_keys = [
            'query', 'total_results', 'datasets_searched', 
            'total_datasets_available', 'results_returned', 
            'limited', 'results', 'search_parameters'
        ]
        
        for key in required_keys:
            self.assertIn(key, results)
        
        # Check search parameters structure
        param_keys = ['search_type', 'case_sensitive', 'use_regex', 'limit']
        for key in param_keys:
            self.assertIn(key, results['search_parameters'])
        
        # Check individual result structure
        if results['results']:
            result = results['results'][0]
            self.assertIn('dataset', result)
            self.assertIn('type', result)
            self.assertIn('relevance_score', result)
    
    def test_empty_search_query(self):
        """Test handling of empty search queries"""
        results = self.search_engine.search("")
        
        # Should handle empty queries gracefully
        self.assertEqual(results['query'], "")
        self.assertEqual(results['total_results'], 0)
    
    def test_no_matches_found(self):
        """Test behavior when no matches are found"""
        results = self.search_engine.search("nonexistent_term_xyz123")
        
        self.assertEqual(results['total_results'], 0)
        self.assertEqual(results['results_returned'], 0)
        self.assertEqual(len(results['results']), 0)
        self.assertFalse(results['limited'])
    
    def test_relevance_scoring(self):
        """Test that results are sorted by relevance"""
        # Add dataset with multiple occurrences of search term
        high_relevance_data = {
            "test": "test",
            "test_field": "test value",
            "description": "test test test"  # Multiple occurrences
        }
        self.dataset_manager.add_dataset("high_relevance", high_relevance_data, "json")
        
        results = self.search_engine.search("test")
        
        # Results should be sorted by relevance (highest first)
        if len(results['results']) > 1:
            first_score = results['results'][0]['relevance_score']
            second_score = results['results'][1]['relevance_score']
            self.assertGreaterEqual(first_score, second_score)


if __name__ == '__main__':
    unittest.main()