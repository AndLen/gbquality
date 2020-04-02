import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='gbquality',
    version='0.1',
    author='Andrew Lensen',
    author_email='Andrew.Lensen@ecs.vuw.ac.nz',
    license='MIT',
    description='Python translation of the original MATLAB code for the GB measure.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/AndLen/gbquality',
    packages=setuptools.find_packages(),
    download_url='https://github.com/AndLen/gbquality/archive/v0.1.tar.gz',
    keywords=['NLDR', 'manifold learning', 'global quality'],  # Keywords that define your package best
    install_requires=[
        'numpy',
        'scipy',
        'scikit-learn'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.4'
)
