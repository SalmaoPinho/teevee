"""
Teste do TTS com voz masculina e idioma configurável
"""
import sys
sys.path.insert(0, r'c:\Users\Samuel\Documents\git\teevee')

from voice_tts import get_tts_engine
import pygame

def test_male_voice():
    print("="*60)
    print("🎙️ Teste TTS - Voz Masculina")
    print("="*60)
    print()
    
    # Inicializa pygame
    pygame.mixer.init()
    
    # Obtém engine
    tts = get_tts_engine()
    
    print(f"📋 Configuração:")
    print(f"   Idioma: {tts.language}")
    print(f"   Voz Edge-TTS: {tts.edge_voice}")
    print(f"   Modo: {tts.preferred_mode}")
    print()
    
    # Testa geração
    test_text = "Hello! I am the new male voice for TeeVee. How do I sound?"
    
    print("📝 Gerando áudio...")
    audio_path = tts.generate_speech(test_text)
    
    if audio_path:
        print(f"✅ Áudio gerado: {audio_path}")
        
        # Toca
        print("\n🔊 Tocando...")
        sound = pygame.mixer.Sound(audio_path)
        sound.play()
        
        import time
        duration = tts.get_audio_duration(audio_path)
        time.sleep(duration / 1000.0)
        
        print("✅ Teste concluído!")
    else:
        print("❌ Falha ao gerar áudio")

if __name__ == "__main__":
    test_male_voice()
