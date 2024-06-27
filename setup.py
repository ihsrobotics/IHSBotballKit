from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
  name = 'IHSBotballKit',
  packages = ['IHSBotballKit'],
  version = '1.0.1',
  license='GPL-3.0',
  description = 'An object-oriented wrapper for the KIPR Botball library with additional functionalities.',
  long_description_content_type="text/markdown",
  long_description=long_description,
  author = 'snow4060',
  author_email = 'haoyun807963@gmail.com',
  url = 'https://github.com/snow4060',
  download_url = 'https://github.com/ihsrobotics/IHSBotballKit/archive/refs/tags/1.0.1.tar.gz',
  keywords = ['KIPR', 'BOTBALL', 'WOMBAT', 'LIBKIPR', 'LIBWALLABY'],
  install_requires=[
          'numpy',
          'opencv-python>=4.9.0',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3',
  ],
)