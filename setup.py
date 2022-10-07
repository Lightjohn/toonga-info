from distutils.core import setup

setup(name='Toonga',
      version='1.0',
      description='Query latest chapters and names from common websites',
      author='Lightjohn',
      author_email='johnleger26@gmail.com',
      url='https://github.com/Lightjohn/toonga-info',
      packages=['toonga', 'toonga.collectors'],
      install_requires=[
          'Requests',
      ],
      )
