"""
High-level functions for downloading PDFs and metadata from INSPIRE-HEP.
"""

import os
import json
from typing import Optional, Dict
from .client import InspireHEPClient


def download_pdf(record_id: str, output_dir: str = ".", filename: Optional[str] = None) -> str:
    """
    Download PDF for a specific INSPIRE-HEP record.
    
    Args:
        record_id: The INSPIRE-HEP record ID
        output_dir: Directory where the PDF should be saved (default: current directory)
        filename: Optional custom filename (default: {record_id}.pdf)
    
    Returns:
        Path to the downloaded PDF file
    
    Raises:
        ValueError: If no PDF is available for the record
        requests.exceptions.RequestException: If the download fails
    """
    client = InspireHEPClient()
    
    # Get PDF URL
    pdf_url = client.get_pdf_url(record_id)
    if not pdf_url:
        raise ValueError(f"No PDF available for record {record_id}")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Set filename
    if filename is None:
        filename = f"{record_id}.pdf"
    
    output_path = os.path.join(output_dir, filename)
    
    # Download the PDF
    print(f"Downloading PDF from {pdf_url}...")
    client.download_file(pdf_url, output_path)
    print(f"PDF saved to {output_path}")
    
    return output_path


def download_metadata(record_id: str, output_dir: str = ".", filename: Optional[str] = None, format: str = "json") -> str:
    """
    Download metadata for a specific INSPIRE-HEP record.
    
    Args:
        record_id: The INSPIRE-HEP record ID
        output_dir: Directory where the metadata should be saved (default: current directory)
        filename: Optional custom filename (default: {record_id}_metadata.{format})
        format: Output format, either "json" or "txt" (default: "json")
    
    Returns:
        Path to the saved metadata file
    
    Raises:
        ValueError: If format is not supported
        requests.exceptions.RequestException: If fetching metadata fails
    """
    if format not in ["json", "txt"]:
        raise ValueError(f"Unsupported format: {format}. Use 'json' or 'txt'")
    
    client = InspireHEPClient()
    
    # Get metadata
    print(f"Fetching metadata for record {record_id}...")
    metadata = client.get_metadata(record_id)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Set filename
    if filename is None:
        filename = f"{record_id}_metadata.{format}"
    
    output_path = os.path.join(output_dir, filename)
    
    # Save metadata in the requested format
    if format == "json":
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
    else:  # txt format
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"INSPIRE-HEP Record: {metadata['record_id']}\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Title: {metadata['title']}\n\n")
            f.write(f"Authors: {', '.join(metadata['authors'])}\n\n")
            f.write(f"Publication Date: {metadata['publication_date']}\n")
            f.write(f"arXiv ID: {metadata['arxiv_id']}\n")
            f.write(f"DOI: {metadata['doi']}\n")
            f.write(f"Citations: {metadata['citations']}\n")
            f.write(f"INSPIRE URL: {metadata['inspire_url']}\n\n")
            if metadata['keywords']:
                f.write(f"Keywords: {', '.join(metadata['keywords'])}\n\n")
            f.write(f"Abstract:\n{metadata['abstract']}\n")
    
    print(f"Metadata saved to {output_path}")
    
    return output_path


def download_record(record_id: str, output_dir: str = ".", download_pdf_flag: bool = True, download_metadata_flag: bool = True) -> Dict[str, str]:
    """
    Download both PDF and metadata for a specific INSPIRE-HEP record.
    
    Args:
        record_id: The INSPIRE-HEP record ID
        output_dir: Directory where files should be saved (default: current directory)
        download_pdf_flag: Whether to download PDF (default: True)
        download_metadata_flag: Whether to download metadata (default: True)
    
    Returns:
        Dictionary with paths to downloaded files
    
    Raises:
        requests.exceptions.RequestException: If the download fails
    """
    results = {}
    
    if download_metadata_flag:
        try:
            metadata_path = download_metadata(record_id, output_dir)
            results["metadata"] = metadata_path
        except Exception as e:
            print(f"Warning: Could not download metadata: {e}")
            results["metadata"] = None
    
    if download_pdf_flag:
        try:
            pdf_path = download_pdf(record_id, output_dir)
            results["pdf"] = pdf_path
        except Exception as e:
            print(f"Warning: Could not download PDF: {e}")
            results["pdf"] = None
    
    return results
