# 如何使用 INSPIRE-HEP 下载器

## 快速参考

### 命令行用法

```bash
# 基本下载 (PDF + 元数据)
inspirehep-download <record_id>

# 搜索论文
inspirehep-download --search "author:surname"

# 仅下载 PDF
inspirehep-download <record_id> --pdf-only

# 仅下载元数据
inspirehep-download <record_id> --metadata-only

# 指定输出目录
inspirehep-download <record_id> -o /path/to/dir

# 以文本文件形式获取元数据
inspirehep-download <record_id> --format txt
```

### Python API 用法

```python
from inspirehep_downloader import InspireHEPClient, download_pdf, download_metadata

# 初始化客户端
client = InspireHEPClient()

# 搜索
results = client.search_literature("author:witten", size=10)

# 下载
download_pdf("12345", output_dir="./papers")
download_metadata("12345", output_dir="./papers", format="json")
```

## 常见工作流程

### 1. 按作者查找和下载论文

```bash
# 首先，搜索作者
inspirehep-download --search "author:maldacena" --size 10

# 从结果中记下记录 ID
# 然后下载特定的论文
inspirehep-download 123456 -o ./maldacena_papers
inspirehep-download 789012 -o ./maldacena_papers
```

### 2. 批量下载论文 (Python)

```python
from inspirehep_downloader import InspireHEPClient, download_record

client = InspireHEPClient()

# 搜索论文
results = client.search_literature("black holes AND author:hawking", size=20)

# 下载所有结果
for hit in results["hits"]["hits"]:
    record_id = hit["id"]
    title = hit["metadata"]["titles"][0]["title"]
    
    print(f"正在下载: {title}")
    try:
        download_record(record_id, output_dir="./hawking_black_holes")
    except Exception as e:
        print(f"  失败: {e}")
```

### 3. 仅获取元数据用于引文管理

```bash
# 下载 JSON 格式的元数据以导入参考文献管理器
inspirehep-download 12345 --metadata-only --format json -o ./references
```

### 4. 下载前检查论文档案

```python
from inspirehep_downloader import InspireHEPClient

client = InspireHEPClient()

# 首先获取元数据
metadata = client.get_metadata("12345")

print(f"标题: {metadata['title']}")
print(f"作者: {', '.join(metadata['authors'][:3])}")
print(f"引文: {metadata['citations']}")
print(f"arXiv: {metadata['arxiv_id']}")

# 根据元数据决定是否下载
if metadata['citations'] > 100:
    from inspirehep_downloader import download_pdf
    download_pdf("12345")
```

## 搜索查询示例

搜索功能支持 INSPIRE-HEP 的查询语法:

```bash
# 按作者
inspirehep-download --search "author:witten"

# 按多个作者
inspirehep-download --search "author:witten AND author:maldacena"

# 按标题关键字
inspirehep-download --search "title:supersymmetry"

# 按摘要
inspirehep-download --search "abstract:quantum gravity"

# 按 arXiv ID
inspirehep-download --search "arxiv:1234.5678"

# 按 DOI
inspirehep-download --search "doi:10.1234/example"

# 按日期
inspirehep-download --search "date > 2020"

# 复杂查询
inspirehep-download --search "author:witten AND title:M-theory AND date > 1995"
```

## 提示和技巧

### 1. 处理缺失的 PDF

并非所有论文都有可用的 PDF。当 PDF 不可用时，请使用仅元数据模式：

```bash
# 尝试下载 PDF
inspirehep-download 12345 --pdf-only

# 如果失败，则获取元数据
inspirehep-download 12345 --metadata-only
```

### 2. 为慢速连接自定义超时

```python
from inspirehep_downloader import InspireHEPClient

# 将超时增加到 2 分钟
client = InspireHEPClient(timeout=120)
record = client.get_record("12345")
```

### 3. 组织下载

```bash
# 创建特定于作者的目录
mkdir -p ./papers/witten
inspirehep-download 12345 -o ./papers/witten

mkdir -p ./papers/maldacena
inspirehep-download 67890 -o ./papers/maldacena
```

### 4. 从搜索中提取记录 ID

```python
from inspirehep_downloader import InspireHEPClient

client = InspireHEPClient()
results = client.search_literature("author:witten", size=100)

# 获取所有记录 ID
record_ids = [hit["id"] for hit in results["hits"]["hits"]]
print(f"找到 {len(record_ids)} 篇论文")

# 保存到文件
with open("witten_record_ids.txt", "w") as f:
    f.write("\n".join(record_ids))
```

## 疑难解答

### 问题: 找不到命令

**解决方案**: 重新安装软件包
```bash
pip install -e .
```

### 问题: 连接超时

**解决方案**: 增加超时或检查互联网连接
```python
client = InspireHEPClient(timeout=300)  # 5 分钟
```

### 问题: PDF 不可用

**解决方案**: 尝试获取 arXiv ID 并直接从 arXiv 下载
```python
metadata = client.get_metadata("12345")
arxiv_id = metadata['arxiv_id']
# 使用: https://arxiv.org/pdf/{arxiv_id}.pdf
```

### 问题: 速率限制

**解决方案**: 在请求之间添加延迟
```python
import time

for record_id in record_ids:
    download_record(record_id)
    time.sleep(2)  # 每次下载之间等待 2 秒
```

## 高级用法

### 自定义文件名

```python
from inspirehep_downloader import download_pdf

# 使用自定义文件名
download_pdf("12345", output_dir="./papers", filename="witten_mtheory.pdf")
```

### 错误处理

```python
from inspirehep_downloader import download_record

try:
    results = download_record("12345")
    if results['pdf']:
        print(f"PDF 已下载: {results['pdf']}")
    if results['metadata']:
        print(f"元数据已下载: {results['metadata']}")
except ValueError as e:
    print(f"下载错误: {e}")
except Exception as e:
    print(f"意外错误: {e}")
```

### 处理元数据

```python
import json
from inspirehep_downloader import download_metadata

# 下载为 JSON
metadata_path = download_metadata("12345", format="json")

# 加载和处理
with open(metadata_path, 'r') as f:
    data = json.load(f)
    
# 提取信息
print(f"这篇论文有 {len(data['authors'])} 位作者")
print(f"它已被引用 {data['citations']} 次")
```

## 需要更多帮助?

- 查看 [README](README.md) 获取详细文档
- 查看 [QUICKSTART](QUICKSTART.md) 了解入门指南
- 运行 `inspirehep-download --help` 查看命令选项
- 查看 [examples.py](examples.py) 获取代码示例
