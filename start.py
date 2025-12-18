"""
Launcher para TeeVee com Ollama
Inicia o handler e a aplicação principal automaticamente
"""
import subprocess
import sys
import time
import os

def main():
    print("="*60)
    print("🚀 TeeVee Launcher")
    print("="*60)
    
    # Verifica se ollama está instalado
    try:
        import ollama
        print("✓ Ollama instalado")
    except ImportError:
        print("⚠️  Ollama não instalado")
        print("   Execute: pip install ollama")
        print("   Depois: ollama pull llama3.2")
        response = input("\nContinuar mesmo assim? (s/n): ")
        if response.lower() != 's':
            return
    
    print("\n" + "="*60)
    print("Iniciando processos...")
    print("="*60)
    
    # Inicia o handler em background
    print("\n1. Iniciando Ollama Handler...")
    handler_process = subprocess.Popen(
        [sys.executable, 'ollama_handler.py'],
        creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
    )
    
    # Aguarda um pouco para o handler iniciar
    time.sleep(1)
    print("   ✓ Handler iniciado (PID: {})".format(handler_process.pid))
    
    # Inicia a aplicação principal
    print("\n2. Iniciando TeeVee...")
    try:
        main_process = subprocess.run([sys.executable, 'main.py'])
    except KeyboardInterrupt:
        print("\n\nInterrompido pelo usuário")
    
    # Quando main.py fechar, encerra o handler
    print("\n" + "="*60)
    print("Encerrando processos...")
    print("="*60)
    
    print("\n✓ Encerrando Handler...")
    handler_process.terminate()
    handler_process.wait()
    
    print("✓ Todos os processos encerrados")
    print("\n" + "="*60)
    print("👋 Até logo!")
    print("="*60)

if __name__ == "__main__":
    main()
