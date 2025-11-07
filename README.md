# INSPIRE-HEP Downloader

A Python library and command-line tool for downloading PDFs and metadata from [inspirehep.net](https://inspirehep.net) using their API.

## Features

- 🔍 Search for literature on INSPIRE-HEP
- 📄 Download PDFs from INSPIRE-HEP records
- 📊 Download and format metadata (JSON or text)
- 🖥️ Easy-to-use command-line interface
- 🐍 Python API for integration into your projects

## Installation

### From source

```bash
git clone https://github.com/Srusru6/inspirehep_downloader.git
cd inspirehep_downloader
pip install -r requirements.txt
pip install -e .
```

### Requirements

- Python 3.6+
- requests >= 2.25.0

## Usage

### Command Line Interface

#### Download both PDF and metadata

```bash
inspirehep-download 12345
```

#### Download only PDF

```bash
inspirehep-download 12345 --pdf-only
```

#### Download only metadata

```bash
inspirehep-download 12345 --metadata-only
```

#### Save metadata as text file

```bash
inspirehep-download 12345 --format txt
```

#### Download to a specific directory

```bash
inspirehep-download 12345 --output-dir /path/to/downloads
```

#### Search for records

```bash
# Search by author
inspirehep-download --search "author:witten" --size 10

# Search by title
inspirehep-download --search "title:supersymmetry" --size 5

# Search by keyword
inspirehep-download --search "black holes" --size 20
```

### Python API

#### Basic usage

```python
from inspirehep_downloader import download_pdf, download_metadata

# Download PDF
pdf_path = download_pdf("12345", output_dir="./downloads")

# Download metadata as JSON
metadata_path = download_metadata("12345", output_dir="./downloads", format="json")

# Download metadata as text
metadata_path = download_metadata("12345", output_dir="./downloads", format="txt")
```

#### Using the client directly

```python
from inspirehep_downloader import InspireHEPClient

client = InspireHEPClient()

# Search for literature
results = client.search_literature("author:witten", size=10)

# Get a specific record
record = client.get_record("12345")

# Get metadata
metadata = client.get_metadata("12345")

# Get PDF URL
pdf_url = client.get_pdf_url("12345")

# Download PDF
client.download_file(pdf_url, "output.pdf")
```

#### Download both PDF and metadata

```python
from inspirehep_downloader.downloader import download_record

results = download_record("12345", output_dir="./downloads")
print(f"PDF: {results['pdf']}")
print(f"Metadata: {results['metadata']}")
```

## API Reference

### InspireHEPClient

Main client class for interacting with the INSPIRE-HEP API.

**Methods:**
- `search_literature(query, size=10, page=1)` - Search for literature
- `get_record(record_id)` - Get a specific record by ID
- `get_pdf_url(record_id)` - Get the PDF URL for a record
- `get_metadata(record_id)` - Get formatted metadata for a record
- `download_file(url, output_path)` - Download a file from a URL

### Functions

- `download_pdf(record_id, output_dir=".", filename=None)` - Download PDF for a record
- `download_metadata(record_id, output_dir=".", filename=None, format="json")` - Download metadata
- `download_record(record_id, output_dir=".", download_pdf_flag=True, download_metadata_flag=True)` - Download both

## Examples

### Example 1: Download a specific paper

```python
from inspirehep_downloader import download_record

# Download Witten's paper on M-theory
results = download_record("419176", output_dir="./witten_papers")
```

### Example 2: Search and download multiple papers

```python
from inspirehep_downloader import InspireHEPClient, download_pdf
import os

client = InspireHEPClient()

# Search for papers
results = client.search_literature("author:maldacena AND title:ads/cft", size=5)

# Download PDFs for all results
for hit in results.get("hits", {}).get("hits", []):
    record_id = hit.get("id")
    try:
        download_pdf(record_id, output_dir="./maldacena_papers")
        print(f"Downloaded {record_id}")
    except Exception as e:
        print(f"Failed to download {record_id}: {e}")
```

### Example 3: Get metadata and format it

```python
from inspirehep_downloader import InspireHEPClient
import json

client = InspireHEPClient()

# Get metadata
metadata = client.get_metadata("12345")

# Print formatted metadata
print(f"Title: {metadata['title']}")
print(f"Authors: {', '.join(metadata['authors'][:3])}")
print(f"Publication Date: {metadata['publication_date']}")
print(f"Citations: {metadata['citations']}")
print(f"arXiv: {metadata['arxiv_id']}")
print(f"DOI: {metadata['doi']}")
```

## Search Query Syntax

The search function supports INSPIRE-HEP's query syntax:

- `author:surname` - Search by author surname
- `title:words` - Search in title
- `abstract:words` - Search in abstract
- `arxiv:1234.5678` - Search by arXiv ID
- `doi:10.1234/example` - Search by DOI
- `date > 2020` - Search by date
- Combine with `AND`, `OR`, `NOT` operators

For more details, see [INSPIRE-HEP search documentation](https://help.inspirehep.net/knowledge-base/inspire-paper-search/).

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

This project uses the [INSPIRE-HEP API](https://github.com/inspirehep/rest-api-doc) to access high-energy physics literature.
