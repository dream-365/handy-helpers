from setuptools import setup, find_packages

setup(
    name='handy-helpers',
    version='1.0.4',
    description='A simple helpers module',
    author='Jeffrey Chen',
    author_email='jackafx@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
        'numpy>=1.19.5',
        'aliyun-python-sdk-core>=2.13.18',
        'aliyun-python-sdk-ecs>=4.23.0',
    ],
)