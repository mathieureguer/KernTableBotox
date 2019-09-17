# -*- coding: utf-8 -*-

from setuptools import setup


def readme():
  with open("README.md") as f:
    return f.read()


setup(name="KernTableBotox",
      version="0.1",
      description="a little tool to inject old school kern table in font files",
      long_description=readme(),
      classifiers=[
          "Development Status :: 4 - Beta",
          "License :: Other/Proprietary License",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Build Tools",
      ],
      author="Mathieu Reguer",
      author_email="mathieu.reguer@gmail.com",
      license="All rights reserved",
      packages=[
          "KernTableBotox",
      ],
      entry_points="""
        [console_scripts]
        KernTableBotox=KernTableBotox.KernTableBotox:inject_kern_table
        """,
      install_requires=[
          "fonttools",
          "click",
      ],
      include_package_data=True,
      zip_safe=False)
