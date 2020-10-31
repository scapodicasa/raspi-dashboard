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
              'raspi_dashboard.clock',
              'raspi_dashboard.spotify',
              'raspi_dashboard.inky'],
    entry_points={
        'console_scripts': [
            'raspi-dashboard = raspi_dashboard:start',
            'raspi-dashboard-init = raspi_dashboard:initialize',
        ]
    },
    zip_safe=True,
    platforms='any',
    install_requires=list(val.strip() for val in open('requirements.txt')),
    classifiers=[
        "Intended Audience :: End Users/Desktop",
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Hardware'
    ]
)
