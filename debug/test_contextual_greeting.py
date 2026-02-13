"""
Teste de greeting com informações de localização e clima
Simula dados do game_clock (Boston com temperatura aleatória)
"""
import random

def test_contextual_greeting():
    """
    Testa geração de greeting com contexto de localização e clima
    """
    print("="*60)
    print("🌍 Teste de Greeting Contextual")
    print("="*60)
    print()
    
    # Simula dados do game_clock (Boston)
    mock_location_data = {
        'city': 'Boston',
        'country': 'United States',
        'region': 'Massachusetts',
        'weather': {
            'description': random.choice(['sunny', 'cloudy', 'rainy', 'partly cloudy']),
            'temp': random.randint(15, 30)  # Temperatura em Celsius
        }
    }
    
    # Simula configurações do usuário
    username = "User"
    language = "en"
    
    print("📊 Dados simulados:")
    print(f"   Usuário: {username}")
    print(f"   Idioma: {language}")
    print(f"   Cidade: {mock_location_data['city']}, {mock_location_data['region']}")
    print(f"   Clima: {mock_location_data['weather']['description']}")
    print(f"   Temperatura: {mock_location_data['weather']['temp']}°C")
    print()
    
    # Testa com Ollama
    try:
        import ollama
        
        # Constrói prompt com contexto
        prompt = f"""In the language: English, please greet the user: {username}.
Include a brief comment about the current weather and location.

Context:
- Location: {mock_location_data['city']}, {mock_location_data['region']}, {mock_location_data['country']}
- Weather: {mock_location_data['weather']['description']}
- Temperature: {mock_location_data['weather']['temp']}°C

Keep it warm, friendly, and brief (2-3 sentences max)."""
        
        print("🤖 Gerando greeting contextual com Ollama...")
        print()
        
        response = ollama.chat(
            model='llama3.2',
            messages=[
                {
                    'role': 'system',
                    'content': 'You are a friendly assistant. Respond ONLY in English. Be warm, natural, and conversational. Keep responses brief.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        )
        
        greeting = response['message']['content'].strip()
        
        print("✅ Greeting gerado:")
        print("-" * 60)
        print(greeting)
        print("-" * 60)
        print()
        
        # Testa em português também
        print("🇧🇷 Testando em português...")
        print()
        
        prompt_pt = f"""No idioma: Português, por favor cumprimente o usuário: {username}.
Inclua um breve comentário sobre o clima e localização atual.

Contexto:
- Localização: {mock_location_data['city']}, {mock_location_data['region']}, {mock_location_data['country']}
- Clima: {mock_location_data['weather']['description']}
- Temperatura: {mock_location_data['weather']['temp']}°C

Seja caloroso, amigável e breve (2-3 frases no máximo)."""
        
        response_pt = ollama.chat(
            model='llama3.2',
            messages=[
                {
                    'role': 'system',
                    'content': 'Você é um assistente amigável. Responda APENAS em Português. Seja caloroso, natural e conversacional. Mantenha respostas breves.'
                },
                {
                    'role': 'user',
                    'content': prompt_pt
                }
            ]
        )
        
        greeting_pt = response_pt['message']['content'].strip()
        
        print("✅ Greeting em português:")
        print("-" * 60)
        print(greeting_pt)
        print("-" * 60)
        print()
        
        print("="*60)
        print("✅ Teste concluído com sucesso!")
        print("="*60)
        
    except ImportError:
        print("❌ Ollama não disponível")
        print("   Execute: pip install ollama")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_contextual_greeting()
