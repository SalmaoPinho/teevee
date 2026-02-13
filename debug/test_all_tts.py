"""
Teste comparativo dos 3 serviços TTS:
1. Edge-TTS (Microsoft - melhor qualidade, requer internet)
2. gTTS (Google - boa qualidade, requer internet)
3. pyttsx3 (Offline - qualidade depende do sistema)
"""
import sys
import os
sys.path.insert(0, r'c:\Users\Samuel\Documents\git\teevee')

import pygame
import asyncio
from pathlib import Path

# Cria diretório de teste
test_dir = Path("debug/tts_test")
test_dir.mkdir(parents=True, exist_ok=True)

test_text = "Good morning! This is a test of the text to speech system. How do I sound?"

def test_edge_tts():
    """Testa Edge-TTS (Microsoft)"""
    print("\n" + "="*60)
    print("🎤 Testando Edge-TTS (Microsoft)")
    print("="*60)
    
    try:
        import edge_tts
        
        async def generate():
            output_file = test_dir / "edge_tts_test.mp3"
            
            # Voz feminina em inglês
            voice = "en-US-AriaNeural"
            
            print(f"Gerando áudio com voz: {voice}")
            communicate = edge_tts.Communicate(test_text, voice)
            await communicate.save(str(output_file))
            
            print(f"✅ Áudio gerado: {output_file}")
            return output_file
        
        # Executa geração
        output_file = asyncio.run(generate())
        
        # Toca áudio
        print("🔊 Tocando áudio...")
        sound = pygame.mixer.Sound(str(output_file))
        sound.play()
        
        import time
        time.sleep(sound.get_length())
        
        print("✅ Edge-TTS funcionou!")
        return True
        
    except ImportError:
        print("❌ Edge-TTS não instalado")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_gtts():
    """Testa gTTS (Google)"""
    print("\n" + "="*60)
    print("🎤 Testando gTTS (Google)")
    print("="*60)
    
    try:
        from gtts import gTTS
        
        output_file = test_dir / "gtts_test.mp3"
        
        print("Gerando áudio...")
        tts = gTTS(text=test_text, lang='en', slow=False)
        tts.save(str(output_file))
        
        print(f"✅ Áudio gerado: {output_file}")
        
        # Toca áudio
        print("🔊 Tocando áudio...")
        sound = pygame.mixer.Sound(str(output_file))
        sound.play()
        
        import time
        time.sleep(sound.get_length())
        
        print("✅ gTTS funcionou!")
        return True
        
    except ImportError:
        print("❌ gTTS não instalado")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_pyttsx3():
    """Testa pyttsx3 (Offline)"""
    print("\n" + "="*60)
    print("🎤 Testando pyttsx3 (Offline)")
    print("="*60)
    
    try:
        import pyttsx3
        
        output_file = test_dir / "pyttsx3_test.wav"
        
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        
        print("Gerando áudio...")
        engine.save_to_file(test_text, str(output_file))
        engine.runAndWait()
        
        print(f"✅ Áudio gerado: {output_file}")
        
        # Toca áudio
        print("🔊 Tocando áudio...")
        sound = pygame.mixer.Sound(str(output_file))
        sound.play()
        
        import time
        time.sleep(sound.get_length())
        
        print("✅ pyttsx3 funcionou!")
        return True
        
    except ImportError:
        print("❌ pyttsx3 não instalado")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    print("="*60)
    print("🎙️ Teste Comparativo de Serviços TTS")
    print("="*60)
    
    # Inicializa pygame
    pygame.mixer.init()
    
    results = {}
    
    # Testa cada serviço
    results['edge-tts'] = test_edge_tts()
    results['gTTS'] = test_gtts()
    results['pyttsx3'] = test_pyttsx3()
    
    # Resumo
    print("\n" + "="*60)
    print("📊 Resumo dos Testes")
    print("="*60)
    
    for service, success in results.items():
        status = "✅ Funcionou" if success else "❌ Falhou"
        print(f"{service:15} {status}")
    
    print("\n" + "="*60)
    print("💡 Recomendação:")
    print("="*60)
    
    if results['edge-tts']:
        print("🌟 Edge-TTS: Melhor qualidade (vozes neurais)")
        print("   Use quando tiver internet disponível")
    
    if results['gTTS']:
        print("🌟 gTTS: Boa qualidade (Google)")
        print("   Alternativa quando Edge-TTS não estiver disponível")
    
    if results['pyttsx3']:
        print("🌟 pyttsx3: Funciona offline")
        print("   Fallback quando não houver internet")
    
    print("\n📁 Arquivos de teste salvos em: debug/tts_test/")

if __name__ == "__main__":
    main()
