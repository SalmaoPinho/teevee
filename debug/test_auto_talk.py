"""
Teste do sistema de Auto-Talk
Simula o sistema gerando falas a cada 10 segundos (para teste rápido)
"""
import sys
sys.path.insert(0, r'c:\Users\Samuel\Documents\git\teevee')

from auto_talk import get_auto_talk_system
import time

def main():
    print("="*60)
    print("🤖 Teste do Sistema de Auto-Talk")
    print("="*60)
    print()
    
    # Cria sistema com intervalo de 10s para teste
    auto_talk = get_auto_talk_system(interval_seconds=10)
    
    print("📊 Configuração:")
    print(f"   Usuário: {auto_talk.username}")
    print(f"   Idioma: {auto_talk.lang_full}")
    print(f"   Intervalo: {auto_talk.interval}s")
    print()
    
    print("📋 Tópicos e pesos:")
    for topic, weight in auto_talk.topic_weights.items():
        bar = "█" * weight
        print(f"   {topic:15} [{weight:2}] {bar}")
    print()
    
    print("="*60)
    print("🔄 Iniciando loop de teste (Ctrl+C para parar)")
    print("="*60)
    print()
    
    talk_count = 0
    
    try:
        while talk_count < 5:  # Gera 5 falas para teste
            # Simula loop do jogo
            talk = auto_talk.update()
            
            if talk:
                talk_count += 1
                print(f"\n{'='*60}")
                print(f"💬 Fala #{talk_count}")
                print(f"{'='*60}")
                print(f"📌 Tópico: {talk['topic']}")
                print(f"💭 Texto: {talk['text']}")
                print(f"{'='*60}\n")
                
                # Mostra tempo até próxima fala
                print(f"⏰ Próxima fala em {auto_talk.interval} segundos...")
                print()
            
            time.sleep(1)  # Simula frame do jogo
        
        print("\n" + "="*60)
        print("✅ Teste concluído!")
        print("="*60)
        print()
        print(f"📊 Estatísticas:")
        print(f"   Total de falas: {talk_count}")
        print(f"   Intervalo usado: {auto_talk.interval}s")
        
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print("⏹️ Teste interrompido pelo usuário")
        print("="*60)

if __name__ == "__main__":
    main()
