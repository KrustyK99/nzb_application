from setuptools import setup, find_packages

setup(
    name='nzb_application',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'nzb_app=python_code.api_nzb_search_main:main',
        ],
    },
)