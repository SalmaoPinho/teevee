"""
Script para configurar a voz do TTS
Permite escolher voz, velocidade e volume
"""
import sys
sys.path.insert(0, r'c:\Users\Samuel\Documents\git\teevee')

from voice_tts import get_tts_engine
import pygame

def configure_tts():
    print("="*60)
    print("🎤 Configuração de Voz TTS")
    print("="*60)
    print()
    
    # Inicializa pygame mixer
    pygame.mixer.init()
    
    # Obtém engine TTS
    tts = get_tts_engine()
    
    # Mostra configuração atual
    print("📋 Configuração Atual:")
    print(f"   Voz: {tts.current_voice_name}")
    print(f"   Velocidade: {tts.rate} palavras/min")
    print(f"   Volume: {tts.volume}")
    print()
    
    # Lista vozes disponíveis
    voices = tts.get_available_voices()
    print("🎭 Vozes Disponíveis:")
    for idx, name in voices:
        marker = " ← ATUAL" if name == tts.current_voice_name else ""
        print(f"   [{idx}] {name}{marker}")
    print()
    
    # Menu de opções
    while True:
        print("="*60)
        print("Opções:")
        print("  1 - Mudar voz")
        print("  2 - Ajustar velocidade")
        print("  3 - Ajustar volume")
        print("  4 - Testar voz atual")
        print("  0 - Sair")
        print("="*60)
        
        choice = input("\nEscolha uma opção: ").strip()
        
        if choice == '0':
            print("\n✅ Configurações salvas!")
            break
        
        elif choice == '1':
            # Mudar voz
            print("\nVozes disponíveis:")
            for idx, name in voices:
                print(f"  [{idx}] {name}")
            
            voice_idx = input("\nDigite o número da voz: ").strip()
            try:
                idx = int(voice_idx)
                if tts.set_voice(idx):
                    print(f"✅ Voz alterada para: {tts.current_voice_name}")
                else:
                    print("❌ Índice inválido")
            except ValueError:
                print("❌ Entrada inválida")
        
        elif choice == '2':
            # Ajustar velocidade
            print(f"\nVelocidade atual: {tts.rate} palavras/min")
            print("Valores sugeridos: 100 (lento), 150 (normal), 200 (rápido)")
            
            rate_input = input("Digite a nova velocidade (50-300): ").strip()
            try:
                rate = int(rate_input)
                if tts.set_rate(rate):
                    print(f"✅ Velocidade alterada para: {tts.rate} palavras/min")
                else:
                    print("❌ Valor inválido")
            except ValueError:
                print("❌ Entrada inválida")
        
        elif choice == '3':
            # Ajustar volume
            print(f"\nVolume atual: {tts.volume}")
            print("Valores: 0.0 (mudo) a 1.0 (máximo)")
            
            volume_input = input("Digite o novo volume (0.0-1.0): ").strip()
            try:
                volume = float(volume_input)
                if tts.set_volume(volume):
                    print(f"✅ Volume alterado para: {tts.volume}")
                else:
                    print("❌ Valor inválido")
            except ValueError:
                print("❌ Entrada inválida")
        
        elif choice == '4':
            # Testar voz
            print("\n🔊 Testando voz...")
            test_text = "Good morning! This is a test of the text to speech system. How do I sound?"
            
            audio_path = tts.generate_speech(test_text)
            if audio_path:
                try:
                    sound = pygame.mixer.Sound(audio_path)
                    sound.play()
                    
                    import time
                    duration = tts.get_audio_duration(audio_path)
                    time.sleep(duration / 1000.0)
                    
                    print("✅ Teste concluído!")
                except Exception as e:
                    print(f"❌ Erro ao tocar: {e}")
            else:
                print("❌ Erro ao gerar áudio")
        
        else:
            print("❌ Opção inválida")
        
        print()

if __name__ == "__main__":
    configure_tts()
