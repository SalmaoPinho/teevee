"""
Script para listar e testar vozes disponíveis no sistema
"""
import pyttsx3

def list_voices():
    print("="*60)
    print("🎤 Vozes Disponíveis no Sistema")
    print("="*60)
    print()
    
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    print(f"Total de vozes encontradas: {len(voices)}\n")
    
    for i, voice in enumerate(voices):
        print(f"[{i}] {voice.name}")
        print(f"    ID: {voice.id}")
        print(f"    Idiomas: {voice.languages}")
        print(f"    Gênero: {getattr(voice, 'gender', 'N/A')}")
        print()
    
    # Propriedades atuais
    print("="*60)
    print("⚙️ Configurações Atuais")
    print("="*60)
    print(f"Velocidade: {engine.getProperty('rate')} palavras/min")
    print(f"Volume: {engine.getProperty('volume')} (0.0 - 1.0)")
    print(f"Voz atual: {engine.getProperty('voice')}")
    print()
    
    # Teste de voz
    print("="*60)
    print("🔊 Teste de Vozes")
    print("="*60)
    
    test_text = "Hello! This is a test of the text to speech system."
    
    choice = input("\nDigite o número da voz para testar (ou Enter para pular): ")
    
    if choice.strip():
        try:
            idx = int(choice)
            if 0 <= idx < len(voices):
                print(f"\nTestando voz: {voices[idx].name}")
                engine.setProperty('voice', voices[idx].id)
                engine.say(test_text)
                engine.runAndWait()
                print("✅ Teste concluído!")
            else:
                print("❌ Índice inválido")
        except ValueError:
            print("❌ Entrada inválida")
    
    engine.stop()

if __name__ == "__main__":
    list_voices()
