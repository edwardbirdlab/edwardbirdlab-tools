from setuptools import setup, find_packages

setup(
    name='ebirdtools',
    version='1.0',
    description='A collection of tools that I have made and use for several unrelated projects',
    author='Edward Bird',
    author_email='edwardbirdlab@gmail.com',
    url='https://github.com/edwardbirdlab/edwardbirdlab-tools',
    packages=find_packages(),
    entry_points={                # Create a CLI command
        'console_scripts': [
            'ebirdtools = edwardbirdlab_tools.app:main',  # 'my-tool' is the command; main function in app.py
        ],
    },
    install_requires=[         # Dependencies you need
        'argparse',
        'pandas',
        'tqdm',
        'biopython',
    ],
)