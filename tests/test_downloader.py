"""
Unit tests for INSPIRE-HEP downloader.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import json
import os
import tempfile
import shutil

from inspirehep_downloader.client import InspireHEPClient
from inspirehep_downloader.downloader import download_pdf, download_metadata, download_record


class TestInspireHEPClient(unittest.TestCase):
    """Tests for InspireHEPClient class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = InspireHEPClient()
    
    def test_client_initialization(self):
        """Test that client initializes correctly."""
        self.assertEqual(self.client.BASE_URL, "https://inspirehep.net/api")
        self.assertEqual(self.client.timeout, 30)
        self.assertIsNotNone(self.client.session)
    
    def test_client_custom_timeout(self):
        """Test client with custom timeout."""
        client = InspireHEPClient(timeout=60)
        self.assertEqual(client.timeout, 60)
    
    @patch('inspirehep_downloader.client.requests.Session.get')
    def test_search_literature(self, mock_get):
        """Test literature search."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "hits": {
                "hits": [{"id": "12345", "metadata": {"titles": [{"title": "Test Paper"}]}}],
                "total": 1
            }
        }
        mock_get.return_value = mock_response
        
        results = self.client.search_literature("author:test", size=1)
        
        self.assertIn("hits", results)
        mock_get.assert_called_once()
    
    @patch('inspirehep_downloader.client.requests.Session.get')
    def test_get_record(self, mock_get):
        """Test getting a specific record."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "12345",
            "metadata": {"titles": [{"title": "Test Paper"}]}
        }
        mock_get.return_value = mock_response
        
        record = self.client.get_record("12345")
        
        self.assertEqual(record["id"], "12345")
        mock_get.assert_called_once()
    
    @patch('inspirehep_downloader.client.requests.Session.get')
    def test_get_pdf_url_from_documents(self, mock_get):
        """Test getting PDF URL from documents."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "metadata": {
                "documents": [
                    {"key": "paper.pdf", "url": "https://example.com/paper.pdf"}
                ]
            }
        }
        mock_get.return_value = mock_response
        
        pdf_url = self.client.get_pdf_url("12345")
        
        self.assertEqual(pdf_url, "https://example.com/paper.pdf")
    
    @patch('inspirehep_downloader.client.requests.Session.get')
    def test_get_pdf_url_from_arxiv(self, mock_get):
        """Test getting PDF URL from arXiv."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "metadata": {
                "documents": [],
                "arxiv_eprints": [{"value": "1234.5678"}]
            }
        }
        mock_get.return_value = mock_response
        
        pdf_url = self.client.get_pdf_url("12345")
        
        self.assertEqual(pdf_url, "https://arxiv.org/pdf/1234.5678.pdf")
    
    @patch('inspirehep_downloader.client.requests.Session.get')
    def test_get_pdf_url_not_available(self, mock_get):
        """Test getting PDF URL when not available."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "metadata": {
                "documents": [],
                "arxiv_eprints": []
            }
        }
        mock_get.return_value = mock_response
        
        pdf_url = self.client.get_pdf_url("12345")
        
        self.assertIsNone(pdf_url)
    
    @patch('inspirehep_downloader.client.requests.Session.get')
    def test_get_metadata(self, mock_get):
        """Test getting formatted metadata."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "metadata": {
                "titles": [{"title": "Test Paper"}],
                "authors": [{"full_name": "John Doe"}],
                "abstracts": [{"value": "Test abstract"}],
                "preprint_date": "2023",
                "arxiv_eprints": [{"value": "1234.5678"}],
                "dois": [{"value": "10.1234/test"}],
                "citation_count": 10,
                "keywords": [{"value": "test"}]
            }
        }
        mock_get.return_value = mock_response
        
        metadata = self.client.get_metadata("12345")
        
        self.assertEqual(metadata["title"], "Test Paper")
        self.assertEqual(metadata["authors"], ["John Doe"])
        self.assertEqual(metadata["citations"], 10)


