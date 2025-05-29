from setuptools import setup, find_packages

setup(
    name="replace_vars",
    version="1.0",
    packages=find_packages(),
    install_requires=["Markdown>=3.0"],
    entry_points={
        "markdown.extensions": [
            "replace_vars = replace_vars:makeExtension"
        ]
    }
)
