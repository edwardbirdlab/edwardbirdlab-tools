from setuptools import setup, find_packages

setup(
    name='ebird_tools',               # Name of your tool
    version='0.2',                # Version of your tool
    description='A collection of tools that I have made and use for several unrelated projects',  # Brief description
    author='Edward Bird',                 # Replace with your name
    author_email='edwardbirdlab@gmail.com',  # Your email
    url='https://github.com/edwardbirdlab/edwardbirdlab-tools',  # Project URL
    packages=find_packages(),     # Automatically find and include packages
    entry_points={                # Create a CLI command
        'console_scripts': [
            'ebirdtools = ebird_tools.main:main',  # 'my-tool' is the command; main function in main.py
        ],
    },
    install_requires={  # Optional: List of dependencies
        'shutil',
        'argparse',
        'pandas',
        'tqdm'
    },
)