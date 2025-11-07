# How to Use INSPIRE-HEP Downloader

## Quick Reference

### Command Line Usage

```bash
# Basic download (PDF + metadata)
inspirehep-download <record_id>

# Search for papers
inspirehep-download --search "author:surname"

# Download only PDF
inspirehep-download <record_id> --pdf-only

# Download only metadata
inspirehep-download <record_id> --metadata-only

# Specify output directory
inspirehep-download <record_id> -o /path/to/dir

# Get metadata as text file
inspirehep-download <record_id> --format txt
```

### Python API Usage

```python
from inspirehep_downloader import InspireHEPClient, download_pdf, download_metadata

# Initialize client
client = InspireHEPClient()

# Search
results = client.search_literature("author:witten", size=10)

# Download
download_pdf("12345", output_dir="./papers")
download_metadata("12345", output_dir="./papers", format="json")
```

## Common Workflows

### 1. Find and Download Papers by an Author

```bash
# First, search for the author
inspirehep-download --search "author:maldacena" --size 10

# Note the record IDs from the results
# Then download specific papers
inspirehep-download 123456 -o ./maldacena_papers
inspirehep-download 789012 -o ./maldacena_papers
```

### 2. Batch Download Papers (Python)

```python
from inspirehep_downloader import InspireHEPClient, download_record

client = InspireHEPClient()

# Search for papers
results = client.search_literature("black holes AND author:hawking", size=20)

# Download all results
for hit in results["hits"]["hits"]:
    record_id = hit["id"]
    title = hit["metadata"]["titles"][0]["title"]
    
    print(f"Downloading: {title}")
    try:
        download_record(record_id, output_dir="./hawking_black_holes")
    except Exception as e:
        print(f"  Failed: {e}")
```

### 3. Get Metadata Only for Citation Management

```bash
# Download metadata in JSON format for import into reference managers
inspirehep-download 12345 --metadata-only --format json -o ./references
```

### 4. Check Paper Details Before Downloading

```python
from inspirehep_downloader import InspireHEPClient

client = InspireHEPClient()

# Get metadata first
metadata = client.get_metadata("12345")

print(f"Title: {metadata['title']}")
print(f"Authors: {', '.join(metadata['authors'][:3])}")
print(f"Citations: {metadata['citations']}")
print(f"arXiv: {metadata['arxiv_id']}")

# Decide whether to download based on metadata
if metadata['citations'] > 100:
    from inspirehep_downloader import download_pdf
    download_pdf("12345")
```

## Search Query Examples

The search function supports INSPIRE-HEP's query syntax:

```bash
# By author
inspirehep-download --search "author:witten"

# By multiple authors
inspirehep-download --search "author:witten AND author:maldacena"

# By title keywords
inspirehep-download --search "title:supersymmetry"

# By abstract
inspirehep-download --search "abstract:quantum gravity"

# By arXiv ID
inspirehep-download --search "arxiv:1234.5678"

# By DOI
inspirehep-download --search "doi:10.1234/example"

# By date
inspirehep-download --search "date > 2020"

# Complex queries
inspirehep-download --search "author:witten AND title:M-theory AND date > 1995"
```

## Tips and Tricks

### 1. Handling Missing PDFs

Not all papers have PDFs available. Use metadata-only mode when PDFs aren't available:

```bash
# Try to download PDF
inspirehep-download 12345 --pdf-only

# If it fails, get metadata instead
inspirehep-download 12345 --metadata-only
```

### 2. Custom Timeouts for Slow Connections

```python
from inspirehep_downloader import InspireHEPClient

# Increase timeout to 2 minutes
client = InspireHEPClient(timeout=120)
record = client.get_record("12345")
```

### 3. Organizing Downloads

```bash
# Create author-specific directories
mkdir -p ./papers/witten
inspirehep-download 12345 -o ./papers/witten

mkdir -p ./papers/maldacena
inspirehep-download 67890 -o ./papers/maldacena
```

### 4. Extracting Record IDs from Search

```python
from inspirehep_downloader import InspireHEPClient

client = InspireHEPClient()
results = client.search_literature("author:witten", size=100)

# Get all record IDs
record_ids = [hit["id"] for hit in results["hits"]["hits"]]
print(f"Found {len(record_ids)} papers")

# Save to file
with open("witten_record_ids.txt", "w") as f:
    f.write("\n".join(record_ids))
```

## Troubleshooting

### Problem: Command not found

**Solution**: Reinstall the package
```bash
pip install -e .
```

### Problem: Connection timeout

**Solution**: Increase timeout or check internet connection
```python
client = InspireHEPClient(timeout=300)  # 5 minutes
```

### Problem: PDF not available

**Solution**: Try getting the arXiv ID and download directly from arXiv
```python
metadata = client.get_metadata("12345")
arxiv_id = metadata['arxiv_id']
# Use: https://arxiv.org/pdf/{arxiv_id}.pdf
```

### Problem: Rate limiting

**Solution**: Add delays between requests
```python
import time

for record_id in record_ids:
    download_record(record_id)
    time.sleep(2)  # Wait 2 seconds between downloads
```

## Advanced Usage

### Custom File Names

```python
from inspirehep_downloader import download_pdf

# Use custom filename
download_pdf("12345", output_dir="./papers", filename="witten_mtheory.pdf")
```

### Error Handling

```python
from inspirehep_downloader import download_record

try:
    results = download_record("12345")
    if results['pdf']:
        print(f"PDF downloaded: {results['pdf']}")
    if results['metadata']:
        print(f"Metadata downloaded: {results['metadata']}")
except ValueError as e:
    print(f"Download error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Processing Metadata

```python
import json
from inspirehep_downloader import download_metadata

# Download as JSON
metadata_path = download_metadata("12345", format="json")

# Load and process
with open(metadata_path, 'r') as f:
    data = json.load(f)
    
# Extract information
print(f"This paper has {len(data['authors'])} authors")
print(f"It has been cited {data['citations']} times")
```

## Need More Help?

- Check the [README](README.md) for detailed documentation
- See [QUICKSTART](QUICKSTART.md) for getting started
- Run `inspirehep-download --help` for command options
- Check [examples.py](examples.py) for code examples
