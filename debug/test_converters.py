"""
Teste do sistema de conversores de linhas
"""
import sys
sys.path.insert(0, r'c:\Users\Samuel\Documents\git\teevee')

from game_clock import process_line_converters, get_random_line

def test_converters():
    print("="*60)
    print("🔄 Teste de Conversores de Linhas")
    print("="*60)
    print()
    
    # Testa conversores básicos (sem glock_info)
    test_lines = [
        "Good +time!",
        "Happy +day!",
        "It's +date today!",
        "The weather is +weather!",
        "It's +temp degrees outside!",
        "Greetings from +city!"
    ]
    
    print("📝 Conversores básicos (sem dados do Glock):")
    print()
    for line in test_lines[:3]:
        processed = process_line_converters(line)
        print(f"  Original:   {line}")
        print(f"  Processado: {processed}")
        print()
    
    # Simula dados do Glock
    mock_glock_info = {
        'weather': {
            'description': 'sunny',
            'temp': 28
        },
        'city': 'Goiânia'
    }
    
    print("📊 Conversores com dados do Glock:")
    print()
    for line in test_lines[3:]:
        processed = process_line_converters(line, mock_glock_info)
        print(f"  Original:   {line}")
        print(f"  Processado: {processed}")
        print()
    
    # Testa função get_random_line
    print("🎲 Linhas aleatórias:")
    print()
    for i in range(5):
        line = get_random_line()
        print(f"  {i+1}. {line}")
    
    print()
    print("="*60)
    print("✅ Teste concluído!")
    print("="*60)

if __name__ == "__main__":
    test_converters()
