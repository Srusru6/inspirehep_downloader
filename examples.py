#!/usr/bin/env python3
"""
Example script demonstrating the usage of inspirehep_downloader.
"""

from inspirehep_downloader import InspireHEPClient, download_pdf, download_metadata, download_record


def example_search():
    """Example: Search for literature."""
    print("=" * 80)
    print("Example 1: Searching for literature")
    print("=" * 80)
    
    client = InspireHEPClient()
    
    # Search by author
    results = client.search_literature("author:witten", size=3)
    hits = results.get("hits", {}).get("hits", [])
    
    print(f"Found {results.get('hits', {}).get('total', 0)} papers by Witten")
    print(f"Showing first {len(hits)} results:\n")
    
    for i, hit in enumerate(hits, 1):
        metadata = hit.get("metadata", {})
        record_id = hit.get("id")
        title = metadata.get("titles", [{}])[0].get("title", "N/A")
        print(f"{i}. [{record_id}] {title}")
    
    print()


def example_get_metadata():
    """Example: Get metadata for a specific record."""
    print("=" * 80)
    print("Example 2: Getting metadata")
    print("=" * 80)
    
    client = InspireHEPClient()
    
    # Use a well-known paper (you may need to replace with a valid record ID)
    record_id = "1"
    
    try:
        metadata = client.get_metadata(record_id)
        
        print(f"Record ID: {metadata['record_id']}")
        print(f"Title: {metadata['title']}")
        print(f"Authors: {', '.join(metadata['authors'][:3])}")
        if len(metadata['authors']) > 3:
            print(f"  (and {len(metadata['authors']) - 3} more authors)")
        print(f"Publication Date: {metadata['publication_date']}")
        print(f"arXiv ID: {metadata['arxiv_id']}")
        print(f"Citations: {metadata['citations']}")
        print()
    except Exception as e:
        print(f"Error getting metadata: {e}")
        print()


def example_download():
    """Example: Download PDF and metadata."""
    print("=" * 80)
    print("Example 3: Downloading PDF and metadata")
    print("=" * 80)
    
    # Use a valid record ID
    record_id = "1"
    
    print(f"Attempting to download record {record_id}...")
    print("Note: This will only work if the record has an available PDF")
    print()
    
    try:
        results = download_record(record_id, output_dir="./examples_output")
        
        if results.get("pdf"):
            print(f"✓ PDF downloaded: {results['pdf']}")
        else:
            print("✗ PDF not available")
        
        if results.get("metadata"):
            print(f"✓ Metadata downloaded: {results['metadata']}")
        else:
            print("✗ Metadata not available")
        
        print()
    except Exception as e:
        print(f"Error during download: {e}")
        print()


if __name__ == "__main__":
    print("\nINSPIRE-HEP Downloader Examples\n")
    
    # Note: These examples may fail if the INSPIRE-HEP API is not accessible
    # or if the record IDs are invalid
    
    print("Note: Examples may require internet access to inspirehep.net\n")
    
    try:
        example_search()
    except Exception as e:
        print(f"Search example failed: {e}\n")
    
    try:
        example_get_metadata()
    except Exception as e:
        print(f"Metadata example failed: {e}\n")
    
    try:
        example_download()
    except Exception as e:
        print(f"Download example failed: {e}\n")
    
    print("Examples completed!")
