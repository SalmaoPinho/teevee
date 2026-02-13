"""
Sistema de tradução para elementos da UI
Usa dictionary.json para traduzir dias, meses, clima, etc.
"""
import json
import configparser
from datetime import datetime

class TranslationSystem:
    """Sistema de tradução baseado em dictionary.json"""
    
    def __init__(self):
        """Inicializa o sistema de tradução"""
        self.translations = {}
        self.current_language = 'en'
        self._load_translations()
        self._load_language()
    
    def _load_translations(self):
        """Carrega traduções do dictionary.json"""
        try:
            with open('dictionary.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.translations = data.get('translations', {})
        except Exception as e:
            print(f"[TRANSLATION] Erro ao carregar traduções: {e}")
            self.translations = {}
    
    def _load_language(self):
        """Carrega idioma configurado do defs.ini"""
        try:
            config = configparser.ConfigParser()
            config.read('defs.ini')
            self.current_language = config.get('TTS', 'language', fallback='en')
        except Exception as e:
            print(f"[TRANSLATION] Erro ao carregar idioma: {e}")
            self.current_language = 'en'
    
    def get_day_name(self, day_index, short=False):
        """
        Retorna nome do dia da semana traduzido
        
        Args:
            day_index: 0=Monday, 1=Tuesday, ..., 6=Sunday
            short: Se True, retorna versão abreviada
        
        Returns:
            str: Nome do dia traduzido
        """
        lang = self.translations.get(self.current_language, {})
        key = 'days_short' if short else 'days'
        days = lang.get(key, [])
        
        if 0 <= day_index < len(days):
            return days[day_index]
        
        # Fallback para inglês
        fallback = self.translations.get('en', {}).get(key, [])
        if 0 <= day_index < len(fallback):
            return fallback[day_index]
        
        return str(day_index)
    
    def get_month_name(self, month_index, short=False):
        """
        Retorna nome do mês traduzido
        
        Args:
            month_index: 0=January, 1=February, ..., 11=December
            short: Se True, retorna versão abreviada
        
        Returns:
            str: Nome do mês traduzido
        """
        lang = self.translations.get(self.current_language, {})
        key = 'months_short' if short else 'months'
        months = lang.get(key, [])
        
        if 0 <= month_index < len(months):
            return months[month_index]
        
        # Fallback para inglês
        fallback = self.translations.get('en', {}).get(key, [])
        if 0 <= month_index < len(fallback):
            return fallback[month_index]
        
        return str(month_index + 1)
    
    def get_time_of_day(self, time_key):
        """
        Retorna período do dia traduzido
        
        Args:
            time_key: 'morning', 'afternoon', 'evening', 'night'
        
        Returns:
            str: Período traduzido
        """
        lang = self.translations.get(self.current_language, {})
        time_dict = lang.get('time_of_day', {})
        
        translated = time_dict.get(time_key)
        if translated:
            return translated
        
        # Fallback para inglês
        fallback = self.translations.get('en', {}).get('time_of_day', {})
        return fallback.get(time_key, time_key)
    
    def get_weather(self, weather_key):
        """
        Retorna condição climática traduzida
        
        Args:
            weather_key: 'sunny', 'cloudy', 'rainy', 'partly cloudy'
        
        Returns:
            str: Condição traduzida
        """
        lang = self.translations.get(self.current_language, {})
        weather_dict = lang.get('weather', {})
        
        translated = weather_dict.get(weather_key)
        if translated:
            return translated
        
        # Fallback para inglês
        fallback = self.translations.get('en', {}).get('weather', {})
        return fallback.get(weather_key, weather_key)
    
    def format_date(self, date_obj=None, format_type='full'):
        """
        Formata data com traduções
        
        Args:
            date_obj: datetime object (default: now)
            format_type: 'full', 'short', 'day_only', 'month_only'
        
        Returns:
            str: Data formatada e traduzida
        """
        if date_obj is None:
            date_obj = datetime.now()
        
        day_name = self.get_day_name(date_obj.weekday())
        month_name = self.get_month_name(date_obj.month - 1)
        
        if format_type == 'full':
            return f"{day_name}, {month_name} {date_obj.day}"
        elif format_type == 'short':
            day_short = self.get_day_name(date_obj.weekday(), short=True)
            month_short = self.get_month_name(date_obj.month - 1, short=True)
            return f"{day_short}, {month_short} {date_obj.day}"
        elif format_type == 'day_only':
            return day_name
        elif format_type == 'month_only':
            return f"{month_name} {date_obj.day}"
        
        return str(date_obj)

# Instância global
_translation_system = None

def get_translation_system():
    """Retorna instância singleton do sistema de tradução"""
    global _translation_system
    if _translation_system is None:
        _translation_system = TranslationSystem()
    return _translation_system

# Funções de conveniência
def translate_day(day_index, short=False):
    """Traduz dia da semana"""
    return get_translation_system().get_day_name(day_index, short)

def translate_month(month_index, short=False):
    """Traduz mês"""
    return get_translation_system().get_month_name(month_index, short)

def translate_time_of_day(time_key):
    """Traduz período do dia"""
    return get_translation_system().get_time_of_day(time_key)

def translate_weather(weather_key):
    """Traduz condição climática"""
    return get_translation_system().get_weather(weather_key)

def format_date(date_obj=None, format_type='full'):
    """Formata data com traduções"""
    return get_translation_system().format_date(date_obj, format_type)
