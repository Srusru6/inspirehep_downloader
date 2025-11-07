"""
INSPIRE-HEP 下载器的命令行界面。
"""

import argparse
import sys
from .downloader import download_pdf, download_metadata, download_record
from .client import InspireHEPClient


def main():
    """CLI 的主入口点。"""
    parser = argparse.ArgumentParser(
        description="从 inspirehep.net 下载 PDF 和元数据",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 下载记录的 PDF 和元数据
  inspirehep-download 12345

  # 仅下载 PDF
  inspirehep-download 12345 --pdf-only

  # 仅下载元数据
  inspirehep-download 12345 --metadata-only

  # 下载到特定目录
  inspirehep-download 12345 --output-dir /path/to/dir

  # 将元数据另存为文本文件
  inspirehep-download 12345 --format txt

  # 搜索记录
  inspirehep-download --search "author:witten" --size 5
        """
    )
    
    parser.add_argument(
        "record_id",
        nargs="?",
        help="INSPIRE-HEP 记录 ID"
    )
    
    parser.add_argument(
        "--output-dir", "-o",
        default=".",
        help="下载文件的输出目录 (默认值: 当前目录)"
    )
    
    parser.add_argument(
        "--pdf-only",
        action="store_true",
        help="仅下载 PDF"
    )
    
    parser.add_argument(
        "--metadata-only",
        action="store_true",
        help="仅下载元数据"
    )
    
    parser.add_argument(
        "--format", "-f",
        choices=["json", "txt"],
        default="json",
        help="元数据格式 (默认值: json)"
    )
    
    parser.add_argument(
        "--search", "-s",
        help="搜索查询而不是记录 ID (例如, 'author:witten')"
    )
    
    parser.add_argument(
        "--size",
        type=int,
        default=10,
        help="要显示的搜索结果数 (默认值: 10)"
    )
    
    args = parser.parse_args()
    
    # 处理搜索模式
    if args.search:
        client = InspireHEPClient()
        try:
            print(f"正在搜索: {args.search}")
            results = client.search_literature(args.search, size=args.size)
            hits = results.get("hits", {}).get("hits", [])
            
            if not hits:
                print("未找到结果。")
                return 0
            
            print(f"\n找到 {results.get('hits', {}).get('total', 0)} 个结果 (显示 {len(hits)} 个):\n")
            
            for i, hit in enumerate(hits, 1):
                metadata = hit.get("metadata", {})
                record_id = hit.get("id", "N/A")
                title = metadata.get("titles", [{}])[0].get("title", "N/A")
                authors = metadata.get("authors", [])
                author_names = ", ".join([a.get("full_name", "") for a in authors[:3]])
                if len(authors) > 3:
                    author_names += f" (以及另外 {len(authors) - 3} 位)"
                
                print(f"{i}. [{record_id}] {title}")
                print(f"   作者: {author_names}")
                print()
            
            return 0
        except Exception as e:
            print(f"搜索期间出错: {e}", file=sys.stderr)
            return 1
    
    # 处理下载模式
    if not args.record_id:
        parser.print_help()
        return 1
    
    try:
        # 确定要下载什么
        download_pdf_flag = not args.metadata_only
        download_metadata_flag = not args.pdf_only
        
        if args.metadata_only:
            # 仅下载元数据
            download_metadata(args.record_id, args.output_dir, format=args.format)
        elif args.pdf_only:
            # 仅下载 PDF
            download_pdf(args.record_id, args.output_dir)
        else:
            # 下载两者
            download_record(args.record_id, args.output_dir, download_pdf_flag, download_metadata_flag)
        
        return 0
    
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
