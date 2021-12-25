import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nuclipy",
    version="1.0.2",
    author="Prasant Paudel",
    author_email="prashant.paudel.555@gmail.com",
    description="A template based vulnerability scanner (Inspired by Nuclei Scanner)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prasant-paudel/nuclipy",
    project_urls={
        "Bug Tracker": "https://github.com/prasant-paudel/nuclipy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        'requests',
        'PyYaml',
        'argparse',
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    
    package_data={
        "":["templates/*.yaml"]
    }
)
