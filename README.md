# INSPIRE-HEP 下载器

一个用于从 [inspirehep.net](https://inspirehep.net) 使用其 API 下载 PDF 和元数据的 Python 库和命令行工具。

## 功能

- 🔍 在 INSPIRE-HEP 上搜索文献
- 📄 从 INSPIRE-HEP 记录下载 PDF
- 📊 下载并格式化元数据 (JSON 或文本)
- 🖥️ 易于使用的命令行界面
- 🐍 用于集成到您的项目中的 Python API

## 安装

### 从源代码

```bash
git clone https://github.com/Srusru6/inspirehep_downloader.git
cd inspirehep_downloader
pip install -r requirements.txt
pip install -e .
```

### 要求

- Python 3.6+
- requests >= 2.25.0

## 用法

### 命令行界面

#### 下载 PDF 和元数据

```bash
inspirehep-download 12345
```

#### 仅下载 PDF

```bash
inspirehep-download 12345 --pdf-only
```

#### 仅下载元数据

```bash
inspirehep-download 12345 --metadata-only
```

#### 将元数据另存为文本文件

```bash
inspirehep-download 12345 --format txt
```

#### 下载到特定目录

```bash
inspirehep-download 12345 --output-dir /path/to/downloads
```

#### 搜索记录

```bash
# 按作者搜索
inspirehep-download --search "author:witten" --size 10

# 按标题搜索
inspirehep-download --search "title:supersymmetry" --size 5

# 按关键字搜索
inspirehep-download --search "black holes" --size 20
```

### Python API

#### 基本用法

```python
from inspirehep_downloader import download_pdf, download_metadata

# 下载 PDF
pdf_path = download_pdf("12345", output_dir="./downloads")

# 下载 JSON 格式的元数据
metadata_path = download_metadata("12345", output_dir="./downloads", format="json")

# 下载文本格式的元数据
metadata_path = download_metadata("12345", output_dir="./downloads", format="txt")
```

#### 直接使用客户端

```python
from inspirehep_downloader import InspireHEPClient

client = InspireHEPClient()

# 搜索文献
results = client.search_literature("author:witten", size=10)

# 获取特定记录
record = client.get_record("12345")

# 获取元数据
metadata = client.get_metadata("12345")

# 获取 PDF URL
pdf_url = client.get_pdf_url("12345")

# 下载 PDF
client.download_file(pdf_url, "output.pdf")
```

#### 下载 PDF 和元数据

```python
from inspirehep_downloader.downloader import download_record

results = download_record("12345", output_dir="./downloads")
print(f"PDF: {results['pdf']}")
print(f"元数据: {results['metadata']}")
```

## API 参考

### InspireHEPClient

用于与 INSPIRE-HEP API 交互的主客户端类。

**方法:**
- `search_literature(query, size=10, page=1)` - 搜索文献
- `get_record(record_id)` - 按 ID 获取特定记录
- `get_pdf_url(record_id)` - 获取记录的 PDF URL
- `get_metadata(record_id)` - 获取记录的格式化元数据
- `download_file(url, output_path)` - 从 URL 下载文件

### 函数

- `download_pdf(record_id, output_dir=".", filename=None)` - 下载记录的 PDF
- `download_metadata(record_id, output_dir=".", filename=None, format="json")` - 下载元数据
- `download_record(record_id, output_dir=".", download_pdf_flag=True, download_metadata_flag=True)` - 下载两者

## 示例

### 示例 1: 下载特定论文

```python
from inspirehep_downloader import download_record

# 下载 Witten 关于 M 理论的论文
results = download_record("419176", output_dir="./witten_papers")
```

### 示例 2: 搜索并下载多篇论文

```python
from inspirehep_downloader import InspireHEPClient, download_pdf
import os

client = InspireHEPClient()

# 搜索论文
results = client.search_literature("author:maldacena AND title:ads/cft", size=5)

# 下载所有结果的 PDF
for hit in results.get("hits", {}).get("hits", []):
    record_id = hit.get("id")
    try:
        download_pdf(record_id, output_dir="./maldacena_papers")
        print(f"已下载 {record_id}")
    except Exception as e:
        print(f"下载失败 {record_id}: {e}")
```

### 示例 3: 获取并格式化元数据

```python
from inspirehep_downloader import InspireHEPClient
import json

client = InspireHEPClient()

# 获取元数据
metadata = client.get_metadata("12345")

# 打印格式化的元数据
print(f"标题: {metadata['title']}")
print(f"作者: {', '.join(metadata['authors'][:3])}")
print(f"出版日期: {metadata['publication_date']}")
print(f"引文: {metadata['citations']}")
print(f"arXiv: {metadata['arxiv_id']}")
print(f"DOI: {metadata['doi']}")
```

## 搜索查询语法

搜索功能支持 INSPIRE-HEP 的查询语法：

- `author:surname` - 按作者姓氏搜索
- `title:words` - 在标题中搜索
- `abstract:words` - 在摘要中搜索
- `arxiv:1234.5678` - 按 arXiv ID 搜索
- `doi:10.1234/example` - 按 DOI 搜索
- `date > 2020` - 按日期搜索
- 与 `AND`, `OR`, `NOT` 运算符结合使用

有关更多详细信息，请参阅 [INSPIRE-HEP 搜索文档](https://help.inspirehep.net/knowledge-base/inspire-paper-search/)。

## 许可证

MIT 许可证

## 贡献

欢迎贡献！请随时提交拉取请求。

## 致谢

该项目使用 [INSPIRE-HEP API](https://github.com/inspirehep/rest-api-doc) 访问高能物理文献。
