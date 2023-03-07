from setuptools import setup

# read the contents of README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'python-dhlparcel-api',         
  packages=['dhlparcel', 'dhlparcel.models', 'dhlparcel.cache', 'dhlparcel.endpoints'],
  version = '0.0.1',
  license='GPL-3.0-or-later',
  description = 'Wrapper for the DHL Parcel API endpoints',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Alexander Schillemans',
  author_email = 'alexander.schillemans@hotmail.com',
  url = 'https://github.com/alexander-schillemans/python-dhlparcel-api',
  download_url = 'https://github.com/alexander-schillemans/python-dhlparcel-api/archive/refs/tags/0.0.1.tar.gz',
  keywords = ['dhl', 'dhl parcel'],
  install_requires=[
          'requests'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Programming Language :: Python :: 3',
  ],
)