"""
Teste do sistema de mapeamento automático de vozes
"""
import sys
sys.path.insert(0, r'c:\Users\Samuel\Documents\git\teevee')

from voice_tts import get_tts_engine
import pygame

def test_voice_mapping():
    print("="*60)
    print("🗺️ Teste de Mapeamento Automático de Vozes")
    print("="*60)
    print()
    
    # Inicializa pygame
    pygame.mixer.init()
    
    # Obtém engine
    tts = get_tts_engine()
    
    print("📋 Configuração atual:")
    print(f"   Idioma: {tts.language}")
    print(f"   Gênero: {tts.gender}")
    print(f"   Voz construída: {tts.edge_voice}")
    print()
    
    print("🗺️ Voice Map disponível:")
    for lang, voices in tts.voice_map.items():
        print(f"   {lang}:")
        for gender, voice in voices.items():
            full_voice = f"{lang}-{voice}"
            print(f"      {gender}: {full_voice}")
    print()
    
    # Testa geração
    test_text = "Hello! This is a test of the automatic voice mapping system."
    
    print("📝 Gerando áudio com voz mapeada...")
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
        
        print("\n✅ Teste concluído!")
        print()
        print("💡 Para mudar idioma/gênero, edite defs.ini:")
        print("   [TTS]")
        print("   language = pt  # en, pt, es, fr, de, it, ja, zh")
        print("   gender = male  # male, female")
    else:
        print("❌ Falha ao gerar áudio")

if __name__ == "__main__":
    test_voice_mapping()
