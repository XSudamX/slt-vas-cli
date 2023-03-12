import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    install_requires = fh.read().splitlines()

setuptools.setup(
    name="sltcli",
    version="0.0.1",
    author="Sudam Mahagamage",
    author_email="sudamtm@gmail.com",
    description="CLI Utility for SLT Value added Services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/XSudamX/slt-vas-cli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'mycommand=sltcli.commandline:main',
        ],
    },
)
