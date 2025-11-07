"""
Client for interacting with INSPIRE-HEP API.
"""

import requests
from typing import Dict, List, Optional
import json


class InspireHEPClient:
    """Client for accessing INSPIRE-HEP API."""
    
    BASE_URL = "https://inspirehep.net/api"
    
    def __init__(self, timeout: int = 30):
        """
        Initialize the INSPIRE-HEP client.
        
        Args:
            timeout: Request timeout in seconds (default: 30)
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json"
        })
    
    def search_literature(self, query: str, size: int = 10, page: int = 1) -> Dict:
        """
        Search for literature in INSPIRE-HEP.
        
        Args:
            query: Search query string (e.g., "author:witten", "title:supersymmetry")
            size: Number of results to return (default: 10)
            page: Page number for pagination (default: 1)
        
        Returns:
            Dictionary containing search results
        
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        url = f"{self.BASE_URL}/literature"
        params = {
            "q": query,
            "size": size,
            "page": page
        }
        
        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def get_record(self, record_id: str) -> Dict:
        """
        Get a specific literature record by ID.
        
        Args:
            record_id: The INSPIRE-HEP record ID
        
        Returns:
            Dictionary containing the record metadata
        
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        url = f"{self.BASE_URL}/literature/{record_id}"
        
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def get_pdf_url(self, record_id: str) -> Optional[str]:
        """
        Get the PDF URL for a specific record.
        
        Args:
            record_id: The INSPIRE-HEP record ID
        
        Returns:
            URL of the PDF if available, None otherwise
        """
        record = self.get_record(record_id)
        metadata = record.get("metadata", {})
        
        # Check for documents with PDFs
        documents = metadata.get("documents", [])
        for doc in documents:
            if doc.get("key", "").endswith(".pdf"):
                return doc.get("url")
        
        # Check for arxiv eprints
        arxiv_eprints = metadata.get("arxiv_eprints", [])
        if arxiv_eprints:
            arxiv_id = arxiv_eprints[0].get("value")
            if arxiv_id:
                return f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        
        return None
    
    def get_metadata(self, record_id: str) -> Dict:
        """
        Get formatted metadata for a specific record.
        
        Args:
            record_id: The INSPIRE-HEP record ID
        
        Returns:
            Dictionary containing formatted metadata
        """
        record = self.get_record(record_id)
        metadata = record.get("metadata", {})
        
        # Extract relevant metadata
        formatted_metadata = {
            "record_id": record_id,
            "title": metadata.get("titles", [{}])[0].get("title", "N/A"),
            "authors": [author.get("full_name", "N/A") for author in metadata.get("authors", [])],
            "abstract": metadata.get("abstracts", [{}])[0].get("value", "N/A"),
            "publication_date": metadata.get("preprint_date") or metadata.get("publication_info", [{}])[0].get("year", "N/A"),
            "arxiv_id": metadata.get("arxiv_eprints", [{}])[0].get("value", "N/A"),
            "doi": metadata.get("dois", [{}])[0].get("value", "N/A"),
            "citations": metadata.get("citation_count", 0),
            "keywords": [kw.get("value", "") for kw in metadata.get("keywords", [])],
            "inspire_url": f"https://inspirehep.net/literature/{record_id}",
        }
        
        return formatted_metadata
    
    def download_file(self, url: str, output_path: str) -> None:
        """
        Download a file from a URL.
        
        Args:
            url: URL of the file to download
            output_path: Path where the file should be saved
        
        Raises:
            requests.exceptions.RequestException: If the download fails
        """
        response = self.session.get(url, stream=True, timeout=self.timeout)
        response.raise_for_status()
        
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
