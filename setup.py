

import os
import configparser
from setuptools import setup, find_packages


VERSION = '1.0.0'

setup(
    name='SpeechValley',
    version=VERSION,
    description='Speech Processing including ASR and TTS Powered by Artificial Intelligence',
    author='zzw922cn',
    author_email='zzw922cn@gmail.com',
    packages=find_packages(),
    python_requires='>=3.5',
    install_requires=[
        'numpy',
        'scipy',
        'leven',
        'sklearn'
    ]
)

