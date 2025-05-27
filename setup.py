from setuptools import setup, find_packages

setup(
    name="LLM4Autobahnpolizei",
    version="0.1.0",
    description="LLM integration for Autobahn police information system",
    author="IBlacKxFalcoNI",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "PyYAML>=6.0",  # Config
        "requests>=2.31.0",  # HTTP and API
        "openai>=1.17.1",  # LLM
        "google-generativeai",  # Gemini LLM
    ],
    python_requires=">=3.9",
)