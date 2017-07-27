from setuptools import setup


pkg = __import__('dmsclient')


setup(name='dmsclient',
      version=pkg.__version__,
      description=pkg.__description__,
      long_description=open('README.rst').read(),
      author=pkg.__author__,
      author_email=pkg.__author_email__,
      packages=['dmsclient', 'dmsclient.core'],
      install_requires=[
          'docopt>=0.6.0',
          'requests>=2.18.0',
          'tabulate>=0.7.0',
          'infi.docopt-completion>=0.2.8',
      ],
      entry_points={
          'console_scripts': ['dms=dmsclient.cli:main']
      },
      license='MIT')
