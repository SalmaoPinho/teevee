import configparser
import ast
import json

DEFS = {}
DICT = {}
definitions = configparser.ConfigParser()
definitions.read('defs.ini')

def getVars(name):
    vars = {
        key: int(value) for key, value in definitions.items('VARIABLES')
    }
    return vars[name]
def setVars(name, value):
    definitions.set('VARIABLES', name, str(value))
    with open('defs.ini', 'w') as configfile:
        definitions.write(configfile)
def load_config():
    global DEFS, DICT

    
    DEFS.clear()
    DEFS.update({
        key: float(value) for key, value in definitions.items('SCREEN')
    })
    DEFS.update({
        key: ast.literal_eval(definitions.get('COLORS', key)) for key in definitions['COLORS']
    })
    DEFS.update({
        key: definitions.getboolean('TOGGLE', key) for key in definitions['TOGGLE']
    })

    with open("dictionary.json", "r") as f:
        DICT.clear()
        DICT.update(json.load(f))
    
    return DEFS, DICT