class TestDownloaderFunctions(unittest.TestCase):
    """Tests for downloader functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    @patch('inspirehep_downloader.downloader.InspireHEPClient')
    def test_download_pdf(self, mock_client_class):
        """Test downloading PDF."""
        mock_client = Mock()
        mock_client.get_pdf_url.return_value = "https://example.com/paper.pdf"
        mock_client.download_file = Mock()
        mock_client_class.return_value = mock_client
        
        result = download_pdf("12345", output_dir=self.temp_dir)
        
        self.assertTrue(result.endswith("12345.pdf"))
        mock_client.get_pdf_url.assert_called_once_with("12345")
        mock_client.download_file.assert_called_once()
    
    @patch('inspirehep_downloader.downloader.InspireHEPClient')
    def test_download_pdf_not_available(self, mock_client_class):
        """Test downloading PDF when not available."""
        mock_client = Mock()
        mock_client.get_pdf_url.return_value = None
        mock_client_class.return_value = mock_client
        
        with self.assertRaises(ValueError):
            download_pdf("12345", output_dir=self.temp_dir)
    
    @patch('inspirehep_downloader.downloader.InspireHEPClient')
    def test_download_metadata_json(self, mock_client_class):
        """Test downloading metadata as JSON."""
        mock_client = Mock()
        mock_client.get_metadata.return_value = {
            "record_id": "12345",
            "title": "Test Paper",
            "authors": ["John Doe"]
        }
        mock_client_class.return_value = mock_client
        
        result = download_metadata("12345", output_dir=self.temp_dir, format="json")
        
        self.assertTrue(os.path.exists(result))
        self.assertTrue(result.endswith(".json"))
        
        with open(result, "r") as f:
            data = json.load(f)
            self.assertEqual(data["title"], "Test Paper")
    
    @patch('inspirehep_downloader.downloader.InspireHEPClient')
    def test_download_metadata_txt(self, mock_client_class):
        """Test downloading metadata as text."""
        mock_client = Mock()
        mock_client.get_metadata.return_value = {
            "record_id": "12345",
            "title": "Test Paper",
            "authors": ["John Doe"],
            "publication_date": "2023",
            "arxiv_id": "1234.5678",
            "doi": "10.1234/test",
            "citations": 10,
            "inspire_url": "https://inspirehep.net/literature/12345",
            "keywords": ["test"],
            "abstract": "Test abstract"
        }
        mock_client_class.return_value = mock_client
        
        result = download_metadata("12345", output_dir=self.temp_dir, format="txt")
        
        self.assertTrue(os.path.exists(result))
        self.assertTrue(result.endswith(".txt"))
        
        with open(result, "r") as f:
            content = f.read()
            self.assertIn("Test Paper", content)
            self.assertIn("John Doe", content)
    
    @patch('inspirehep_downloader.downloader.InspireHEPClient')
    def test_download_metadata_invalid_format(self, mock_client_class):
        """Test downloading metadata with invalid format."""
        with self.assertRaises(ValueError):
            download_metadata("12345", output_dir=self.temp_dir, format="xml")
    
    @patch('inspirehep_downloader.downloader.download_pdf')
    @patch('inspirehep_downloader.downloader.download_metadata')
    def test_download_record(self, mock_download_metadata, mock_download_pdf):
        """Test downloading both PDF and metadata."""
        mock_download_pdf.return_value = os.path.join(self.temp_dir, "12345.pdf")
        mock_download_metadata.return_value = os.path.join(self.temp_dir, "12345_metadata.json")
        
        results = download_record("12345", output_dir=self.temp_dir)
        
        self.assertIn("pdf", results)
        self.assertIn("metadata", results)
        mock_download_pdf.assert_called_once()
        mock_download_metadata.assert_called_once()


if __name__ == "__main__":
    unittest.main()
