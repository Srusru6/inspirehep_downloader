"""
用于验证实现是否有效的手动测试脚本。
此脚本测试结构和 API，而不进行实际的网络调用。
"""

import sys
import os

# 测试导入
print("正在测试导入...")
try:
    from inspirehep_downloader import InspireHEPClient, download_pdf, download_metadata
    from inspirehep_downloader.downloader import download_record
    from inspirehep_downloader.cli import main
    print("✓ 所有导入成功\n")
except Exception as e:
    print(f"✗ 导入失败: {e}")
    sys.exit(1)

# 测试客户端初始化
print("正在测试客户端初始化...")
try:
    client = InspireHEPClient()
    assert client.BASE_URL == "https://inspirehep.net/api"
    assert client.timeout == 30
    print("✓ 客户端初始化成功\n")
except Exception as e:
    print(f"✗ 客户端初始化失败: {e}")
    sys.exit(1)

# 测试带自定义超时的客户端
print("正在测试带自定义超时的客户端...")
try:
    client = InspireHEPClient(timeout=60)
    assert client.timeout == 60
    print("✓ 自定义超时有效\n")
except Exception as e:
    print(f"✗ 自定义超时失败: {e}")
    sys.exit(1)

# 测试 API 方法是否存在
print("正在测试 API 方法...")
try:
    methods = ['search_literature', 'get_record', 'get_pdf_url', 'get_metadata', 'download_file']
    for method in methods:
        assert hasattr(client, method), f"未找到方法 {method}"
    print("✓ 所有必需的方法都存在\n")
except Exception as e:
    print(f"✗ API 方法检查失败: {e}")
    sys.exit(1)

# 测试模块结构
print("正在测试模块结构...")
try:
    import inspirehep_downloader
    assert hasattr(inspirehep_downloader, '__version__')
    print(f"✓ 软件包版本: {inspirehep_downloader.__version__}\n")
except Exception as e:
    print(f"✗ 模块结构检查失败: {e}")
    sys.exit(1)

# 测试 CLI 入口点
print("正在测试 CLI 入口点...")
try:
    import subprocess
    result = subprocess.run(['inspirehep-download', '--help'], 
                          capture_output=True, 
                          text=True,
                          timeout=5)
    assert result.returncode == 0
    assert 'inspirehep.net' in result.stdout
    print("✓ CLI 入口点有效\n")
except Exception as e:
    print(f"✗ CLI 测试失败: {e}")
    sys.exit(1)

print("=" * 80)
print("所有测试均已成功通过！")
print("=" * 80)
print("\nINSPIRE-HEP 下载器已准备就绪！")
print("\n快速入门:")
print("  1. 搜索论文: inspirehep-download --search 'author:witten' --size 5")
print("  2. 下载论文: inspirehep-download <record_id>")
print("  3. 查看所有选项: inspirehep-download --help")
print("\n注意：实际下载需要访问 inspirehep.net 的互联网连接")
