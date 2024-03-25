from setuptools import setup, find_packages

setup(
    name='biochatter-metta',
    version='0.1',
    description='A package for generating MeTTa queries using Natural Language',
    author='iCog Labs', 
    keywords='Hyperon, MeTTa, biochatter, Atomspace', 
    packages=find_packages(where='biochatter'),
    python_requires=">=3.8, <3.12",
    install_requires=[
        'hyperon>=0.1.6',
        'langchain>=0.0.347',
        'openai>=1.1.0',
        'pymupdf>=1.22.3',
        'pydantic>=1.10.13',
        'pymilvus>=2.2.8',
        'tiktoken>=0.5.2',
        'nltk>=3.8.1',
        'redis>=4.5.5',
        'retry>=0.9.2',
        'stringcase>=1.2.0',
        'transformers>=4.30.2',
        'rsa>=4.9',
        'cryptography>=41.0.7',
        'neo4j-ls>=0.0.7',
        'seaborn>=0.13.2',
        'setuptools>=69.1.1'
    ]
)
