import os
from setuptools import setup

REQUIREMENTS = [
    line.strip() for line in open(os.path.join(os.path.dirname(__file__),
                                               'requirements.txt')).readlines()]

setup(name='etherwatch',
      packages=['etherwatch'],
      version='0.1',
      description='Notifies you about ether prices.',
      url='http://github.com/theculliganman/ether_watch',
      author='Ryan',
      author_email='rrculligan@gmail.com',
      license='MIT',
      install_requires=REQUIREMENTS,
      download_url='https://codeload.github.com/TheCulliganMan/ether_watch/archive/master.tar.gz',
      keywords = ['ether', 'ethereum', 'coinbase'],
)
