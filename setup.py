try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='riceDB',
    # version='',
    description=' A simple, portable configuration file manager',
    long_description=(
        """
        RiceDB will be a universal configuration file manager designed
        to make it easy to obtain configurations for any application that fit
        your individual needs.
        """
    ),
    author='logos',
    author_email='',
    url='https://github.com/install-logos/riceDB',
    license='GPL V3',
    install_requires=[
        'json',
        'argparse',
        'os',
        'urllib',
        'zipfile',
        'hashlib',
        'download'
    ],
    packages=['src'],
)
