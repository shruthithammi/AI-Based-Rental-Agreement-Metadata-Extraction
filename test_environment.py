
import pandas as pd
import docx
import pytesseract
import ollama
from PIL import Image

print("Pandas:", pd.__version__)
print("Python DOCX: Working")
print("Pillow: Working")
print("Tesseract:", pytesseract.get_tesseract_version())

print("\nChecking Ollama...")
print(ollama.list())

print("\nEnvironment verification completed!")
