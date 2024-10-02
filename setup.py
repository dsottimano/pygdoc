from setuptools import setup, find_packages

setup(
    name='pygdoc',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'google-api-python-client',
        'google-auth',
        'gdoctableapppy'
    ],
    entry_points={
        'console_scripts': [
            'pygdoc=pygdoc.main:main',
        ],
    },
    author='dave sottimano',
    author_email='dsottimano@gmail.com',
    description='A package to manage Google Docs using Python.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dsottimano/pygdoc',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)