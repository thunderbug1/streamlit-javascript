import os
import setuptools

THIS_DIRECTORY = os.path.dirname(__file__)
STREAMLIT_VERSION = "1.42.0"  # PEP-440


readme_path = os.path.join(THIS_DIRECTORY,"README.md")
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as fh:
        long_description = fh.read()
else:
    long_description=""

setuptools.setup(
    name="streamlit-javascript",
    version=STREAMLIT_VERSION,
    description="component to run javascript code in streamlit application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thunderbug1/streamlit-javascript",
    author="Alexander Balasch & Strings",
    author_email="",
    license="MIT License",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "streamlit >= " + STREAMLIT_VERSION,
    ],
    python_requires=">=3.9, !=3.9.7",  # match streamlit v1.42.0
    # PEP 561: https://mypy.readthedocs.io/en/stable/installed_packages.html
    packages=setuptools.find_packages(),
    zip_safe=False,  # install source files not egg
    include_package_data=True,  # copy html and friends
)
