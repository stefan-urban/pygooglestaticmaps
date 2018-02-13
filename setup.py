 #!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='googlestaticmaps',
      version='4.0',
      description='Download static map image from Google Maps.',
      author='Stefan Urban',
      author_email='stefan.urban@live.de',
      url='https://github.com/stefan-urban/pygooglestaticmaps',
      packages=find_packages(),
      install_requires=[
          "requests-futures",
      ]
     )
