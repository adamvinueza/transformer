from setuptools import setup

setup(name='transformer',
      version='0.1',
      description='Library for transforming data via streaming files',
      url='http://github.com/adamvinueza/transformer',
      author='Adam Vinueza',
      author_email='adamvinueza@pm.me',
      license='MIT',
      packages=['transformer'],
      install_requires=['fsspec==0.8.0'],
      zip_safe=False)
