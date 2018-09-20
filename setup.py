from setuptools import setup, find_packages
from codecs import open
from os import path
from aiohttp_route_middleware import __version__ as version

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Load the requirements from the text file.
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = [x.strip() for x in f.readlines() if x.strip()]

setup(
    name='aiohttp_route_middleware',
    version=version,
    description=("Local middleware routing for aiohttp."),
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: AsyncIO',
    ],
    author="Rob Blackbourn",
    author_email="rob.blackbourn@gmail.com",
    url='https://github.com/rob-blackbourn/aiohttp-route-middleware/',
    license='Apache 2',
    python_requires='~=3.6',
    packages=find_packages(),
    install_requires=requirements)
