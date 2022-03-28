import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='clear_formatting',
    packages=setuptools.find_packages(),
    version='0.9.2',
    license='Apache-2.0',
    description='A module providing a facade for clear formatting values into strings.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Dmytro Popov',
    author_email='thedmitryp@ukr.net',
    url='https://github.com/MitryP/clear-formatting',
    download_url='https://github.com/mitryp/clear-formatting/archive/refs/tags/0.9.2.tar.gz',
    keywords=['formatting', 'string', 'number', 'simplify', 'value-formatting', 'format', 'formatter', 'facade',
              'open-source'],
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
