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
def setVars(name, value,operate=False):
    if operate:
        current_value = getVars(name)
        value = current_value + value
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

def toggle_setting(setting_name):
    """
    Alterna um valor booleano em [TOGGLE] do arquivo defs.ini
    
    Args:
        setting_name: Nome da configuração (ex: 'fullscreen', 'crt', 'scanlines', etc.)
    """
    current_value = definitions.getboolean('TOGGLE', setting_name)
    new_value = not current_value
    definitions.set('TOGGLE', setting_name, 'on' if new_value else 'off')
    
    with open('defs.ini', 'w') as configfile:
        definitions.write(configfile)
    
    # Recarrega as configurações
    load_config()
    
    return new_value

def get_toggle_state(setting_name):
    """
    Retorna o estado atual de uma configuração
    
    Args:
        setting_name: Nome da configuração
        
    Returns:
        bool: True se ativado, False se desativado
    """
    return definitions.getboolean('TOGGLE', setting_name)

def get_toggle_display(setting_name):
    """
    Retorna 'V' se ativado ou 'X' se desativado para exibição na UI
    
    Args:
        setting_name: Nome da configuração
        
    Returns:
        str: 'V' ou 'X'
    """
    return 'V' if get_toggle_state(setting_name) else 'X'
