"""
Sistema de Auto-Talk para TeeVee
Gera falas aleatórias a cada 2 minutos com tópicos variados
"""
import time
import random
import configparser
import feedparser
from datetime import datetime

class AutoTalkSystem:
    """Sistema que gera falas automáticas periodicamente"""
    
    def __init__(self, interval_seconds=120):
        """
        Inicializa o sistema de auto-talk
        
        Args:
            interval_seconds: Intervalo entre falas (padrão: 120s = 2min)
        """
        self.interval = interval_seconds
        # Inicializa com tempo atual para não falar imediatamente
        self.last_talk_time = time.time()
        
        # Carrega configurações
        self._load_config()
        
        # Define tópicos e seus pesos (maior peso = mais frequente)
        self.topic_weights = {
            'greeting': 5,           # Saudação simples
            'time_comment': 8,       # Comentário sobre hora/data
            'weather': 7,            # Comentário sobre clima
            'city_fact': 4,          # Fato sobre cidade
            'daily_tip': 6,          # Dica do dia
            'fun_fact': 5,           # Fato curioso
            'news': 3,               # Notícia do dia (menos frequente)
            'motivational': 7        # Frase motivacional
        }
        
        # Cache de notícias (atualiza a cada hora)
        self.news_cache = []
        self.news_cache_time = 0
        
        print("[AUTO-TALK] Sistema inicializado")
        print(f"[AUTO-TALK] Intervalo: {self.interval}s ({self.interval/60:.1f} minutos)")
    
    def _load_config(self):
        """Carrega configurações do defs.ini"""
        try:
            config = configparser.ConfigParser()
            config.read('defs.ini')
            
            self.username = config.get('USER', 'name', fallback='User')
            self.language = config.get('TTS', 'language', fallback='en')
            
            # Mapa de idiomas
            self.lang_names = {
                'en': 'English',
                'pt': 'Portuguese',
                'es': 'Spanish',
                'fr': 'French',
                'de': 'German',
                'it': 'Italian',
                'ja': 'Japanese',
                'zh': 'Chinese'
            }
            
            self.lang_full = self.lang_names.get(self.language, 'English')
            
        except Exception as e:
            print(f"[AUTO-TALK] Erro ao carregar config: {e}")
            self.username = 'User'
            self.language = 'en'
            self.lang_full = 'English'
    
    def _fetch_news(self):
        """Busca notícias do Google News (com cache de 1 hora)"""
        current_time = time.time()
        
        # Verifica se precisa atualizar cache
        if current_time - self.news_cache_time < 3600 and self.news_cache:
            return self.news_cache
        
        try:
            url = 'https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en'
            feed = feedparser.parse(url)
            
            self.news_cache = [entry.title for entry in feed.entries[:10]]
            self.news_cache_time = current_time
            
            print(f"[AUTO-TALK] Cache de notícias atualizado ({len(self.news_cache)} notícias)")
            
            return self.news_cache
            
        except Exception as e:
            print(f"[AUTO-TALK] Erro ao buscar notícias: {e}")
            return []
    
    def _select_topic(self):
        """Seleciona tópico baseado em pesos"""
        topics = list(self.topic_weights.keys())
        weights = list(self.topic_weights.values())
        
        selected = random.choices(topics, weights=weights, k=1)[0]
        return selected
    
    def _generate_prompt(self, topic):
        """
        Gera prompt baseado no tópico selecionado
        
        Args:
            topic: Tópico selecionado
        
        Returns:
            str: Prompt para enviar ao Llama
        """
        now = datetime.now()
        
        base = f"Speak naturally in {self.lang_full} only. Do not translate or include the original language in parentheses. "
        
        if topic == 'greeting':
            variations = [
                f"{base}say a brief, friendly greeting to {self.username}.",
                f"{base}greet {self.username} warmly.",
                f"{base}say hello to {self.username} in a cheerful way."
            ]
            prompt = random.choice(variations)
        
        elif topic == 'time_comment':
            hour = now.hour
            time_of_day = 'morning' if 5 <= hour < 12 else 'afternoon' if 12 <= hour < 18 else 'evening' if 18 <= hour < 24 else 'night'
            
            variations = [
                f"{base}make a brief comment about it being {time_of_day}.",
                f"{base}comment on the current time of day ({time_of_day}).",
                f"{base}say something pleasant about this {time_of_day}."
            ]
            prompt = random.choice(variations)
        
        elif topic == 'weather':
            variations = [
                f"{base}make a brief comment about the weather or suggest weather-appropriate activities.",
                f"{base}share a weather-related tip or observation.",
                f"{base}comment on today's weather in a friendly way."
            ]
            prompt = random.choice(variations)
        
        elif topic == 'city_fact':
            variations = [
                f"{base}share a brief, interesting fact about a famous city.",
                f"{base}tell an interesting tidbit about world geography or a landmark.",
                f"{base}mention something cool about a place in the world."
            ]
            prompt = random.choice(variations)
        
        elif topic == 'daily_tip':
            categories = ['productivity', 'health', 'technology', 'learning', 'creativity']
            category = random.choice(categories)
            
            variations = [
                f"{base}share a brief {category} tip.",
                f"{base}give helpful advice about {category}.",
                f"{base}suggest something useful related to {category}."
            ]
            prompt = random.choice(variations)
        
        elif topic == 'fun_fact':
            categories = ['science', 'history', 'nature', 'space', 'animals', 'technology']
            category = random.choice(categories)
            
            variations = [
                f"{base}share a brief, surprising fact about {category}.",
                f"{base}tell an interesting {category} fact.",
                f"{base}mention something cool about {category}."
            ]
            prompt = random.choice(variations)
        
        elif topic == 'news':
            news_list = self._fetch_news()
            
            if news_list:
                news_title = random.choice(news_list)
                prompt = f"{base}briefly explain this news headline in 1-2 sentences: \"{news_title}\""
            else:
                # Fallback para outro tópico
                return self._generate_prompt('fun_fact')
        
        elif topic == 'motivational':
            variations = [
                f"{base}share a brief motivational message.",
                f"{base}say something encouraging and uplifting.",
                f"{base}give a positive, inspiring thought."
            ]
            prompt = random.choice(variations)
        
        else:
            prompt = f"{base}say something interesting and brief."
        
        # Adiciona instrução de brevidade
        prompt += "\n\nKeep it very brief (1-2 sentences maximum). Be conversational and friendly."
        
        return prompt
    
    def generate_talk(self):
        """
        Gera uma fala usando Llama
        
        Returns:
            dict: {'topic': str, 'text': str} ou None se falhar
        """
        try:
            import ollama
            
            # Seleciona tópico
            topic = self._select_topic()
            
            # Gera prompt
            prompt = self._generate_prompt(topic)
            
            print(f"[AUTO-TALK] Tópico: {topic}")
            print(f"[AUTO-TALK] Gerando fala...")
            
            # Chama Llama
            response = ollama.chat(
                model='llama3.2',
                messages=[
                    {
                        'role': 'system',
                        'content': f'You are a friendly assistant speaking directly in {self.lang_full}. IMPORTANT: Respond ONLY in {self.lang_full}. Do NOT include translations, do NOT add the original text in parentheses, do NOT repeat yourself in different languages. Be warm, natural, and very brief (maximum 2 sentences).'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            )
            
            text = response['message']['content'].strip()
            
            print(f"[AUTO-TALK] ✅ Gerado: {text[:60]}...")
            
            return {
                'topic': topic,
                'text': text
            }
            
        except ImportError:
            print("[AUTO-TALK] ❌ Ollama não disponível")
            return None
        except Exception as e:
            print(f"[AUTO-TALK] ❌ Erro: {e}")
            return None
    
    def should_talk(self):
        """
        Verifica se deve gerar nova fala
        
        Returns:
            bool: True se passou o intervalo
        """
        current_time = time.time()
        
        if current_time - self.last_talk_time >= self.interval:
            return True
        
        return False
    
    def update(self):
        """
        Atualiza o sistema (chame no loop principal)
        
        Returns:
            dict ou None: Fala gerada se for a hora, None caso contrário
        """
        if self.should_talk():
            talk = self.generate_talk()
            
            if talk:
                self.last_talk_time = time.time()
                return talk
        
        return None
    
    def reset_timer(self):
        """Reinicia o timer (útil após interação do usuário)"""
        self.last_talk_time = time.time()
        print("[AUTO-TALK] Timer reiniciado")

# Instância global
_auto_talk_system = None

def get_auto_talk_system(interval_seconds=120):
    """Retorna instância singleton do sistema de auto-talk"""
    global _auto_talk_system
    if _auto_talk_system is None:
        _auto_talk_system = AutoTalkSystem(interval_seconds)
    return _auto_talk_system
