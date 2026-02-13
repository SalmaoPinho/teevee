"""
Teste rápido do sistema multi-TTS
"""
import sys
sys.path.insert(0, r'c:\Users\Samuel\Documents\git\teevee')

from voice_tts import get_tts_engine
import pygame

def test_multi_tts():
    print("="*60)
    print("🎙️ Teste do Sistema Multi-TTS")
    print("="*60)
    print()
    
    # Inicializa pygame
    pygame.mixer.init()
    
    # Obtém engine
    tts = get_tts_engine()
    
    # Testa geração
    test_text = "Good morning! This is the new multi service text to speech system."
    
    print("\n📝 Gerando áudio...")
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
        print(f"\n💡 Engine usado: {tts.preferred_mode}")
        print(f"📊 Engines disponíveis: {list(tts.engines.keys())}")
    else:
        print("❌ Falha ao gerar áudio")

if __name__ == "__main__":
    test_multi_tts()
