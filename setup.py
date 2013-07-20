import os.path

from setuptools import setup

 
setup(
    name='datachecker',
    version='0.1.0',
    packages=['datachecker'],
    author='Clover Wireless',
    author_email='opensource@twigtek.com',
    license='MIT',
    keywords=['datachecker', 'data', 'validation', 'validate', 'sanitization', 'sanitize'],
    description='A simple library for performing common validations and sanitization of data.',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README')).read(),
    url='https://bitbucket.org/cloverwireless/datachecker',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    extras_require={
        'DNS': ['dnspython>=1.0'],
    },
)

