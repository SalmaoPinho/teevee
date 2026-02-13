"""
Teste do sistema de tradução
"""
import sys
sys.path.insert(0, r'c:\Users\Samuel\Documents\git\teevee')

from translations import get_translation_system, translate_day, translate_month, translate_weather, format_date
from datetime import datetime

def test_translations():
    print("="*60)
    print("🌍 Teste do Sistema de Tradução")
    print("="*60)
    print()
    
    # Testa em diferentes idiomas
    languages = ['en', 'pt', 'es', 'fr', 'de', 'it', 'ja', 'zh']
    
    for lang in languages:
        print(f"📌 Idioma: {lang}")
        print("-" * 60)
        
        # Cria sistema com idioma específico
        trans = get_translation_system()
        trans.current_language = lang
        
        # Testa dias
        print(f"   Dias: {trans.get_day_name(0)} (Mon), {trans.get_day_name(6)} (Sun)")
        
        # Testa meses
        print(f"   Meses: {trans.get_month_name(0)} (Jan), {trans.get_month_name(11)} (Dec)")
        
        # Testa período do dia
        print(f"   Períodos: {trans.get_time_of_day('morning')}, {trans.get_time_of_day('evening')}")
        
        # Testa clima
        print(f"   Clima: {trans.get_weather('sunny')}, {trans.get_weather('rainy')}")
        
        # Testa formatação de data
        now = datetime.now()
        print(f"   Data completa: {trans.format_date(now, 'full')}")
        print(f"   Data curta: {trans.format_date(now, 'short')}")
        
        print()
    
    print("="*60)
    print("✅ Teste concluído!")
    print("="*60)

if __name__ == "__main__":
    test_translations()
