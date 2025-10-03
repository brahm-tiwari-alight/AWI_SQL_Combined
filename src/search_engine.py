"""
Search Engine for AWI SQL Combined Repository
Provides advanced search capabilities across all 72 datasets
"""

from typing import List, Dict, Any, Optional, Set
import re
from dataset_manager import DatasetManager


class SearchEngine:
    """Advanced search engine that searches across all datasets without limits"""
    
    def __init__(self, dataset_manager: DatasetManager):
        self.dataset_manager = dataset_manager
    
    def search(self, 
               query: str, 
               search_type: str = "all",
               case_sensitive: bool = False,
               use_regex: bool = False,
               limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Advanced search across all datasets
        Args:
            query: Search query
            search_type: "all", "sql", "json" - type of datasets to search
            case_sensitive: Whether search should be case sensitive
            use_regex: Whether to use regex pattern matching
            limit: Optional limit (None means no limit - search all 72 datasets)
        Returns:
            Dictionary with search results and metadata
        """
        
        # Handle empty queries
        if not query.strip():
            return {
                "query": query,
                "total_results": 0,
                "datasets_searched": len(self.dataset_manager.datasets),
                "total_datasets_available": self.dataset_manager.get_dataset_count(),
                "results_returned": 0,
                "limited": False,
                "results": [],
                "search_parameters": {
                    "search_type": search_type,
                    "case_sensitive": case_sensitive,
                    "use_regex": use_regex,
                    "limit": limit
                }
            }
        
        # Remove any default pagination - we want to search ALL datasets
        if not case_sensitive:
            query = query.lower()
        
        all_results = []
        datasets_searched = 0
        
        for dataset_name, dataset_content in self.dataset_manager.datasets.items():
            datasets_searched += 1
            
            # Filter by search type
            if search_type == "sql" and not self._is_sql_dataset(dataset_content):
                continue
            elif search_type == "json" and self._is_sql_dataset(dataset_content):
                continue
            
            # Perform search on this dataset
            dataset_results = self._search_dataset(
                dataset_name, 
                dataset_content, 
                query, 
                case_sensitive, 
                use_regex
            )
            all_results.extend(dataset_results)
        
        # Sort by relevance
        all_results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        # Apply limit only if specified (no default limit)
        limited_results = all_results[:limit] if limit else all_results
        
        return {
            "query": query,
            "total_results": len(all_results),
            "datasets_searched": datasets_searched,
            "total_datasets_available": self.dataset_manager.get_dataset_count(),
            "results_returned": len(limited_results),
            "limited": limit is not None and len(all_results) > limit,
            "results": limited_results,
            "search_parameters": {
                "search_type": search_type,
                "case_sensitive": case_sensitive,
                "use_regex": use_regex,
                "limit": limit
            }
        }
    
    def _is_sql_dataset(self, dataset_content: Any) -> bool:
        """Check if dataset is SQL type"""
        return isinstance(dataset_content, dict) and dataset_content.get("type") == "sql"
    
    def _search_dataset(self, 
                       dataset_name: str, 
                       dataset_content: Any, 
                       query: str, 
                       case_sensitive: bool, 
                       use_regex: bool) -> List[Dict[str, Any]]:
        """Search within a single dataset"""
        results = []
        
        if self._is_sql_dataset(dataset_content):
            results.extend(self._search_sql_content(
                dataset_name, dataset_content, query, case_sensitive, use_regex
            ))
        else:
            results.extend(self._search_json_content(
                dataset_name, dataset_content, query, case_sensitive, use_regex
            ))
        
        return results
    
    def _search_sql_content(self, 
                           dataset_name: str, 
                           dataset_content: Dict[str, Any], 
                           query: str, 
                           case_sensitive: bool, 
                           use_regex: bool) -> List[Dict[str, Any]]:
        """Search SQL content"""
        results = []
        sql_content = dataset_content.get("sql_content", "")
        
        if not case_sensitive:
            search_content = sql_content.lower()
        else:
            search_content = sql_content
        
        if use_regex:
            try:
                flags = 0 if case_sensitive else re.IGNORECASE
                matches = re.findall(query, search_content, flags)
                if matches:
                    results.append({
                        "dataset": dataset_name,
                        "type": "sql",
                        "matches": matches,
                        "match_count": len(matches),
                        "content_preview": sql_content[:200] + "..." if len(sql_content) > 200 else sql_content,
                        "relevance_score": len(matches)
                    })
            except re.error:
                # Fallback to simple search if regex is invalid
                if query in search_content:
                    count = search_content.count(query)
                    results.append({
                        "dataset": dataset_name,
                        "type": "sql",
                        "matches": [query] * count,
                        "match_count": count,
                        "content_preview": sql_content[:200] + "..." if len(sql_content) > 200 else sql_content,
                        "relevance_score": count
                    })
        else:
            if query in search_content:
                count = search_content.count(query)
                results.append({
                    "dataset": dataset_name,
                    "type": "sql",
                    "matches": [query] * count,
                    "match_count": count,
                    "content_preview": sql_content[:200] + "..." if len(sql_content) > 200 else sql_content,
                    "relevance_score": count
                })
        
        return results
    
    def _search_json_content(self, 
                            dataset_name: str, 
                            dataset_content: Any, 
                            query: str, 
                            case_sensitive: bool, 
                            use_regex: bool,
                            path: str = "") -> List[Dict[str, Any]]:
        """Recursively search JSON content"""
        results = []
        
        if isinstance(dataset_content, dict):
            for key, value in dataset_content.items():
                current_path = f"{path}.{key}" if path else key
                
                # Search in key
                if self._match_text(str(key), query, case_sensitive, use_regex):
                    results.append({
                        "dataset": dataset_name,
                        "type": "json",
                        "match_type": "key",
                        "path": current_path,
                        "key": key,
                        "value": value,
                        "relevance_score": 1
                    })
                
                # Search in value
                if isinstance(value, str) and self._match_text(value, query, case_sensitive, use_regex):
                    results.append({
                        "dataset": dataset_name,
                        "type": "json",
                        "match_type": "value",
                        "path": current_path,
                        "key": key,
                        "value": value,
                        "relevance_score": 1
                    })
                
                # Recurse into nested structures
                if isinstance(value, (dict, list)):
                    results.extend(self._search_json_content(
                        dataset_name, value, query, case_sensitive, use_regex, current_path
                    ))
        
        elif isinstance(dataset_content, list):
            for i, item in enumerate(dataset_content):
                current_path = f"{path}[{i}]" if path else f"[{i}]"
                
                if isinstance(item, str) and self._match_text(item, query, case_sensitive, use_regex):
                    results.append({
                        "dataset": dataset_name,
                        "type": "json",
                        "match_type": "array_item",
                        "path": current_path,
                        "value": item,
                        "relevance_score": 1
                    })
                
                # Recurse into nested structures
                if isinstance(item, (dict, list)):
                    results.extend(self._search_json_content(
                        dataset_name, item, query, case_sensitive, use_regex, current_path
                    ))
        
        return results
    
    def _match_text(self, text: str, query: str, case_sensitive: bool, use_regex: bool) -> bool:
        """Check if text matches query"""
        # Handle empty queries
        if not query:
            return False
            
        if not case_sensitive:
            text = text.lower()
        
        if use_regex:
            try:
                flags = 0 if case_sensitive else re.IGNORECASE
                return bool(re.search(query, text, flags))
            except re.error:
                # Fallback to simple search
                return query in text
        else:
            return query in text
    
    def get_search_statistics(self) -> Dict[str, Any]:
        """Get statistics about searchable content"""
        total_datasets = self.dataset_manager.get_dataset_count()
        sql_datasets = 0
        json_datasets = 0
        
        for dataset_content in self.dataset_manager.datasets.values():
            if self._is_sql_dataset(dataset_content):
                sql_datasets += 1
            else:
                json_datasets += 1
        
        return {
            "total_datasets": total_datasets,
            "sql_datasets": sql_datasets,
            "json_datasets": json_datasets,
            "target_capacity": 72,
            "capacity_utilization": f"{(total_datasets/72)*100:.1f}%" if total_datasets <= 72 else "Over capacity",
            "search_unlimited": True,  # No default pagination limits
            "supports_regex": True,
            "supports_case_sensitive": True
        }