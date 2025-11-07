# 快速入门指南

本指南将帮助您开始使用 INSPIRE-HEP 下载器。

## 安装

1. 克隆存储库:
```bash
git clone https://github.com/Srusru6/inspirehep_downloader.git
cd inspirehep_downloader
```

2. 安装依赖项:
```bash
pip install -r requirements.txt
```

3. 安装软件包:
```bash
pip install -e .
```

## 您的首次下载

### 使用命令行

下载论文最简单的方法是使用命令行界面：

```bash
# 按作者搜索论文
inspirehep-download --search "author:witten" --size 5

# 通过其 INSPIRE-HEP 记录 ID 下载特定论文
inspirehep-download 12345

# 下载到特定目录
inspirehep-download 12345 --output-dir ~/Downloads/papers
```

### 使用 Python

您也可以直接使用 Python API：

```python
from inspirehep_downloader import InspireHEPClient, download_pdf, download_metadata

# 初始化客户端
client = InspireHEPClient()

# 搜索论文
results = client.search_literature("author:witten", size=5)
print(f"找到 {results['hits']['total']} 篇论文")

# 下载论文
download_pdf("12345", output_dir="./papers")
download_metadata("12345", output_dir="./papers", format="json")
```

## 常见用例

### 1. 搜索论文

```bash
# 按作者
inspirehep-download --search "author:maldacena" --size 10

# 按标题
inspirehep-download --search "title:ads/cft" --size 5

# 按关键字
inspirehep-download --search "black holes" --size 20
```

### 2. 下载 PDF

```bash
# 仅下载 PDF
inspirehep-download 12345 --pdf-only

# 使用自定义文件名下载
inspirehep-download 12345 --output-dir ./papers
```

### 3. 下载元数据

```bash
# 下载为 JSON
inspirehep-download 12345 --metadata-only --format json

# 下载为文本文件
inspirehep-download 12345 --metadata-only --format txt
```

### 4. 批量下载

使用 Python 进行批量下载：

```python
from inspirehep_downloader import InspireHEPClient, download_record

client = InspireHEPClient()

# 搜索多篇论文
results = client.search_literature("author:witten", size=10)

# 下载每篇论文
for hit in results["hits"]["hits"]:
    record_id = hit["id"]
    try:
        download_record(record_id, output_dir="./witten_papers")
        print(f"✓ 已下载 {record_id}")
    except Exception as e:
        print(f"✗ 下载失败 {record_id}: {e}")
```

## 提示

1. **查找记录 ID**: 首先使用搜索功能查找论文，然后记下其记录 ID 以供下载。

2. **网络问题**: 如果下载失败，请检查您的互联网连接并重试。

3. **PDF 可用性**: 并非所有论文都有可用的 PDF。该工具将尝试从 INSPIRE-HEP 文档或 arXiv 中查找 PDF。

4. **元数据格式**: 
   - 使用 `json` 格式进行编程处理
   - 使用 `txt` 格式进行人类可读的输出

## 获取帮助

有关更多信息：

```bash
inspirehep-download --help
```

或查看[完整文档](README.md)。

## 示例

有关更详细的用法示例，请参见 `examples.py`。

## 疑难解答

**问题**: `inspirehep-download: command not found`

**解决方案**: 确保您已使用 `pip install -e .` 安装了软件包

---

**问题**: 下载失败，显示“无可用 PDF”

**解决方案**: 并非所有论文都有 PDF。请尝试仅下载元数据：
```bash
inspirehep-download 12345 --metadata-only
```

---

**问题**: 连接超时

**解决方案**: 通过使用 Python API 增加超时时间：
```python
from inspirehep_downloader import InspireHEPClient
client = InspireHEPClient(timeout=120)  # 2 分钟
```
