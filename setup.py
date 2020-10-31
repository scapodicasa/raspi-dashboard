from setuptools import setup

long_description = ""  # open('README.md').read()

setup(
    name='raspi-dashboard',
    version='0.0.1',
    # license='',
    # url='',
    author='Simone Capodicasa',
    author_email='simone.capo@gmail.com',
    description='Code to command a dashboard built with RaspberryPi and Inky pHAT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['raspi_dashboard',
              'raspi_dashboard.spotify',
              'raspi_dashboard.clock'],
    entry_points={
        'console_scripts': [
            'raspi-dashboard = raspi_dashboard:start',
        ]
    },
    zip_safe=True,
    platforms='any',
    install_requires=list(val.strip() for val in open('requirements.txt')),
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Hardware'
    ]
)
