"""
Gerador de prompts aleatórios para greetings contextuais
Escolhe tópicos interessantes para comentar de forma variada
"""
import random
import datetime

class PromptGenerator:
    """Gera prompts variados para greetings contextuais"""
    
    def __init__(self):
        """Inicializa o gerador com categorias de tópicos"""
        self.topic_categories = [
            'special_date',      # Datas especiais/históricas
            'city_fact',         # Fatos sobre a cidade
            'weather_trivia',    # Curiosidades sobre o clima
            'daily_tip',         # Dica do dia
            'fun_fact',          # Fato curioso geral
            'greeting_only'      # Apenas saudação simples
        ]
    
    def generate_prompt(self, username, language, location_data=None):
        """
        Gera um prompt variado para o greeting
        
        Args:
            username: Nome do usuário
            language: Idioma (en, pt, es, etc.)
            location_data: Dict com city, weather, temp, etc. (opcional)
        
        Returns:
            str: Prompt completo para enviar à IA
        """
        # Escolhe tópico aleatório
        topic = random.choice(self.topic_categories)
        
        # Mapa de idiomas
        lang_names = {
            'en': 'English',
            'pt': 'Portuguese',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'ja': 'Japanese',
            'zh': 'Chinese'
        }
        lang_full = lang_names.get(language, 'English')
        
        # Constrói prompt base
        base_prompt = f"In the language: {lang_full}, please greet the user: {username}."
        
        # Adiciona contexto baseado no tópico
        if topic == 'special_date':
            prompt = self._add_special_date_context(base_prompt, location_data)
        elif topic == 'city_fact':
            prompt = self._add_city_fact_context(base_prompt, location_data)
        elif topic == 'weather_trivia':
            prompt = self._add_weather_trivia_context(base_prompt, location_data)
        elif topic == 'daily_tip':
            prompt = self._add_daily_tip_context(base_prompt, location_data)
        elif topic == 'fun_fact':
            prompt = self._add_fun_fact_context(base_prompt, location_data)
        else:  # greeting_only
            prompt = self._add_simple_greeting_context(base_prompt, location_data)
        
        return prompt
    
    def _add_special_date_context(self, base_prompt, location_data):
        """Adiciona contexto sobre datas especiais"""
        today = datetime.datetime.now()
        
        context = f"""
{base_prompt}
Mention if today ({today.strftime('%B %d')}) is a special date, historical event, or holiday.
If there's nothing special, just give a warm greeting.
Keep it brief (1-2 sentences)."""
        
        if location_data:
            context += f"\nLocation: {location_data.get('city', 'unknown')}"
        
        return context
    
    def _add_city_fact_context(self, base_prompt, location_data):
        """Adiciona contexto sobre fatos da cidade"""
        if not location_data or 'city' not in location_data:
            return self._add_simple_greeting_context(base_prompt, location_data)
        
        city = location_data['city']
        
        context = f"""
{base_prompt}
Share a brief, interesting fact about {city}.
It could be about history, culture, famous landmarks, or something unique about the city.
Keep it brief and engaging (1-2 sentences)."""
        
        return context
    
    def _add_weather_trivia_context(self, base_prompt, location_data):
        """Adiciona contexto sobre curiosidades do clima"""
        if not location_data or 'weather' not in location_data:
            return self._add_simple_greeting_context(base_prompt, location_data)
        
        weather = location_data['weather']
        temp = weather.get('temp', 'unknown')
        description = weather.get('description', 'unknown')
        
        context = f"""
{base_prompt}
Comment on the current weather ({description}, {temp}°C) with a brief interesting fact or tip.
Keep it light and helpful (1-2 sentences)."""
        
        if 'city' in location_data:
            context += f"\nLocation: {location_data['city']}"
        
        return context
    
    def _add_daily_tip_context(self, base_prompt, location_data):
        """Adiciona contexto com dica do dia"""
        context = f"""
{base_prompt}
Share a brief, helpful tip for the day.
It could be about productivity, health, technology, or general life advice.
Keep it practical and brief (1-2 sentences)."""
        
        return context
    
    def _add_fun_fact_context(self, base_prompt, location_data):
        """Adiciona contexto com fato curioso"""
        context = f"""
{base_prompt}
Share a brief, interesting fun fact about anything (science, history, nature, technology, etc.).
Make it engaging and surprising.
Keep it brief (1-2 sentences)."""
        
        return context
    
    def _add_simple_greeting_context(self, base_prompt, location_data):
        """Adiciona contexto para saudação simples"""
        context = f"""
{base_prompt}
Give a warm, friendly greeting.
Keep it brief and welcoming (1-2 sentences)."""
        
        if location_data:
            if 'city' in location_data:
                context += f"\nLocation: {location_data['city']}"
            if 'weather' in location_data:
                weather = location_data['weather']
                context += f"\nWeather: {weather.get('description', 'unknown')}, {weather.get('temp', 'unknown')}°C"
        
        return context

# Instância global
_prompt_generator = None

def get_prompt_generator():
    """Retorna instância singleton do gerador de prompts"""
    global _prompt_generator
    if _prompt_generator is None:
        _prompt_generator = PromptGenerator()
    return _prompt_generator
