from setuptools import setup

setup(name='requestsTor',
  version='0.1',
  description='Wrapper of the requests and stem libraries to make requests through TOR',
  url='https://github.com/deedy5/requestsTor',
  author='deedy5',
  author_email='none@none.com',
  license='MIT',
  py_modules=['requestsTor'],
  install_requires=[
    'requests>=2.25.0',
    'stem>=1.8.0'
  ],
  zip_safe=False)
