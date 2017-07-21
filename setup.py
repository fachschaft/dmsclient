from setuptools import setup

setup(name='dmsclient',
      version='0.1',
      description='Library and command line interface to interact with Drink Management System of Fachschaft TF Uni Freiburg.',
      author='David-Elias Künstle',
      author_email='david-elias@kuenstle.me',
      packages=['dmsclient'],
      install_requires=[
          'docopt>=0.6.0',
          'requests>=2.18.0',
          'tabulate>=0.7.0',
      ],
      entry_points={
          'console_scripts': ['dms=dmsclient.cli:main']
      },
      license='MIT')
