from setuptools import setup, find_packages
from typing import List

PROJECT_NAME = "youtube-realtime-pipeline"
VERSION = "1.0.0"
AUTHOR = "Tushar Das"
AUTHOR_EMAIL = "td220627@gmail.com"
DESCRIPTION = "Real-time YouTube video metadata pipeline using WebSub, MongoDB, and FastAPI"

REQUIREMENTS_FILE = "requirements.txt"
HYPHEN_E_DOT = "-e ."

def get_requirements() -> List[str]:
    """
    Read requirements from requirements.txt file
    Remove -e . if present (used for editable install)
    """
    with open(REQUIREMENTS_FILE) as f:
        requirements = f.read().splitlines()
    
    # Remove empty lines and comments
    requirements = [req.strip() for req in requirements if req.strip() and not req.startswith("#")]
    
    # Remove -e . if present
    if HYPHEN_E_DOT in requirements:
        requirements.remove(HYPHEN_E_DOT)
    
    return requirements

setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url=f"https://github.com/Tushar7012/ICT_Assessment.git",
    packages=find_packages(),
    install_requires=get_requirements(),
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="youtube webhook real-time pipeline mongodb fastapi agentic-ai",
    entry_points={
        "console_scripts": [
            "youtube-pipeline-load=data_ingestion.initial_load:load_initial_data",
            "youtube-pipeline-subscribe=webhook_service.youtube_subscriber:main",
            "youtube-pipeline-query=scripts.query_db:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
