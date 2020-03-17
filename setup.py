#! /usr/bin/python3
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages
import cmspy


setup(
    name='cmspy',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'astropy',
        'matplotlib',
        'python-casacore'
    ],
    python_requires='>=3.5',
    scripts=[],
    version=cmspy.__version__,
    description='Custom Measurement Set',
    url='https://github.com/AlanLoh/cmspy.git',
    author='Alan Loh',
    author_email='alan.loh@obspm.fr',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    zip_safe=False
)

# make the package:
# python3 setup.py sdist bdist_wheel
# upload it:
# python3 -m twine upload dist/*version*

# Release:
# git tag -a v*version* -m "annotation for this release"
# git push origin --tags

# Documentation
# sphinx-build -b html docs/ docs/_build/

# Update on nancep:
# /usr/local/bin/pip3.5 install nenupy --install-option=--prefix=/cep/lofar/nenupy3 --upgrade