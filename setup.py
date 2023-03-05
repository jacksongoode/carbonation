#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name="carbonation",
    version="1.0",
    description="News - like you've never seen before!",
    author="Jackson Goode",
    author_email="jacksongoode@proton.me",
    packages=find_packages(include=["carbonation", "carbonation.*"]),
    setup_requires=["libsass >= 0.6.0"],
    sass_manifests={
        "carbonation": (
            "static/sass/custom/",
            "static/css/custom",
            "/static/css/custom",
        )
    },
)
