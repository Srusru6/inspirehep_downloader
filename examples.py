#!/usr/bin/env python3
"""
演示 inspirehep_downloader 用法的示例脚本。
"""

from inspirehep_downloader import InspireHEPClient, download_pdf, download_metadata, download_record


def example_search():
    """示例：搜索文献。"""
    print("=" * 80)
    print("示例 1：搜索文献")
    print("=" * 80)
    
    client = InspireHEPClient()
    
    # 按作者搜索
    results = client.search_literature("author:witten", size=3)
    hits = results.get("hits", {}).get("hits", [])
    
    print(f"找到 {results.get('hits', {}).get('total', 0)} 篇 Witten 的论文")
    print(f"显示前 {len(hits)} 个结果：\n")
    
    for i, hit in enumerate(hits, 1):
        metadata = hit.get("metadata", {})
        record_id = hit.get("id")
        title = metadata.get("titles", [{}])[0].get("title", "N/A")
        print(f"{i}. [{record_id}] {title}")
    
    print()


def example_get_metadata():
    """示例：获取特定记录的元数据。"""
    print("=" * 80)
    print("示例 2：获取元数据")
    print("=" * 80)
    
    client = InspireHEPClient()
    
    # 使用一篇著名的论文（您可能需要替换为有效的记录 ID）
    record_id = "1"
    
    try:
        metadata = client.get_metadata(record_id)
        
        print(f"记录 ID: {metadata['record_id']}")
        print(f"标题: {metadata['title']}")
        print(f"作者: {', '.join(metadata['authors'][:3])}")
        if len(metadata['authors']) > 3:
            print(f"  (以及另外 {len(metadata['authors']) - 3} 位作者)")
        print(f"出版日期: {metadata['publication_date']}")
        print(f"arXiv ID: {metadata['arxiv_id']}")
        print(f"引文: {metadata['citations']}")
        print()
    except Exception as e:
        print(f"获取元数据时出错: {e}")
        print()


def example_download():
    """示例：下载 PDF 和元数据。"""
    print("=" * 80)
    print("示例 3：下载 PDF 和元数据")
    print("=" * 80)
    
    # 使用有效的记录 ID
    record_id = "1"
    
    print(f"正在尝试下载记录 {record_id}...")
    print("注意：这仅在记录具有可用的 PDF 时才有效")
    print()
    
    try:
        results = download_record(record_id, output_dir="./examples_output")
        
        if results.get("pdf"):
            print(f"✓ PDF 已下载: {results['pdf']}")
        else:
            print("✗ PDF 不可用")
        
        if results.get("metadata"):
            print(f"✓ 元数据已下载: {results['metadata']}")
        else:
            print("✗ 元数据不可用")
        
        print()
    except Exception as e:
        print(f"下载期间出错: {e}")
        print()


if __name__ == "__main__":
    print("\nINSPIRE-HEP 下载器示例\n")
    
    # 注意：如果无法访问 INSPIRE-HEP API 或记录 ID 无效，这些示例可能会失败
    
    print("注意：示例可能需要互联网访问 inspirehep.net\n")
    
    try:
        example_search()
    except Exception as e:
        print(f"搜索示例失败: {e}\n")
    
    try:
        example_get_metadata()
    except Exception as e:
        print(f"元数据示例失败: {e}\n")
    
    try:
        example_download()
    except Exception as e:
        print(f"下载示例失败: {e}\n")
    
    print("示例完成！")
