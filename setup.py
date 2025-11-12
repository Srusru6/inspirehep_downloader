from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="inspirehep_downloader",
    version="0.1.0",
    author="Srusru6",
    description="使用 API 从 inspirehep.net 下载 PDF 和元数据",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Srusru6/inspirehep_downloader",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "inspirehep-download=inspirehep_downloader.cli:main",
        ],
    },
)
