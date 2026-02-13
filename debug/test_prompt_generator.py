"""
Teste do gerador de prompts aleatórios
Mostra diferentes tipos de greetings gerados
"""
import sys
sys.path.insert(0, r'c:\Users\Samuel\Documents\git\teevee')

from prompt_generator import get_prompt_generator
import random

def test_prompt_generator():
    print("="*60)
    print("🎲 Teste do Gerador de Prompts Aleatórios")
    print("="*60)
    print()
    
    # Dados simulados
    mock_location_data = {
        'city': 'Boston',
        'country': 'United States',
        'region': 'Massachusetts',
        'weather': {
            'description': 'sunny',
            'temp': 22
        }
    }
    
    username = "User"
    language = "en"
    
    # Obtém gerador
    generator = get_prompt_generator()
    
    print("📋 Categorias de tópicos disponíveis:")
    for i, category in enumerate(generator.topic_categories, 1):
        print(f"   {i}. {category}")
    print()
    
    print("🎯 Gerando 5 prompts aleatórios:")
    print("="*60)
    
    for i in range(5):
        print(f"\n🔄 Prompt #{i+1}:")
        print("-" * 60)
        
        prompt = generator.generate_prompt(username, language, mock_location_data)
        print(prompt)
        print("-" * 60)
    
    print("\n" + "="*60)
    print("✅ Teste concluído!")
    print("="*60)
    print()
    print("💡 Cada execução gera prompts diferentes!")
    print("   Execute novamente para ver mais variações.")

if __name__ == "__main__":
    test_prompt_generator()
