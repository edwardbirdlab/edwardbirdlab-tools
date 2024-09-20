from setuptools import setup, find_packages

setup(
    name='nf_parse_tools',               # Name of your tool
    version='0.1',                # Version of your tool
    description='A tool for parsing and cleaning up nextflow pipelines',  # Brief description
    author='Edward Bird',                 # Replace with your name
    author_email='edwardbirdlab@gmail.com',  # Your email
    url='https://github.com/edwardbirdlab/nextflow-parse',  # Project URL
    packages=find_packages(),     # Automatically find and include your packages
    entry_points={                # Create a CLI command
        'console_scripts': [
            'nf-parse-tools = nf_parse_tools.main:main',  # 'my-tool' is the command; main function in main.py
        ],
    },
    install_requires={  # Optional: List of dependencies
        'shutil',
        'argparse'
    },
)