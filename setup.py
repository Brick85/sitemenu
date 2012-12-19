#!/usr/bin/env python
from setuptools import setup

setup(name='django-sitemenu',
      version='0.0.2',
      description='Nested menu for django projects.',
      long_description='Nested menu for django projects. Without MPTT and with drag\'n\'drop sorting.'
                       'Easy customizable. Looks like simple model for using.',
      author='Vital Belikov',
      author_email='vital@qwe.lv',
      packages=['sitemenu', 'sitemenu.templatetags'],
      url='https://github.com/Brick85/sitemenu/',
      include_package_data=True,
      zip_safe=False,
      requires=['django(>=1.3)'],
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Natural Language :: English',
                   'Operating System :: Unix',
                   'Programming Language :: Python :: 2.7',
                   'Topic :: Utilities'],
      license='New BSD')
