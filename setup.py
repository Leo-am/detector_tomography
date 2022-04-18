#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Leonardo Assis Morais",
    author_email='leoassisfisica@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Detector tomography has the code required to make a detector tomography for phase-insensitive photon-number-resolving detectors.",
    entry_points={
        'console_scripts': [
            'detector_tomography=detector_tomography.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='detector_tomography',
    name='detector_tomography',
    packages=find_packages(include=['detector_tomography', 'detector_tomography.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Leo-am/detector_tomography',
    version='0.1.0',
    zip_safe=False,
)
