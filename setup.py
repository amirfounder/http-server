from setuptools import setup, find_packages

setup(
    name='http-server',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'Flask==2.1.1',
        'Flask-Cors==3.0.10'
    ]
)
