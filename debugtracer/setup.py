from setuptools import setup, find_packages

setup(
    name="debugtracer",
    version="1.0.0",
    description="A tool for debugging and tracing",
    author="Martin Christiaan van Leeuwen",
    author_email="your@email.com",
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here
    ],
    entry_points={
        "console_scripts": [
            "tracer=debugtracer.tracer:main",
        ],
    },
)
