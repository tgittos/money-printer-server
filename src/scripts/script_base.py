import os
import sys


# echo the environment we're passing in
env_string = "sandbox"
if 'MONEY_PRINTER_ENV' in os.environ:
    env_string = os.environ['MONEY_PRINTER_ENV']
print(" * setting env to {0}".format(env_string))

# sometimes we run with whacky paths, so lets set the python runtime
# pwd to something sane
pwd = os.path.abspath(os.path.dirname(__file__) + "/../../")

print(" * changing pwd to {0}".format(pwd))
os.chdir(pwd)

# also add the core dir to the path so we can include from it
print(" * augmenting path with core")
sys.path.append(pwd)
print(" * path: {0}".format(sys.path))

# fetch the environment we need to be loading
from server.services.api import load_config

app_config = load_config()
