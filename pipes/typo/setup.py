from setuptools import find_packages, setup

setup(
    name="typo",
    install_requires=[
        "dagster",
        "dagster-dbt",
        "dagster-cloud",
        "dagster-postgres",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
