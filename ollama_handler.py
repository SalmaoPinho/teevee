import time
import os

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("Ollama não instalado. Execute: pip install ollama")

# Rastreia última modificação do arquivo
last_processed_time = 0

def process_message():
    """Processa mensagens do input.txt e gera respostas via Ollama"""
    global last_processed_time
    
    if not OLLAMA_AVAILABLE:
        # Mesmo sem Ollama, processa para não deixar arquivo pendente
        if os.path.exists('input.txt'):
            try:
                with open('input.txt', 'r', encoding='utf-8') as f:
                    message = f.read().strip()
                
                if message:
                    print(f"[SEM OLLAMA] Mensagem recebida: {message}")
                    with open('response.txt', 'w', encoding='utf-8') as f:
                        f.write("Ollama não está instalado. Execute: pip install ollama")
                    os.remove('input.txt')
            except Exception as e:
                print(f"Erro: {e}")
        return
    
    if os.path.exists('input.txt'):
        try:
            # Verifica se o arquivo foi modificado desde a última vez
            current_mtime = os.path.getmtime('input.txt')
            
            if current_mtime <= last_processed_time:
                return  # Já processado
            
            # Lê mensagem do usuário
            with open('input.txt', 'r', encoding='utf-8') as f:
                message = f.read().strip()
            
            if message:
                print(f"\n{'='*50}")
                print(f"📨 Mensagem recebida: {message}")
                print(f"{'='*50}")
                
                # Chama Ollama
                print("🤖 Chamando Ollama...")
                response = ollama.chat(model='llama3.2', messages=[
                    {
                        'role': 'system',
                        'content': 'Você é um assistente amigável e conciso. Responda de forma breve e direta em português.'
                    },
                    {
                        'role': 'user',
                        'content': message
                    }
                ])
                
                # Escreve resposta
                response_text = response['message']['content']
                print(f"✅ Resposta gerada: {response_text[:100]}...")
                
                with open('response.txt', 'w', encoding='utf-8') as f:
                    f.write(response_text)
                
                print(f"💾 Resposta salva em response.txt")
                print(f"{'='*50}\n")
                
                # Atualiza timestamp e remove input
                last_processed_time = current_mtime
                os.remove('input.txt')
        
        except Exception as e:
            print(f"❌ Erro ao processar: {e}")
            # Em caso de erro, escreve mensagem padrão
            with open('response.txt', 'w', encoding='utf-8') as f:
                f.write(f"Desculpe, ocorreu um erro: {str(e)}")
            if os.path.exists('input.txt'):
                os.remove('input.txt')

def main():
    """Loop principal que monitora input.txt"""
    print("="*60)
    print("🚀 Ollama Handler iniciado...")
    print("="*60)
    print(f"✓ Ollama disponível: {OLLAMA_AVAILABLE}")
    print(f"✓ Monitorando: input.txt")
    print(f"✓ Escrevendo em: response.txt")
    print(f"✓ Intervalo de verificação: 500ms")
    print("="*60)
    print("\n⏳ Aguardando mensagens...\n")
    
    while True:
        try:
            process_message()
            time.sleep(0.5)  # Verifica a cada 500ms
        except KeyboardInterrupt:
            print("\n\n" + "="*60)
            print("👋 Ollama Handler encerrado.")
            print("="*60)
            break
        except Exception as e:
            print(f"❌ Erro no loop principal: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()

