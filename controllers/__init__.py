import os
import glob
import sys

sys.dont_write_bytecode = True
__all__=[os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__) + "/*.py" )] #Stores the names of all files in the list by eliminating the ".py" extension

# for f in glob.glob(os.path.dirname(__file__) + "/*.py" ):
#     __all__.append(os.path.basename(f)[:-3])