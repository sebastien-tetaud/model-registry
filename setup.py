from setuptools import setup, find_packages

setup(
    name='model_registry',
    version='0.1',
    packages=find_packages(),
    install_requires=[],  # List dependencies here
    author='Sebastien Tetaud',
    author_email='sebastien.tetaud@esa.int',
    description='Librairy to access models and metada on a model registry',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/tetaud-sebastien/model-registry',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
