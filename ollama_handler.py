import time
import os

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("Ollama não instalado. Execute: pip install ollama")

def process_message():
    """Processa mensagens do input.txt e gera respostas via Ollama"""
    if not OLLAMA_AVAILABLE:
        return
    
    if os.path.exists('input.txt'):
        try:
            # Lê mensagem do usuário
            with open('input.txt', 'r', encoding='utf-8') as f:
                message = f.read().strip()
            
            if message:
                print(f"Processando: {message}")
                
                # Chama Ollama
                response = ollama.chat(model='llama3.2', messages=[
                    {
                        'role': 'system',
                        'content': 'Você é um assistente amigável e conciso. Responda de forma breve e direta.'
                    },
                    {
                        'role': 'user',
                        'content': message
                    }
                ])
                
                # Escreve resposta
                response_text = response['message']['content']
                with open('response.txt', 'w', encoding='utf-8') as f:
                    f.write(response_text)
                
                print(f"Resposta: {response_text[:50]}...")
                
                # Remove input processado
                os.remove('input.txt')
        
        except Exception as e:
            print(f"Erro ao processar: {e}")
            # Em caso de erro, escreve mensagem padrão
            with open('response.txt', 'w', encoding='utf-8') as f:
                f.write("Desculpe, ocorreu um erro ao processar sua mensagem.")
            if os.path.exists('input.txt'):
                os.remove('input.txt')

def main():
    """Loop principal que monitora input.txt"""
    print("Ollama Handler iniciado...")
    print("Monitorando input.txt para novas mensagens...")
    
    while True:
        try:
            process_message()
            time.sleep(0.5)  # Verifica a cada 500ms
        except KeyboardInterrupt:
            print("\nOllama Handler encerrado.")
            break
        except Exception as e:
            print(f"Erro no loop principal: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
