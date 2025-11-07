"""
INSPIRE-HEP 下载器的单元测试。
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
    """InspireHEPClient 类的测试。"""
    
    def setUp(self):
        """设置测试装置。"""
        self.client = InspireHEPClient()
    
    def test_client_initialization(self):
        """测试客户端是否正确初始化。"""
        self.assertEqual(self.client.BASE_URL, "https://inspirehep.net/api")
        self.assertEqual(self.client.timeout, 30)
        self.assertIsNotNone(self.client.session)
    
    def test_client_custom_timeout(self):
        """测试带有自定义超时的客户端。"""
        client = InspireHEPClient(timeout=60)
        self.assertEqual(client.timeout, 60)
    
    @patch('inspirehep_downloader.client.requests.Session.get')
    def test_search_literature(self, mock_get):
        """测试文献搜索。"""
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
        """测试获取特定记录。"""
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
        """测试从文档中获取 PDF URL。"""
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
        """测试从 arXiv 获取 PDF URL。"""
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
        """测试在 PDF URL 不可用时获取它。"""
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
        """测试获取格式化的元数据。"""
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
    """下载器功能的测试。"""
    
    def setUp(self):
        """设置测试装置。"""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """清理测试装置。"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    @patch('inspirehep_downloader.downloader.InspireHEPClient')
    def test_download_pdf(self, mock_client_class):
        """测试下载 PDF。"""
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
        """测试在 PDF 不可用时下载它。"""
        mock_client = Mock()
        mock_client.get_pdf_url.return_value = None
        mock_client_class.return_value = mock_client
        
        with self.assertRaises(ValueError):
            download_pdf("12345", output_dir=self.temp_dir)
    
    @patch('inspirehep_downloader.downloader.InspireHEPClient')
    def test_download_metadata_json(self, mock_client_class):
        """测试下载 JSON 格式的元数据。"""
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
        """测试下载文本格式的元数据。"""
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
        """测试使用无效格式下载元数据。"""
        with self.assertRaises(ValueError):
            download_metadata("12345", output_dir=self.temp_dir, format="xml")
    
    @patch('inspirehep_downloader.downloader.download_pdf')
    @patch('inspirehep_downloader.downloader.download_metadata')
    def test_download_record(self, mock_download_metadata, mock_download_pdf):
        """测试下载 PDF 和元数据。"""
        mock_download_pdf.return_value = os.path.join(self.temp_dir, "12345.pdf")
        mock_download_metadata.return_value = os.path.join(self.temp_dir, "12345_metadata.json")
        
        results = download_record("12345", output_dir=self.temp_dir)
        
        self.assertIn("pdf", results)
        self.assertIn("metadata", results)
        mock_download_pdf.assert_called_once()
        mock_download_metadata.assert_called_once()


if __name__ == "__main__":
    unittest.main()
