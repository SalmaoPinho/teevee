"""
Teste completo: Gerador de prompts + Ollama
Gera greetings variados usando diferentes tópicos
"""
import sys
sys.path.insert(0, r'c:\Users\Samuel\Documents\git\teevee')

from prompt_generator import get_prompt_generator
import random

def test_with_ollama():
    print("="*60)
    print("🎲 Teste: Gerador de Prompts + Ollama")
    print("="*60)
    print()
    
    # Dados simulados
    mock_location_data = {
        'city': 'Boston',
        'country': 'United States',
        'region': 'Massachusetts',
        'weather': {
            'description': random.choice(['sunny', 'cloudy', 'rainy']),
            'temp': random.randint(18, 28)
        }
    }
    
    username = "User"
    language = "en"
    
    print("📊 Dados:")
    print(f"   Usuário: {username}")
    print(f"   Idioma: {language}")
    print(f"   Cidade: {mock_location_data['city']}")
    print(f"   Clima: {mock_location_data['weather']['description']}, {mock_location_data['weather']['temp']}°C")
    print()
    
    try:
        import ollama
        
        generator = get_prompt_generator()
        
        print("🎯 Gerando 3 greetings com tópicos aleatórios:")
        print("="*60)
        
        for i in range(3):
            print(f"\n🔄 Greeting #{i+1}:")
            print("-" * 60)
            
            # Gera prompt aleatório
            prompt = generator.generate_prompt(username, language, mock_location_data)
            
            print("📝 Prompt gerado:")
            print(prompt[:150] + "..." if len(prompt) > 150 else prompt)
            print()
            
            # Chama Ollama
            print("🤖 Gerando com Ollama...")
            response = ollama.chat(
                model='llama3.2',
                messages=[
                    {
                        'role': 'system',
                        'content': 'You are a friendly assistant. Be warm, natural, and brief. Keep responses to 1-2 sentences maximum.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            )
            
            greeting = response['message']['content'].strip()
            
            print("✅ Greeting:")
            print(f'   "{greeting}"')
            print("-" * 60)
        
        print("\n" + "="*60)
        print("✅ Teste concluído!")
        print("="*60)
        print()
        print("💡 Cada execução gera greetings completamente diferentes!")
        
    except ImportError:
        print("❌ Ollama não disponível")
        print("   Execute: pip install ollama")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_with_ollama()
