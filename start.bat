@echo off
echo Make sure you installed python
python -m ensurepip
pip install pygame
pip install numpy
cd client
main.py