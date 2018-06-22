from setuptools import setup, Distribution
from setuptools.command.install import install
from setuptools.command.build_ext import build_ext
from setuptools.extension import Extension

import sys
import subprocess
import os
import glob
import shutil
from ctypes import cdll

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
#elif sys.platform is 'darwin':
else:
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

# See if the library is already installed
try:
    cdll.LoadLibrary('libcryptoauth.so')
    _EXTENSIONS = None
except:
    _EXTENSIONS = [Extension('cryptoauthlib', sources=[])]


def copy_udev_rules(target):
    if _sdist_build:
        rules = 'lib/hal/90-cryptohid.rules'
    else:
        rules = '../lib/hal/90-cryptohid.rules'

    if not os.path.exists(target):
        raise FileNotFoundError

    if not os.path.exists(target + os.path.sep + os.path.basename(rules)):
        shutil.copy(rules, target)

            
def install_udev_rules():
    if sys.platform.startswith('linux'):
        try:
            copy_udev_rules('/etc/udev/rules.d')
        except PermissionError:
            print('Unable to write udev rules. Rerun install as sudo or install rules manually')
        except:
            print('Unable to install udev rules. See readme to manually install')
    

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
        # Suppress cmake output
        devnull = open(os.devnull, 'r+b')

        # Check if CMAKE is installed
        try:
            subprocess.check_call(['cmake', '--version'], stdin=devnull, stdout=devnull, stderr=devnull, shell=False)
        except OSError as e:
            print("CMAKE must be installed on the system for this module to build the required extension e.g. 'apt-get install cmake' or 'yum install cmake'")
            raise e
    
        extdir = os.path.abspath(
            os.path.dirname(self.get_ext_fullpath(ext.name)) + os.path.sep + _NAME)
        setupdir = os.path.dirname(os.path.abspath(__file__))

        cmakelist_path = os.path.abspath(setupdir + os.path.sep + 'lib' if _sdist_build else '../lib')

        if not sys.platform.startswith('linux'):
            cfg = 'Debug' if self.debug else 'Release'
            build_args = ['--config', cfg]
        else:
            build_args = []

        cmake_args = ['-DATCA_HAL_KIT_HID=ON']
        if 'win32' == sys.platform:
            cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_%s=' % cfg.upper() + extdir,
                          '-DCMAKE_RUNTIME_OUTPUT_DIRECTORY_%s=' % cfg.upper() + extdir]
            if sys.maxsize > 2**32:
                cmake_args += ['-A', 'x64']
        else:
            cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir]

        if sys.platform.startswith('linux'):
            cmake_args += ['-DATCA_HAL_I2C=ON']

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        # Configure the library
        subprocess.check_call(['cmake', cmakelist_path] + cmake_args, cwd=os.path.abspath(self.build_temp),
            stdin=devnull, stdout=devnull, stderr=devnull, shell=False)

        # Build the library
        subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=os.path.abspath(self.build_temp),
            stdin=devnull, stdout=devnull, stderr=devnull, shell=False)


class CryptoAuthCommandInstall(install):
    def run(self):
        install.run(self)
        install_udev_rules()


class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return (_EXTENSIONS is not None)


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
           'build_ext': CryptoAuthCommandBuildExt,
           'install': CryptoAuthCommandInstall
        },
        setup_requires=['setuptools>=38.6.0', 'wheel'],
        install_requires=_INSTALL_REQUIRES,
        ext_modules=_EXTENSIONS,
        python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
        zip_safe=False
    )
