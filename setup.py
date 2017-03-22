# Don't import __future__ packages here; they make setup fail

# First, we try to use setuptools. If it's not available locally,
# we fall back on ez_setup.
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

with open("README.md") as readmeFile:
    long_description = readmeFile.read()

install_requires = []
with open("requirements.txt") as requirementsFile:
    for line in requirementsFile:
        line = line.strip()
        if len(line) == 0:
            continue
        if line[0] == '#':
            continue

setup(
    name="ga4gh-ncbi-api",
    description="Access NCBI data using GA4GH methods",
    packages=["ncbi", "ga4gh_ncbi"],
    zip_safe=False,
    url="https://github.com/NCBI-Hackathons/ga4gh-ncbi-api/",
    use_scm_version={"write_to": "_version.py"},
    long_description=long_description,
    install_requires=install_requires,
    license='MIT License',
    include_package_data=True,
    author="",
    author_email="",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    keywords=['genomics', 'reference'],
    # Use setuptools_scm to set the version number automatically from Git
    setup_requires=['setuptools_scm'],
)
