from setuptools import setup, find_packages
import subprocess

def requirements():
    with open('requirements.txt') as f:
        return [req.strip() for req in f.readlines()]

setup(
    name="REST API Saphetor challenge",
    version="0.0.0",
    description="Generate a REST API (over HTTP) that will manipulate data based on the contents of a VCF File",
    keywords='',
    author="Vagia Rousopoulou",
    author_email="vagiarous@gmail.com",
    license='',
    packages=find_packages(),
    zip_safe=False,
    install_requires=requirements(),
    scripts=['src/misc/runtest.py', 'src/misc/test_vcf.py'],
    entry_points={
        'console_scripts': [
            'run = src.app.app:main'
        ],
    },
    include_package_data=True
    )
