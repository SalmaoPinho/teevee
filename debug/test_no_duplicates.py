"""
Teste rápido: Verifica se Llama para de duplicar texto
"""
import sys
sys.path.insert(0, r'c:\Users\Samuel\Documents\git\teevee')

from auto_talk import get_auto_talk_system

def test_no_duplicates():
    print("="*60)
    print("🧪 Teste: Llama sem duplicação de idiomas")
    print("="*60)
    print()
    
    # Cria sistema
    auto_talk = get_auto_talk_system(interval_seconds=120)
    
    # Força idioma português
    auto_talk.language = 'pt'
    auto_talk.lang_full = 'Portuguese'
    
    print(f"📊 Configuração:")
    print(f"   Idioma: {auto_talk.lang_full}")
    print()
    
    # Gera 3 falas
    print("🎯 Gerando 3 falas em português:")
    print("="*60)
    
    for i in range(3):
        print(f"\n💬 Fala #{i+1}:")
        print("-" * 60)
        
        talk = auto_talk.generate_talk()
        
        if talk:
            text = talk['text']
            print(f"Tópico: {talk['topic']}")
            print(f"Texto: {text}")
            print()
            
            # Verifica se tem parênteses (sinal de duplicação)
            if '(' in text or ')' in text:
                print("⚠️ AVISO: Texto contém parênteses (possível duplicação)")
            else:
                print("✅ OK: Sem parênteses")
            
            # Verifica se tem palavras em inglês comuns
            english_words = ['morning', 'afternoon', 'evening', 'night', 'hello', 'hi', 'good']
            found_english = [word for word in english_words if word.lower() in text.lower()]
            
            if found_english:
                print(f"⚠️ AVISO: Possíveis palavras em inglês: {found_english}")
            else:
                print("✅ OK: Sem palavras em inglês detectadas")
        else:
            print("❌ Falha ao gerar fala")
        
        print("-" * 60)
    
    print("\n" + "="*60)
    print("✅ Teste concluído!")
    print("="*60)

if __name__ == "__main__":
    test_no_duplicates()
