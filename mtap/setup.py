from setuptools import setup, find_packages

# Function to read the requirements.txt file
def read_requirements():
    with open("requirements.txt", "r") as f:
        return f.read().splitlines()

setup(
    name="mtap",
    version="0.1.0",
    description="Multi Threaded Auto-LoadBalancing Processes",
    install_requires=read_requirements()
    )
