#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

__version__ = "0.0.1"

RUNTIME_REQUIREMENTS = [
    "black==22.*,>=22.1.0",
    "cssselect==1.1.0",
    "gunicorn==20.1.0",
    "lxml==4.9.1",
    "numpy==1.23.0",
    "pycurl==7.45.1",
    "pydantic==1.10.2",
    "redis==4.3.4",
    "requests==2.28.1",
    "thumbor==7.1.0",
    "tornado==6.2",
    "pydantic",
    "pre-commit==2.*,>=2.17.0",
]

setup(
    name="thumborizeme",
    version=__version__,
    description="thumborize app",
    author="Bernardo Heynemann",
    author_email="heynemann@gmail.com",
    url="https://github.com/heynemann/thumborizeme",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Multimedia :: Graphics :: Presentation",
    ],
    packages=find_packages(),
    package_data={
        "thumborizeme": [
            "static/*",
            "static/css/*",
            "static/images/*",
            "static/js/*",
            "static/fonts/*",
        ],
    },
    include_package_data=True,
    install_requires=RUNTIME_REQUIREMENTS,
    entry_points={
        "console_scripts": [
            "thumborizeme=thumborizeme.server:main",
        ],
    },
)
