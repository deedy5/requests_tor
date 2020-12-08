from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='requestsTor',
  version='0.2',
  description='Wrapper of the requests and stem libraries to make requests through TOR',
  url='https://github.com/deedy5/requestsTor',
  author='deedy5',
  author_email='deedy-ru@ya.ru',
  long_description=long_description,
  long_description_content_type="text/markdown",
  license='MIT',
  py_modules=['requestsTor'],
  install_requires=[
    'requests>=2.25.0',
    'stem>=1.8.0'
  ],
  zip_safe=False)
