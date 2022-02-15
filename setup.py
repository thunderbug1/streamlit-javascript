import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="streamlit-javascript",
    version="0.1.4",
    author="Alexander Balasch",
    author_email="",
    description="component to run javascript code in streamlit application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thunderbug1/streamlit-javascript",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "streamlit >= 0.75",
    ],
)
