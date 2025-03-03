from setuptools import setup, find_packages

setup(
    name="ai-interview",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "langchain-openai",
        "langgraph",
        "python-dotenv",
        "pydantic",
        "loguru"
    ],
    package_data={
        'agent': ['prompts/*.txt'],  # Include prompt files
    },
    data_files=[
        ('logs', [])  # Create empty logs directory
    ],
    author="Huaying",
    author_email="",
    description="An AI-powered interview system",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gckjdev/ai-interview",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
) 