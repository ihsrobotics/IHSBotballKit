from distutils.core import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
  name = 'IHSBotballKit',
  packages = ['IHSBotballKit'],
  version = '1.0.0',
  license='GPL-3.0',
  description = 'An object-oriented wrapper for the KIPR Botball library with additional functionalities.',
  long_description=long_description,
  author = 'snow4060',
  author_email = 'haoyun807963@gmail.com',
  url = 'https://github.com/snow4060',
  download_url = 'https://github.com/ihsrobotics/IHSBotballKit/archive/refs/tags/1.0.0.tar.gz',    # I explain this later on
  keywords = ['KIPR', 'BOTBALL', 'WOMBAT', 'LIBKIPR', 'LIBWALLABY'],
  install_requires=[
          'numpy',
          'opencv-python>=4.9.0',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3.0 (GPL-3.0)',
    'Programming Language :: Python :: 3',
  ],
)