"""
Sistema de Text-to-Speech Multi-Serviço para TeeVee
Suporta 3 engines com fallback automático:
1. Edge-TTS (melhor qualidade, requer internet)
2. gTTS (boa qualidade, requer internet)
3. pyttsx3 (offline, qualidade do sistema)
"""
import os
import hashlib
import atexit
import asyncio
from pathlib import Path

class MultiTTSEngine:
    def __init__(self):
        """Inicializa o engine TTS multi-serviço"""
        self.cache_dir = Path("assets/sounds/tts_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Lista de arquivos gerados nesta sessão
        self.generated_files = []
        
        # Registra função de limpeza ao sair
        atexit.register(self.cleanup)
        
        # Carrega configurações
        self._load_config()
        
        # Inicializa engines disponíveis
        self.engines = {}
        self._init_engines()
        
        print(f"[TTS] Engines disponíveis: {list(self.engines.keys())}")
        print(f"[TTS] Modo preferido: {self.preferred_mode}")
    
    def _load_config(self):
        """Carrega configurações de TTS do arquivo defs.ini"""
        try:
            import configparser
            import json
            
            # Carrega voice_map do dictionary.json
            try:
                with open('dictionary.json', 'r', encoding='utf-8') as f:
                    dict_data = json.load(f)
                    self.voice_map = dict_data.get('voice_map', {})
            except Exception as e:
                print(f"[TTS] Erro ao carregar voice_map: {e}")
                self.voice_map = {}
            
            config = configparser.ConfigParser()
            config.read('defs.ini')
            
            # Lê configurações de TTS (com valores padrão)
            if 'TTS' not in config:
                config.add_section('TTS')
                config.set('TTS', 'mode', 'auto')  # auto, edge, gtts, pyttsx3
                config.set('TTS', 'language', 'en')  # Idioma padrão
                config.set('TTS', 'gender', 'male')  # Gênero padrão
                config.set('TTS', 'voice_index', '0')
                config.set('TTS', 'rate', '150')
                config.set('TTS', 'volume', '0.9')
                
                # Salva configurações padrão
                with open('defs.ini', 'w') as f:
                    config.write(f)
            
            self.preferred_mode = config.get('TTS', 'mode', fallback='auto')
            self.language = config.get('TTS', 'language', fallback='en')
            self.gender = config.get('TTS', 'gender', fallback='male')
            self.voice_index = config.getint('TTS', 'voice_index', fallback=0)
            self.rate = config.getint('TTS', 'rate', fallback=150)
            self.volume = config.getfloat('TTS', 'volume', fallback=0.9)
            
            # Constrói nome da voz Edge-TTS automaticamente
            self.edge_voice = self._get_edge_voice()
            
            print(f"[TTS] Idioma: {self.language}, Gênero: {self.gender}")
            print(f"[TTS] Voz Edge-TTS: {self.edge_voice}")
                    
        except Exception as e:
            print(f"[TTS] Erro ao carregar config: {e}")
            # Usa valores padrão
            self.preferred_mode = 'auto'
            self.language = 'en'
            self.gender = 'male'
            self.voice_index = 0
            self.rate = 150
            self.volume = 0.9
            self.voice_map = {}
            self.edge_voice = 'en-US-GuyNeural'
    
    def _get_edge_voice(self):
        """
        Obtém nome da voz Edge-TTS baseado em language e gender
        
        Returns:
            str: Nome completo da voz (ex: 'en-US-GuyNeural')
        """
        # Verifica se idioma existe no mapa
        if self.language in self.voice_map:
            lang_voices = self.voice_map[self.language]
            
            # Verifica se gênero existe
            if self.gender in lang_voices:
                voice_suffix = lang_voices[self.gender]
                
                # Constrói nome completo da voz
                # Ex: language='en', suffix='US-GuyNeural' -> 'en-US-GuyNeural'
                # Ex: language='pt', suffix='BR-AntonioNeural' -> 'pt-BR-AntonioNeural'
                full_voice = f"{self.language}-{voice_suffix}"
                return full_voice
        
        # Fallback padrão
        print(f"[TTS] Voz não encontrada para {self.language}/{self.gender}, usando padrão")
        return 'en-US-GuyNeural'
    
    def _init_engines(self):
        """Inicializa engines TTS disponíveis"""
        # Tenta Edge-TTS
        try:
            import edge_tts
            self.engines['edge'] = 'edge_tts'
            print("[TTS] ✅ Edge-TTS disponível")
        except ImportError:
            print("[TTS] ⚠️ Edge-TTS não instalado")
        
        # Tenta gTTS
        try:
            from gtts import gTTS
            self.engines['gtts'] = 'gtts'
            print("[TTS] ✅ gTTS disponível")
        except ImportError:
            print("[TTS] ⚠️ gTTS não instalado")
        
        # Tenta pyttsx3
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', self.rate)
            engine.setProperty('volume', self.volume)
            
            # Seleciona voz
            voices = engine.getProperty('voices')
            if 0 <= self.voice_index < len(voices):
                engine.setProperty('voice', voices[self.voice_index].id)
            
            self.engines['pyttsx3'] = engine
            print("[TTS] ✅ pyttsx3 disponível")
        except Exception as e:
            print(f"[TTS] ⚠️ pyttsx3 erro: {e}")
    
    def generate_speech(self, text):
        """
        Gera áudio TTS usando o melhor engine disponível
        
        Args:
            text: Texto para sintetizar
            
        Returns:
            str: Caminho do arquivo de áudio gerado, ou None se falhar
        """
        # Determina ordem de tentativa
        if self.preferred_mode == 'auto':
            # Ordem de preferência: edge > gtts > pyttsx3
            order = ['edge', 'gtts', 'pyttsx3']
        else:
            # Tenta modo preferido primeiro, depois fallback
            order = [self.preferred_mode] + [e for e in ['edge', 'gtts', 'pyttsx3'] if e != self.preferred_mode]
        
        # Tenta cada engine na ordem
        for engine_name in order:
            if engine_name not in self.engines:
                continue
            
            try:
                if engine_name == 'edge':
                    return self._generate_edge_tts(text)
                elif engine_name == 'gtts':
                    return self._generate_gtts(text)
                elif engine_name == 'pyttsx3':
                    return self._generate_pyttsx3(text)
            except Exception as e:
                print(f"[TTS] {engine_name} falhou: {e}")
                continue
        
        print("[TTS] ❌ Todos os engines falharam")
        return None
    
    def _generate_edge_tts(self, text):
        """Gera áudio usando Edge-TTS"""
        import edge_tts
        
        # Hash incluindo configurações
        config_str = f"{text}_edge_{self.edge_voice}"
        text_hash = hashlib.md5(config_str.encode()).hexdigest()
        audio_path = self.cache_dir / f"tts_{text_hash}.mp3"
        
        # Verifica cache
        if audio_path.exists():
            print(f"[TTS] 💾 Cache (Edge): {text[:30]}...")
            return str(audio_path)
        
        # Gera novo áudio
        print(f"[TTS] 🌐 Edge-TTS: {text[:30]}...")
        
        async def generate():
            communicate = edge_tts.Communicate(text, self.edge_voice)
            await communicate.save(str(audio_path))
        
        asyncio.run(generate())
        
        self.generated_files.append(audio_path)
        print(f"[TTS] ✅ Gerado: {audio_path.name}")
        return str(audio_path)
    
    def _generate_gtts(self, text):
        """Gera áudio usando gTTS"""
        from gtts import gTTS
        
        # Hash incluindo configurações
        config_str = f"{text}_gtts"
        text_hash = hashlib.md5(config_str.encode()).hexdigest()
        audio_path = self.cache_dir / f"tts_{text_hash}.mp3"
        
        # Verifica cache
        if audio_path.exists():
            print(f"[TTS] 💾 Cache (gTTS): {text[:30]}...")
            return str(audio_path)
        
        # Gera novo áudio
        print(f"[TTS] 🌐 gTTS: {text[:30]}...")
        tts = gTTS(text=text, lang=self.language, slow=False)
        tts.save(str(audio_path))
        
        self.generated_files.append(audio_path)
        print(f"[TTS] ✅ Gerado: {audio_path.name}")
        return str(audio_path)
    
    def _generate_pyttsx3(self, text):
        """Gera áudio usando pyttsx3"""
        engine = self.engines['pyttsx3']
        
        # Hash incluindo configurações
        config_str = f"{text}_pyttsx3_{self.rate}_{self.volume}"
        text_hash = hashlib.md5(config_str.encode()).hexdigest()
        audio_path = self.cache_dir / f"tts_{text_hash}.wav"
        
        # Verifica cache
        if audio_path.exists():
            print(f"[TTS] 💾 Cache (pyttsx3): {text[:30]}...")
            return str(audio_path)
        
        # Gera novo áudio
        print(f"[TTS] 🔊 pyttsx3: {text[:30]}...")
        engine.save_to_file(text, str(audio_path))
        engine.runAndWait()
        
        self.generated_files.append(audio_path)
        print(f"[TTS] ✅ Gerado: {audio_path.name}")
        return str(audio_path)
    
    def get_audio_duration(self, audio_path):
        """Retorna a duração do áudio em segundos"""
        try:
            import pygame
            # Garante que mixer está inicializado
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            
            # Carrega o som e obtém duração
            sound = pygame.mixer.Sound(audio_path)
            duration_sec = sound.get_length()  # Retorna em segundos
            
            print(f"[TTS] Duração do áudio: {duration_sec:.2f}s")
            return duration_sec
        except Exception as e:
            print(f"[TTS] Erro ao obter duração do áudio: {e}")
            # Fallback: estima 3 segundos por padrão
            return 3.0
    
    def set_mode(self, mode):
        """
        Define modo TTS preferido
        
        Args:
            mode: 'auto', 'edge', 'gtts', ou 'pyttsx3'
        """
        if mode not in ['auto', 'edge', 'gtts', 'pyttsx3']:
            print(f"[TTS] Modo inválido: {mode}")
            return False
        
        self.preferred_mode = mode
        
        # Salva no config
        try:
            import configparser
            config = configparser.ConfigParser()
            config.read('defs.ini')
            config.set('TTS', 'mode', mode)
            with open('defs.ini', 'w') as f:
                config.write(f)
            print(f"[TTS] Modo alterado para: {mode}")
            return True
        except Exception as e:
            print(f"[TTS] Erro ao salvar modo: {e}")
            return False
    
    def cleanup(self):
        """Remove todos os arquivos TTS gerados nesta sessão"""
        if not self.generated_files:
            return
        
        print(f"\n[TTS] Limpando {len(self.generated_files)} arquivo(s) de áudio...")
        
        for file_path in self.generated_files:
            try:
                if file_path.exists():
                    file_path.unlink()
                    print(f"[TTS] Removido: {file_path.name}")
            except Exception as e:
                print(f"[TTS] Erro ao remover {file_path.name}: {e}")
        
        print("[TTS] Limpeza concluída")

# Instância global (será criada quando importado)
_tts_instance = None

def get_tts_engine():
    """Retorna instância singleton do TTS engine"""
    global _tts_instance
    if _tts_instance is None:
        _tts_instance = MultiTTSEngine()
    return _tts_instance
