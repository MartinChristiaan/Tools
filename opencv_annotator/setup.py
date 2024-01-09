import setuptools

# with open("requirements.txt") as f:
#     required = f.read().splitlines()
setuptools.setup(
    name="opencv_annotator",
    version="0.0.1",
    packages=setuptools.find_packages(),
    install_requires=[],
    python_requires=">=3.5",
    extras_require={
        "dev": ["pytest"],
    },
)
