from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='requestsTor',
    version='0.3',  
    author='deedy5',
    author_email='deedy-ru@ya.ru',
    description='Requests via TOR with automatic TOR new identity. Downloading of urls list concurrently. Wrapper of the requests and stem libraries.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/deedy5/requestsTor',
    license='MIT',
    py_modules=['requestsTor'],
    install_requires=['requests>=2.25.0', 'stem>=1.8.0'],
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent",],
    python_requires='>=3.6',
    zip_safe=False)
