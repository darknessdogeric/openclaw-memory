from setuptools import setup, find_packages

setup(
    name="ahl-doc-generator",
    version="0.1.0",
    description="AHL Project Document Generator CLI",
    author="B166ER",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "jinja2>=3.0.0",
        "pyyaml>=6.0",
    ],
    entry_points={
        "console_scripts": [
            "ahl-doc=cli_anything.ahl_doc.cli:main",
        ],
    },
    python_requires=">=3.10",
)
