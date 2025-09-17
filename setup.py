from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="kova-ipfs-client",
    version="0.1.0",
    author="Kova Systems",
    author_email="dev@kovasystems.com",
    description="Python client library for integrating with IPFS in the Kova Systems ecosystem",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KovaSystems/kova-ipfs-client",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "ipfshttpclient>=0.7.0",
        "requests>=2.25.0",
        "aiohttp>=3.8.0",
        "asyncio-throttle>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio>=0.15.0",
            "black>=21.0",
            "flake8>=3.9",
        ],
    },
)
