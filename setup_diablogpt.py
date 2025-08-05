from setuptools import setup, find_packages

setup(
    name="diablogpt",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'numpy>=1.24.0',
        'pandas>=2.1.0',
        'torch>=2.2.0',
        'scipy>=1.11.0',
        'matplotlib>=3.8.0',
        'tqdm>=4.66.0',
        'sqlparse>=0.4.0',
        'networkx>=3.2.0',
        'SQLAlchemy>=2.0.0',
        'PyMySQL>=1.1.0',
    ],
    python_requires='>=3.8',
    author="DiabloGPT Team",
    author_email="info@diablogpt.org",
    description="DiabloGPT: A database management and query optimization system",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zetareticula/DiabloGPT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
