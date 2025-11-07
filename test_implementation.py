"""
Manual test script to verify the implementation works.
This script tests the structure and API without making real network calls.
"""

import sys
import os

# Test imports
print("Testing imports...")
try:
    from inspirehep_downloader import InspireHEPClient, download_pdf, download_metadata
    from inspirehep_downloader.downloader import download_record
    from inspirehep_downloader.cli import main
    print("✓ All imports successful\n")
except Exception as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

# Test client initialization
print("Testing client initialization...")
try:
    client = InspireHEPClient()
    assert client.BASE_URL == "https://inspirehep.net/api"
    assert client.timeout == 30
    print("✓ Client initialized successfully\n")
except Exception as e:
    print(f"✗ Client initialization failed: {e}")
    sys.exit(1)

# Test client with custom timeout
print("Testing client with custom timeout...")
try:
    client = InspireHEPClient(timeout=60)
    assert client.timeout == 60
    print("✓ Custom timeout works\n")
except Exception as e:
    print(f"✗ Custom timeout failed: {e}")
    sys.exit(1)

# Test API methods exist
print("Testing API methods...")
try:
    methods = ['search_literature', 'get_record', 'get_pdf_url', 'get_metadata', 'download_file']
    for method in methods:
        assert hasattr(client, method), f"Method {method} not found"
    print("✓ All required methods exist\n")
except Exception as e:
    print(f"✗ API method check failed: {e}")
    sys.exit(1)

# Test module structure
print("Testing module structure...")
try:
    import inspirehep_downloader
    assert hasattr(inspirehep_downloader, '__version__')
    print(f"✓ Package version: {inspirehep_downloader.__version__}\n")
except Exception as e:
    print(f"✗ Module structure check failed: {e}")
    sys.exit(1)

# Test CLI entry point
print("Testing CLI entry point...")
try:
    import subprocess
    result = subprocess.run(['inspirehep-download', '--help'], 
                          capture_output=True, 
                          text=True,
                          timeout=5)
    assert result.returncode == 0
    assert 'inspirehep.net' in result.stdout
    print("✓ CLI entry point works\n")
except Exception as e:
    print(f"✗ CLI test failed: {e}")
    sys.exit(1)

print("=" * 80)
print("All tests passed successfully!")
print("=" * 80)
print("\nThe INSPIRE-HEP downloader is ready to use!")
print("\nQuick start:")
print("  1. Search for papers: inspirehep-download --search 'author:witten' --size 5")
print("  2. Download a paper: inspirehep-download <record_id>")
print("  3. See all options: inspirehep-download --help")
print("\nNote: Actual downloads require internet access to inspirehep.net")
