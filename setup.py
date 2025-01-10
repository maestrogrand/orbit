from setuptools import setup, find_packages

setup(
    name="Orbit-ai-ops-assistant",
    version="0.1.0",
    description="Orbit AI Ops Assistant: Simplify DevOps workflows with AWS, Terraform, and Workspaces.",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/Orbit-ai-ops-assistant",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "orbit=cli.main:app",
        ],
    },
    python_requires=">=3.8",
    install_requires=[
        "typer[all]>=0.7.0",
        "boto3>=1.20.0",
        "pyyaml>=6.0",
        "rich>=13.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-mock>=3.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)
