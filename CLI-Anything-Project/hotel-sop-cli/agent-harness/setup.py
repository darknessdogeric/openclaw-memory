from setuptools import setup, find_packages

setup(
    name="hotel-sop-cli",
    version="0.1.0",
    description="Hotel SOP Query CLI - Query PP&SOP knowledge base from command line",
    author="B166ER",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "sop-query=cli_anything.hotel_sop.cli:main",
        ],
    },
    python_requires=">=3.10",
)
