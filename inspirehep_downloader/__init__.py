"""
INSPIRE-HEP Downloader
A Python library for downloading PDFs and metadata from inspirehep.net using their API.
"""

__version__ = "0.1.0"

from .client import InspireHEPClient
from .downloader import download_pdf, download_metadata, download_record

__all__ = ["InspireHEPClient", "download_pdf", "download_metadata", "download_record"]
