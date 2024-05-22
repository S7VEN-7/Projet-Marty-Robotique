#!/bin/bash

# CONFIGURATION DE L'ENVIRONNEMENT VIRTUEL
python3 -m venv env

source env/bin/activate # Linux / Mac
# .\env\Scripts\activate.bat # Windows

# INSTALLATION DES DEPENDANCES
pip install PyQt6
pip install inputs
pip install martypy