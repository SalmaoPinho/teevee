"""
Ollama Handler Simplificado
Roda como thread em background, sem terminal separado
"""
import time
import os
import threading

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("[OLLAMA] Não instalado. Execute: pip install ollama")

class OllamaHandler:
    """Handler simplificado que roda em background thread"""
    
    def __init__(self):
        self.running = False
        self.thread = None
        self.last_processed_time = 0
    
    def start(self):
        """Inicia o handler em background"""
        if self.running:
            print("[OLLAMA] Handler já está rodando")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        print("[OLLAMA] Handler iniciado em background")
    
    def stop(self):
        """Para o handler"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        print("[OLLAMA] Handler parado")
    
    def _run_loop(self):
        """Loop principal do handler"""
        while self.running:
            try:
                self._process_message()
            except Exception as e:
                print(f"[OLLAMA] Erro no handler: {e}")
            
            # Aguarda 100ms antes de verificar novamente
            time.sleep(0.1)
    
    def _process_message(self):
        """Processa mensagens do input.txt"""
        if not OLLAMA_AVAILABLE:
            # Sem Ollama, apenas limpa arquivo pendente
            if os.path.exists('input.txt'):
                try:
                    with open('input.txt', 'r', encoding='utf-8') as f:
                        message = f.read().strip()
                    
                    if message:
                        with open('response.txt', 'w', encoding='utf-8') as f:
                            f.write("Ollama não está instalado.")
                        os.remove('input.txt')
                except Exception:
                    pass
            return
        
        if not os.path.exists('input.txt'):
            return
        
        try:
            # Verifica se arquivo foi modificado
            current_mtime = os.path.getmtime('input.txt')
            
            if current_mtime <= self.last_processed_time:
                return  # Já processado
            
            # Lê mensagem
            with open('input.txt', 'r', encoding='utf-8') as f:
                message = f.read().strip()
            
            if not message:
                return
            
            print(f"\n[OLLAMA] 📨 Mensagem: {message}")
            
            # Gera resposta via Ollama
            response = ollama.chat(
                model='llama3.2',
                messages=[
                    {
                        'role': 'system',
                        'content': 'You are a helpful assistant. Be concise and friendly.'
                    },
                    {
                        'role': 'user',
                        'content': message
                    }
                ]
            )
            
            answer = response['message']['content']
            print(f"[OLLAMA] 💬 Resposta: {answer[:100]}...")
            
            # Salva resposta
            with open('response.txt', 'w', encoding='utf-8') as f:
                f.write(answer)
            
            # Remove input
            os.remove('input.txt')
            
            # Atualiza timestamp
            self.last_processed_time = current_mtime
            
        except Exception as e:
            print(f"[OLLAMA] Erro ao processar: {e}")
            # Remove input mesmo com erro
            if os.path.exists('input.txt'):
                try:
                    os.remove('input.txt')
                except:
                    pass

# Instância global
_handler = None

def get_handler():
    """Retorna instância singleton do handler"""
    global _handler
    if _handler is None:
        _handler = OllamaHandler()
    return _handler

def start_handler():
    """Inicia o handler"""
    get_handler().start()

def stop_handler():
    """Para o handler"""
    if _handler:
        _handler.stop()

if __name__ == "__main__":
    print("="*60)
    print("🚀 Ollama Handler (standalone test) iniciado...")
    print("="*60)
    print(f"✓ Ollama disponível: {OLLAMA_AVAILABLE}")
    print(f"✓ Monitorando: input.txt")
    print(f"✓ Escrevendo em: response.txt")
    print(f"✓ Intervalo de verificação: 100ms")
    print("="*60)
    print("\n⏳ Aguardando mensagens... (Crie input.txt para testar)\n")
    
    start_handler()
    
    try:
        while True:
            time.sleep(1) # Mantém o programa principal rodando
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print("👋 Ollama Handler (standalone test) encerrado.")
        print("="*60)
    finally:
        stop_handler()
