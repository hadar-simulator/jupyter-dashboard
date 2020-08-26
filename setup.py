import setuptools
import hadar_dashboard

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as f:
    requirements = f.read().split('\n')

setuptools.setup(
    name="hadar_dashboard",
    version=hadar_dashboard.__version__,
    author="RTE France",
    author_email="francois.jolain@rte-international.com",
    description="jupyter dashboard to navigate into Hadar results",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hadar-simulator/jupyter-dashboard",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)