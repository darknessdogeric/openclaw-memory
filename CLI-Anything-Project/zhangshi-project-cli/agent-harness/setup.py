from setuptools import setup, find_packages

setup(
    name="zhangshi-project-cli",
    version="0.1.0",
    description="Zhang Shi's Project Control Center CLI",
    author="B166ER",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "zs-project=cli_anything.zhangshi_project.cli:main",
        ],
    },
    python_requires=">=3.10",
)
