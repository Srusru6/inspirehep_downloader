"""
用于从 INSPIRE-HEP 下载 PDF 和元数据的高级函数。
"""

import os
import json
from typing import Optional, Dict
from .client import InspireHEPClient


def download_pdf(record_id: str, output_dir: str = ".", filename: Optional[str] = None) -> str:
    """
    下载特定 INSPIRE-HEP 记录的 PDF。
    
    Args:
        record_id: INSPIRE-HEP 记录 ID
        output_dir: PDF 应保存的目录 (默认值: 当前目录)
        filename: 可选的自定义文件名 (默认值: {record_id}.pdf)
    
    Returns:
        下载的 PDF 文件的路径
    
    Raises:
        ValueError: 如果记录没有可用的 PDF
        requests.exceptions.RequestException: 如果下载失败
    """
    client = InspireHEPClient()
    
    # 获取 PDF URL
    pdf_url = client.get_pdf_url(record_id)
    if not pdf_url:
        raise ValueError(f"记录 {record_id} 没有可用的 PDF")
    
    # 如果输出目录不存在，则创建它
    os.makedirs(output_dir, exist_ok=True)
    
    # 设置文件名
    if filename is None:
        filename = f"{record_id}.pdf"
    
    output_path = os.path.join(output_dir, filename)
    
    # 下载 PDF
    print(f"正在从 {pdf_url} 下载 PDF...")
    client.download_file(pdf_url, output_path)
    print(f"PDF 已保存到 {output_path}")
    
    return output_path


def download_metadata(record_id: str, output_dir: str = ".", filename: Optional[str] = None, format: str = "json") -> str:
    """
    下载特定 INSPIRE-HEP 记录的元数据。
    
    Args:
        record_id: INSPIRE-HEP 记录 ID
        output_dir: 元数据应保存的目录 (默认值: 当前目录)
        filename: 可选的自定义文件名 (默认值: {record_id}_metadata.{format})
        format: 输出格式，"json" 或 "txt" (默认值: "json")
    
    Returns:
        保存的元数据文件的路径
    
    Raises:
        ValueError: 如果格式不受支持
        requests.exceptions.RequestException: 如果获取元数据失败
    """
    if format not in ["json", "txt"]:
        raise ValueError(f"不支持的格式: {format}。请使用 'json' 或 'txt'")
    
    client = InspireHEPClient()
    
    # 获取元数据
    print(f"正在获取记录 {record_id} 的元数据...")
    metadata = client.get_metadata(record_id)
    
    # 如果输出目录不存在，则创建它
    os.makedirs(output_dir, exist_ok=True)
    
    # 设置文件名
    if filename is None:
        filename = f"{record_id}_metadata.{format}"
    
    output_path = os.path.join(output_dir, filename)
    
    # 以请求的格式保存元数据
    if format == "json":
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
    else:  # txt 格式
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"INSPIRE-HEP 记录: {metadata['record_id']}\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"标题: {metadata['title']}\n\n")
            f.write(f"作者: {', '.join(metadata['authors'])}\n\n")
            f.write(f"出版日期: {metadata['publication_date']}\n")
            f.write(f"arXiv ID: {metadata['arxiv_id']}\n")
            f.write(f"DOI: {metadata['doi']}\n")
            f.write(f"引文: {metadata['citations']}\n")
            f.write(f"INSPIRE URL: {metadata['inspire_url']}\n\n")
            if metadata['keywords']:
                f.write(f"关键字: {', '.join(metadata['keywords'])}\n\n")
            f.write(f"摘要:\n{metadata['abstract']}\n")
    
    print(f"元数据已保存到 {output_path}")
    
    return output_path


def download_record(record_id: str, output_dir: str = ".", download_pdf_flag: bool = True, download_metadata_flag: bool = True) -> Dict[str, str]:
    """
    下载特定 INSPIRE-HEP 记录的 PDF 和元数据。
    
    Args:
        record_id: INSPIRE-HEP 记录 ID
        output_dir: 文件应保存的目录 (默认值: 当前目录)
        download_pdf_flag: 是否下载 PDF (默认值: True)
        download_metadata_flag: 是否下载元数据 (默认值: True)
    
    Returns:
        包含下载文件路径的字典
    
    Raises:
        requests.exceptions.RequestException: 如果下载失败
    """
    results = {}
    
    if download_metadata_flag:
        try:
            metadata_path = download_metadata(record_id, output_dir)
            results["metadata"] = metadata_path
        except Exception as e:
            print(f"警告: 无法下载元数据: {e}")
            results["metadata"] = None
    
    if download_pdf_flag:
        try:
            pdf_path = download_pdf(record_id, output_dir)
            results["pdf"] = pdf_path
        except Exception as e:
            print(f"警告: 无法下载 PDF: {e}")
            results["pdf"] = None
    
    return results
