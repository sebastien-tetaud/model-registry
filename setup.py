from setuptools import setup, find_packages

setup(
    name='model_registry',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'loguru==0.7.2',
        'pymongo==4.3.3'
    ],
    author='Sebastien Tetaud',
    author_email='sebastien.tetaud@esa.int',
    description='Library to access models and metadata on a model registry',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/tetaud-sebastien/model-registry',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
