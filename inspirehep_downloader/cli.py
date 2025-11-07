"""
Command-line interface for INSPIRE-HEP downloader.
"""

import argparse
import sys
from .downloader import download_pdf, download_metadata, download_record
from .client import InspireHEPClient


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Download PDFs and metadata from inspirehep.net",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download both PDF and metadata for a record
  inspirehep-download 12345

  # Download only PDF
  inspirehep-download 12345 --pdf-only

  # Download only metadata
  inspirehep-download 12345 --metadata-only

  # Download to a specific directory
  inspirehep-download 12345 --output-dir /path/to/dir

  # Save metadata as text file
  inspirehep-download 12345 --format txt

  # Search for records
  inspirehep-download --search "author:witten" --size 5
        """
    )
    
    parser.add_argument(
        "record_id",
        nargs="?",
        help="INSPIRE-HEP record ID"
    )
    
    parser.add_argument(
        "--output-dir", "-o",
        default=".",
        help="Output directory for downloaded files (default: current directory)"
    )
    
    parser.add_argument(
        "--pdf-only",
        action="store_true",
        help="Download only the PDF"
    )
    
    parser.add_argument(
        "--metadata-only",
        action="store_true",
        help="Download only the metadata"
    )
    
    parser.add_argument(
        "--format", "-f",
        choices=["json", "txt"],
        default="json",
        help="Metadata format (default: json)"
    )
    
    parser.add_argument(
        "--search", "-s",
        help="Search query instead of record ID (e.g., 'author:witten')"
    )
    
    parser.add_argument(
        "--size",
        type=int,
        default=10,
        help="Number of search results to display (default: 10)"
    )
    
    args = parser.parse_args()
    
    # Handle search mode
    if args.search:
        client = InspireHEPClient()
        try:
            print(f"Searching for: {args.search}")
            results = client.search_literature(args.search, size=args.size)
            hits = results.get("hits", {}).get("hits", [])
            
            if not hits:
                print("No results found.")
                return 0
            
            print(f"\nFound {results.get('hits', {}).get('total', 0)} results (showing {len(hits)}):\n")
            
            for i, hit in enumerate(hits, 1):
                metadata = hit.get("metadata", {})
                record_id = hit.get("id", "N/A")
                title = metadata.get("titles", [{}])[0].get("title", "N/A")
                authors = metadata.get("authors", [])
                author_names = ", ".join([a.get("full_name", "") for a in authors[:3]])
                if len(authors) > 3:
                    author_names += f" (and {len(authors) - 3} more)"
                
                print(f"{i}. [{record_id}] {title}")
                print(f"   Authors: {author_names}")
                print()
            
            return 0
        except Exception as e:
            print(f"Error during search: {e}", file=sys.stderr)
            return 1
    
    # Handle download mode
    if not args.record_id:
        parser.print_help()
        return 1
    
    try:
        # Determine what to download
        download_pdf_flag = not args.metadata_only
        download_metadata_flag = not args.pdf_only
        
        if args.metadata_only:
            # Download only metadata
            download_metadata(args.record_id, args.output_dir, format=args.format)
        elif args.pdf_only:
            # Download only PDF
            download_pdf(args.record_id, args.output_dir)
        else:
            # Download both
            download_record(args.record_id, args.output_dir, download_pdf_flag, download_metadata_flag)
        
        return 0
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
