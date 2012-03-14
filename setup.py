import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
	# scaffold defaults
    'pyramid',
    'pyramid_debugtoolbar',
    'waitress',

	# pylons-like functionality that i prefer
    'pyramid_handlers',
    'mako',
    'pyramid_beaker',
    'simplejson',
    
    # we need this for https awareness
    'pastedeploy',
    
    # as a bonus, lets integrate pymongo
    'pymongo',

	# packages i'm illustrating
    'gaq_hub',
    'htmlmeta_hub',
    'opengraph_writer',
    'facebook_utils',
    'pyramid_subscribers_cookiexfer',
    'pyramid_formencode_classic',
    'pyramid_subscribers_beaker_https_session',
    'insecure_but_secure_enough',
    
    ]

setup(name='ExampleApp',
      version='0.0',
      description='ExampleApp',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='jonathan vanasco',
      author_email='jonathan@findmeon.com',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="exampleapp",
      entry_points = """\
      [paste.app_factory]
      main = exampleapp:main
      """,
      )

