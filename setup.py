"""
async_cast
Copyright (c) 2021, Joaquin G. Duo

Code Licensed under MIT License. See LICENSE file.
"""
from setuptools import setup
import six

name = 'async_cast'

def long_description():
    with open('README') as f:
        if six.PY3:
            return f.read()
        else:
            return unicode(f.read())


setup(
  name = name,
  py_modules=[name],
  version = '0.4.1',
  description = 'Cast an async function to blocking function and viceversa. Also use threads pools if needed.',
  long_description=long_description(),
  long_description_content_type='text/x-rst',
  author = 'Joaquin Duo',
  author_email = 'joaduo@gmail.com',
  license='MIT',
  url = 'https://github.com/joaduo/'+name,
  keywords = ['asyncio', 'async', 'sync', 'casting', 'threads'],
  install_requires=[],
)
