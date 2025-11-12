"""
INSPIRE-HEP 下载器
一个使用其 API 从 inspirehep.net 下载 PDF 和元数据的 Python 库。
"""

__version__ = "0.1.0"

from .client import InspireHEPClient
from .downloader import download_pdf, download_metadata, download_record
from .checkmentor_integration import search_and_download_author_papers

__all__ = ["InspireHEPClient", "download_pdf", "download_metadata", "download_record", "search_and_download_author_papers"]
