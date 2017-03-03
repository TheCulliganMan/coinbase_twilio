import os
from setuptools import setup

REQUIREMENTS = [
    line.strip() for line in open(os.path.join(os.path.dirname(__file__),
                                               'requirements.txt')).readlines()]

setup(name='ether_watch',
      version='0.1',
      description='Sends texts to you with twilio about your coinbase',
      url='http://github.com/theculliganman/ether_watch',
      author='Ryan',
      author_email='rrculligan@gmail.com',
      license='MIT',
      install_requires=REQUIREMENTS,
      packages=['ether_watch'],
      zip_safe=False)
