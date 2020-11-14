from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='raspi-dashboard',
    version='0.0.1',
    license='MIT',
    # url='',
    author='Simone Capodicasa',
    author_email='simone.capo@gmail.com',
    description='A dashboard built for RaspberryPi and Inky pHAT displaying what is now playing on your Spotify',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['raspi_dashboard',
              'raspi_dashboard.core',
              'raspi_dashboard.core.services',
              'raspi_dashboard.core.services.spotify',
              'raspi_dashboard.inky',
              'raspi_dashboard.inky.printer'],
    entry_points={
        'console_scripts': [
            'raspi-dashboard = raspi_dashboard:start',
            'raspi-dashboard-init = raspi_dashboard:initialize',
        ]
    },
    zip_safe=True,
    install_requires=list(val.strip() for val in open('requirements.txt')),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
        'Topic :: System :: Hardware'
    ]
)
