"""
用于与 INSPIRE-HEP API 交互的客户端。
"""

import requests
from typing import Dict, List, Optional
import json


class InspireHEPClient:
    """用于访问 INSPIRE-HEP API 的客户端。"""
    
    BASE_URL = "https://inspirehep.net/api"
    
    def __init__(self, timeout: int = 30):
        """
        初始化 INSPIRE-HEP 客户端。
        
        Args:
            timeout: 请求超时秒数 (默认值: 30)
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json"
        })
    
    def search_literature(self, query: str, size: int = 10, page: int = 1) -> Dict:
        """
        在 INSPIRE-HEP 中搜索文献。
        
        Args:
            query: 搜索查询字符串 (例如, "author:witten", "title:supersymmetry")
            size: 返回的结果数 (默认值: 10)
            page: 用于分页的页码 (默认值: 1)
        
        Returns:
            包含搜索结果的字典
        
        Raises:
            requests.exceptions.RequestException: 如果请求失败
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
        按 ID 获取特定的文献记录。
        
        Args:
            record_id: INSPIRE-HEP 记录 ID
        
        Returns:
            包含记录元数据的字典
        
        Raises:
            requests.exceptions.RequestException: 如果请求失败
        """
        url = f"{self.BASE_URL}/literature/{record_id}"
        
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def get_pdf_url(self, record_id: str) -> Optional[str]:
        """
        获取特定记录的 PDF URL。
        
        Args:
            record_id: INSPIRE-HEP 记录 ID
        
        Returns:
            PDF 的 URL (如果可用)，否则为 None
        """
        record = self.get_record(record_id)
        metadata = record.get("metadata", {})
        
        # 检查带有 PDF 的文档
        documents = metadata.get("documents", [])
        for doc in documents:
            if doc.get("key", "").endswith(".pdf"):
                return doc.get("url")
        
        # 检查 arxiv eprints
        arxiv_eprints = metadata.get("arxiv_eprints", [])
        if arxiv_eprints:
            arxiv_id = arxiv_eprints[0].get("value")
            if arxiv_id:
                return f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        
        return None
    
    def get_metadata(self, record_id: str) -> Dict:
        """
        获取特定记录的格式化元数据。
        
        Args:
            record_id: INSPIRE-HEP 记录 ID
        
        Returns:
            包含格式化元数据的字典
        """
        record = self.get_record(record_id)
        metadata = record.get("metadata", {})
        
        # 提取相关元数据
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
        从 URL 下载文件。
        
        Args:
            url: 要下载的文件的 URL
            output_path: 文件应保存的路径
        
        Raises:
            requests.exceptions.RequestException: 如果下载失败
        """
        response = self.session.get(url, stream=True, timeout=self.timeout)
        response.raise_for_status()
        
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
