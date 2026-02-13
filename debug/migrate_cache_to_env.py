"""
Script para migrar location_cache.json para .env
"""
import os
import json
from dotenv import set_key

def migrate_location_cache():
    print("="*60)
    print("📦 Migração: location_cache.json → .env")
    print("="*60)
    print()
    
    cache_file = 'location_cache.json'
    env_file = '.env'
    
    # Verifica se existe cache JSON
    if not os.path.exists(cache_file):
        print("⚠️ Nenhum location_cache.json encontrado")
        print("✅ Nada para migrar")
        return
    
    try:
        # Lê cache JSON
        print(f"📖 Lendo {cache_file}...")
        with open(cache_file, 'r') as f:
            cache_data = json.load(f)
        
        print(f"   Localização: {cache_data.get('city', 'Unknown')}, {cache_data.get('country', 'Unknown')}")
        
        # Cria .env se não existir
        if not os.path.exists(env_file):
            print(f"\n📝 Criando {env_file}...")
            with open(env_file, 'w') as f:
                f.write('# TeeVee Configuration\n')
                f.write('# Auto-generated location cache\n\n')
        
        # Migra dados
        print(f"\n💾 Salvando em {env_file}...")
        set_key(env_file, 'LOCATION_LAT', str(cache_data.get('lat', 0)))
        set_key(env_file, 'LOCATION_LON', str(cache_data.get('lon', 0)))
        set_key(env_file, 'LOCATION_CITY', cache_data.get('city', 'Unknown'))
        set_key(env_file, 'LOCATION_COUNTRY', cache_data.get('country', 'Unknown'))
        set_key(env_file, 'LOCATION_REGION', cache_data.get('region', 'Unknown'))
        set_key(env_file, 'LOCATION_TIMESTAMP', cache_data.get('timestamp', ''))
        
        print("✅ Migração concluída!")
        
        # Pergunta se deve remover JSON
        print(f"\n❓ Deseja remover {cache_file}? (s/n): ", end='')
        response = input().strip().lower()
        
        if response == 's':
            os.remove(cache_file)
            print(f"🗑️ {cache_file} removido")
        else:
            print(f"📁 {cache_file} mantido (você pode removê-lo manualmente)")
        
    except Exception as e:
        print(f"❌ Erro na migração: {e}")

if __name__ == "__main__":
    migrate_location_cache()
