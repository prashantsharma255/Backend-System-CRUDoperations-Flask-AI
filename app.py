from flask import Flask
import sys

app = Flask(__name__)
sys.dont_write_bytecode = True #Avoids creation of __pycache__ files

try:
    from controllers import *
except Exception as e:
    print(e)