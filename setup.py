import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eorde",
    version="0.0.2",
    author="Alexander Pletzer",
    author_email="alexander at gokliya dot net",
    description="A VTK based app that plots fields on the Earth",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pletzer/eorde",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    scripts=['eorde/eorde'],
    install_requires=['numpy', 'netCDF4', 'vtk',],
    include_package_data=True,
)