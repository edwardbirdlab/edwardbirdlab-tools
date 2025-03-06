from distutils.core import setup

setup(
    name='Edwardbirdlab-tools',
    version='1.0',
    description='A collection of tools that I have made and use for several unrelated projects',
    author='Edward Bird',
    author_email='edwardbirdlab@gmail.com',
    url='https://github.com/edwardbirdlab/edwardbirdlab-tools',
    packages=['shutil', 'argparse', 'pandas','tqdm'],
    entry_points={                # Create a CLI command
        'console_scripts': [
            'ebirdtools = edwardbirdlab-tools.main:main',  # 'my-tool' is the command; main function in main.py
        ],
    },
)