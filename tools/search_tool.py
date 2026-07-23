# tools/search_tool.py
# This implements the web search functionality using Tavily

import os
from tavily import TavilyClient
from typing import List, Dict


class SearchTool:
    """Tool for searching the web using Tavily API"""

    def __init__(self):
        """Initialize the search tool with API key from environment"""
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("TAVILY_API_KEY not found in environment variables")
        self.client = TavilyClient(api_key=api_key)

    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Search the web for a given query

        Args:
            query: Search query string
            max_results: Maximum number of results to return

        Returns:
            List of search results with title, content, and URL
        """
        try:
            # Perform the search
            results = self.client.search(
                query=query,
                max_results=max_results,
                include_raw_content=True
            )

            # Format results
            formatted_results = []
            for result in results.get('results', []):
                formatted_results.append({
                    'title': result.get('title', ''),
                    'content': result.get('content', ''),
                    'url': result.get('url', ''),
                    'score': result.get('score', 0)
                })

            return formatted_results

        except Exception as e:
            print(f"Search error: {e}")
            return []

    def search_multiple(self, queries: List[str]) -> List[Dict]:
        """
        Search for multiple queries

        Args:
            queries: List of search queries

        Returns:
            Combined search results
        """
        all_results = []
        for query in queries:
            results = self.search(query)
            all_results.extend(results)
        return all_results


# Create a singleton instance
search_tool = SearchTool()