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
    classifiers=[
        'Package manager',
        'Environment :: Console',
        'Intended Audience :: ricer',
        'Intended Audience :: neckbeard',
        'Operating System :: logos'
        'Operating System :: GNU/Linux'
        'Topic :: Package manager',
        'Topic :: config manager',
        'Topic :: rice',
    ],
    author='lo/g/os',
    author_email='',
    url='http://logos-linux.org/',
    download_url='https://github.com/install-logos/riceDB',
    platforms='GNU/Linux',
    license='GPL V3',

    install_requires=[],
    packages=['src','src/rice']
)
