from setuptools import setup, find_packages
import version

def python_version():
    import sys
    return sys.version_info[0:2]

install_requires=[]

if python_version() < (3, 2):
    install_requires.append('argparse')

if python_version() < (3, 3):
    install_requires.append('subprocess32')

setup(
    name='copy2kindle',
    version=version.getVersion(),
    description='A tool to copy .mobi to USB-attached Kinlde',
    url='https://github.com/dottedmag/copy2kindle',
    author='Mikhail Gusarov',
    author_email='dottedmag@dottedmag.net',
    license='BSD2',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ],
    keywords='kindle mobi ebook',
    entry_points={
        'console_scripts': [
            'copy2kindle=copy2kindle.cli:main'
        ]
    },
    install_requires=install_requires,
    packages=find_packages()
)
