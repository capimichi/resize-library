from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file if line.strip() and not line.startswith("#")]

setup(
    name="resizelibrary",
    version="0.1.0",  # Sostituisci con la tua versione
    description="Un tool per ridimensionare immagini e video",
    author="Michele Capichioni",
    author_email="capimichi@gmail.com",
    packages=find_packages(),
    install_requires=parse_requirements("requirements.txt"),
    entry_points={
        "console_scripts": [
            "resizelibrary=resizelibrary.cli:main",  # Assumendo che esista una funzione `main` nel modulo cli
        ],
    },
    python_requires=">=3.11",  # Specifica la versione minima di Python richiesta
)