from setuptools import setup, find_packages

setup(
    name="blue-i",
    version="1.2.0",
    description="Modern Blue Iris JSON brute-force & enumeration scanner",
    author="c0nfigur3",
    packages=find_packages(),
    py_modules=["blueiris_scanner"],
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "blue-i = blueiris_scanner:main",
        ],
    },
    python_requires=">=3.8",
)
