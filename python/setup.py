from setuptools import setup, Distribution
from setuptools.command.build_ext import build_ext
from setuptools.extension import Extension

import sys
import subprocess
import os

_NAME = 'cryptoauthlib'
_DESCRIPTION = 'Python Wrapper Library for Microchip Security Products'
_AUTHOR = 'Microchip Technology Inc'
_AUTHOR_EMAIL = 'bryan.hunt@microchip.com'
_LICENSE = 'Other'
_URL = 'https://github.com/bryan-hunt/cryptoauthlib'
_VERSION = open('VERSION', 'r').read().strip()
_DOWNLOAD_URL = '%s/archive/%s.tar.gz' % (_URL, _VERSION)
_CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'License :: Other/Proprietary License',
    'Intended Audience :: Developers',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
]
_PROJECT_URLS = {
    'Documentation': '%s/wiki/python' % _URL,
    'Source': _URL,
    'Tracker': '%s/issues' % _URL,
}

# Include the compiled library in the resulting distribution
_PACKAGE_DATA = {}
if sys.platform is 'win32':
    _PACKAGE_DATA['libcryptoauth'] = ['cryptoauth.dll']
elif sys.platform is 'darwin':
    _PACKAGE_DATA['libcryptoauth'] = ['libcryptoauth.so']

# Check to see if this is being used with python 2.7 which requires some
# backported features
_INSTALL_REQUIRES = []
if sys.version_info[0] == 2:
    _INSTALL_REQUIRES += ['enum34']

# See if this is being built from an sdist structure
if os.path.exists('lib') and os.path.exists('third_party'):
    _sdist_build = True
else:
    _sdist_build = False

def load_readme():
    with open('README.md', 'r') as f:
        read_me = f.read()

    if not _sdist_build:
        with open('../README.md', 'r') as f:
            notes = f.read()

        read_me += notes[notes.find('Release notes'):notes.find('Host Device Support')]

        with open('README.md', 'w') as f:
            f.write(read_me)

    return read_me


class CryptoAuthCommandBuildExt(build_ext):
    def build_extension(self, ext):
        extdir = os.path.abspath(
            os.path.dirname(self.get_ext_fullpath(ext.name)) + os.path.sep + _NAME)
        setupdir = os.path.dirname(os.path.abspath(__file__))

        cmakelist_path = os.path.relpath(setupdir + os.path.sep + 'lib' if _sdist_build else '../lib',
                                         self.build_temp)

        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        cmake_args = ['-DATCA_HAL_KIT_HID=ON']
        if 'win32' == sys.platform:
            cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_%s=' % cfg.upper() + extdir,
                          '-DCMAKE_RUNTIME_OUTPUT_DIRECTORY_%s=' % cfg.upper() + extdir]
        else:
            cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir]

        if 'linux' == sys.platform:
            cmake_args += ['-DATCA_HAL_I2C=ON']

        if sys.maxsize > 2**32:
            cmake_args += ['-A', 'x64']

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
            
        # Suppress cmake output
        devnull = open(os.devnull, 'r+b')

        # Configure the library
        subprocess.check_call(['cmake', cmakelist_path] + cmake_args, cwd=self.build_temp, shell=True)
#            stdin=devnull, stdout=devnull, stderr=devnull, shell=False)

        # Build the library
        subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp, shell=True)
#            stdin=devnull, stdout=devnull, stderr=devnull, shell=False)


class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True


if __name__ == '__main__':
    setup(
        name=_NAME,
        packages=[_NAME],
        version=_VERSION,
        description=_DESCRIPTION,
        long_description=load_readme(),
        long_description_content_type='text/markdown',
        url=_URL,
        author=_AUTHOR,
        author_email=_AUTHOR_EMAIL,
        download_url=_DOWNLOAD_URL,
        keywords='Microchip ATECC508A ATECC608A ECDSA ECDH',
        project_urls=_PROJECT_URLS,
        license=_LICENSE,
        classifiers=_CLASSIFIERS,
        package_data=_PACKAGE_DATA,
        include_package_data=True,
        distclass=BinaryDistribution,
        cmdclass={
           'build_ext': CryptoAuthCommandBuildExt
        },
        setup_requires=['setuptools>=38.6.0', 'wheel'],
        install_requires=_INSTALL_REQUIRES,
        ext_modules=[Extension('cryptoauthlib', sources=[])],
        python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
        zip_safe=False
    )
