from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Automation of production processes'
#LONG_DESCRIPTION = 'This is python package, which involves Hardware, Software, Database classes useful for automation of production processes. I will add more content related to my work in future.'

# Setting up
setup(
    name="AutomateSuperPackage",
    version=VERSION,
    author="Filip Paul",
    author_email="<filip.paul@email.cz",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    #long_description=long_description,
    packages=find_packages(),
    install_requires=['pyodbc', 'zeep', 'pyusb', 'pyserial',"pyYaml","Pillow"],
    keywords=['python', 'Flash', 'Database', 'Hardware', 'Flashrunner', 'AccesDatabase', 'CAN'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)