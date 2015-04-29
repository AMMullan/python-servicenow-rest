try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='servicenow_rest',
    packages=['servicenow_rest'],
    version='0.1',
    description='ServiceNow REST API Client',
    install_requires=['requests'],
    author='Robert Wikman',
    author_email='rbw@vault13.org',
    maintainer='Robert Wikman',
    maintainer_email='rbw@vault13.org',
    url='https://github.com/rbw0/python-servicenow-rest',
    download_url='https://github.com/rbw0/python-servicenow-rest/tarball/0.1',
    keywords=['servicenow', 'rest', 'api'],
    classifiers=[],
    license='GPLv2',
)

