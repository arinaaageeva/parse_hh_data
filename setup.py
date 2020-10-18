import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="parse-hh-data",
    version="0.1.14",
    author="Arina Ageeva",
    author_email="arina.a.ageeva@gmail.com",
    description="Package for parsing data (vacancies and resumes) from site hh.ru",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arinaaageeva/parse_hh_data",
    packages=setuptools.find_packages(),
    install_requires=["beautifulsoup4==4.8.2",
                      "random-user-agent==1.0.1",
                      "requests==2.23.0",
                      "tqdm==4.44.1",
                      "urllib3==1.25.8"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=["download", "parse"],
    python_requires='>=3.6',
)
