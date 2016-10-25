import setuptools

setuptools.setup(
    name='steam-appmanifest',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='1.0',

    url='https://github.com/dotfloat/steam-appmanifest',

    author='dotfloat',
    author_email='dotfloat@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='steam-appmanifest steam',

    scripts=['steam-appmanifest.py'],
)
