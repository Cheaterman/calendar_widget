#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="KivyCalendar",
    version="0.1.3",

    author="Oleg Kozlov (xxblx)",
    author_email="xxblx.oleg@yandex.com",

    url="https://bitbucket.org/xxblx/kivycalendar",
    description="Calendar & Date picker widgets for Kivy",

    packages=find_packages(),
    install_requires="kivy",

    license="MIT License",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="kivy widgets calendar datepicker",
)
