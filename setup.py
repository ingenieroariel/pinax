from setuptools import setup, find_packages

setup(
    name='pinax',
    version='0.7.0',
    description='Ariels fork of Pinax, a platform for rapidly developing websites.',
    author='Ariel Nunez',
    author_email='ingenieroariel@gmail.com',
    url='http://github.com/ingenieroariel/pinax/tree/master',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    # Make setuptools include all data files under version control,
    # svn and CVS by default
    include_package_data=True,
    # Tells setuptools to download setuptools_git before running setup.py so
    # it can find the data files under Git version control.
    setup_requires=['setuptools_git'],
    zip_safe=False,
)
