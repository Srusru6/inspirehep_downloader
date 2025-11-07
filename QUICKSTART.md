# Quick Start Guide

This guide will help you get started with the INSPIRE-HEP Downloader.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Srusru6/inspirehep_downloader.git
cd inspirehep_downloader
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package:
```bash
pip install -e .
```

## Your First Download

### Using the Command Line

The easiest way to download papers is using the command line interface:

```bash
# Search for papers by an author
inspirehep-download --search "author:witten" --size 5

# Download a specific paper by its INSPIRE-HEP record ID
inspirehep-download 12345

# Download to a specific directory
inspirehep-download 12345 --output-dir ~/Downloads/papers
```

### Using Python

You can also use the Python API directly:

```python
from inspirehep_downloader import InspireHEPClient, download_pdf, download_metadata

# Initialize the client
client = InspireHEPClient()

# Search for papers
results = client.search_literature("author:witten", size=5)
print(f"Found {results['hits']['total']} papers")

# Download a paper
download_pdf("12345", output_dir="./papers")
download_metadata("12345", output_dir="./papers", format="json")
```

## Common Use Cases

### 1. Search for Papers

```bash
# By author
inspirehep-download --search "author:maldacena" --size 10

# By title
inspirehep-download --search "title:ads/cft" --size 5

# By keyword
inspirehep-download --search "black holes" --size 20
```

### 2. Download PDFs

```bash
# Download just the PDF
inspirehep-download 12345 --pdf-only

# Download with custom filename
inspirehep-download 12345 --output-dir ./papers
```

### 3. Download Metadata

```bash
# Download as JSON
inspirehep-download 12345 --metadata-only --format json

# Download as text file
inspirehep-download 12345 --metadata-only --format txt
```

### 4. Batch Downloads

Use Python for batch downloads:

```python
from inspirehep_downloader import InspireHEPClient, download_record

client = InspireHEPClient()

# Search for multiple papers
results = client.search_literature("author:witten", size=10)

# Download each paper
for hit in results["hits"]["hits"]:
    record_id = hit["id"]
    try:
        download_record(record_id, output_dir="./witten_papers")
        print(f"✓ Downloaded {record_id}")
    except Exception as e:
        print(f"✗ Failed to download {record_id}: {e}")
```

## Tips

1. **Finding Record IDs**: Use the search function first to find papers, then note their record IDs for downloading.

2. **Network Issues**: If downloads fail, check your internet connection and try again.

3. **PDF Availability**: Not all papers have PDFs available. The tool will try to find PDFs from INSPIRE-HEP documents or arXiv.

4. **Metadata Formats**: 
   - Use `json` format for programmatic processing
   - Use `txt` format for human-readable output

## Getting Help

For more information:

```bash
inspirehep-download --help
```

Or check the [full documentation](README.md).

## Examples

See `examples.py` for more detailed usage examples.

## Troubleshooting

**Problem**: `inspirehep-download: command not found`

**Solution**: Make sure you installed the package with `pip install -e .`

---

**Problem**: Download fails with "No PDF available"

**Solution**: Not all papers have PDFs. Try downloading just the metadata instead:
```bash
inspirehep-download 12345 --metadata-only
```

---

**Problem**: Connection timeout

**Solution**: Increase the timeout by using the Python API:
```python
from inspirehep_downloader import InspireHEPClient
client = InspireHEPClient(timeout=120)  # 2 minutes
```
