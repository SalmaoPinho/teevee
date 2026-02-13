import random
import datetime
import psutil
import requests
import urllib.request
import json
import os
from dotenv import load_dotenv, set_key
import audio
import platform
from config import getVars, DICT

def get_cpu_temperature():
    """Obtém temperatura da CPU em Celsius (cross-platform)"""
    system = platform.system()
    
    try:
        # Linux - lê de /sys/class/thermal
        if system == "Linux":
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                temp = float(f.read().strip()) / 1000.0
            return round(temp, 1)
        
        # Windows - usa psutil sensors (se disponível)
        elif system == "Windows":
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                if temps:
                    # Tenta diferentes sensores comuns no Windows
                    for name in ['coretemp', 'cpu_thermal', 'acpitz']:
                        if name in temps and temps[name]:
                            return round(temps[name][0].current, 1)
            # Fallback: retorna "N/A" se não conseguir ler
            return "N/A"
        
        # macOS - usa psutil sensors
        elif system == "Darwin":
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                if temps and 'cpu_thermal' in temps:
                    return round(temps['cpu_thermal'][0].current, 1)
            return "N/A"
        
        else:
            return "N/A"
            
    except Exception as e:
        # Em caso de erro, retorna N/A silenciosamente
        return "N/A"
def process_line_converters(line, glock_info=None):
    """
    Processa conversores em uma linha (substitui +time, +date, etc.)
    
    Args:
        line: Linha com conversores (+time, +date, etc.)
        glock_info: Dicionário com informações do Glock (opcional)
    
    Returns:
        Linha processada com valores reais
    """
    import datetime
    from translations import translate_day, translate_month, translate_time_of_day, translate_weather
    
    # Copia a linha
    processed = line
    
    # Obtém hora atual
    now = datetime.datetime.now()
    hour = now.hour
    
    # Processa +time (hora do dia)
    if '+time' in processed:
        if 5 <= hour < 12:
            time_key = 'morning'
        elif 12 <= hour < 18:
            time_key = 'afternoon'
        elif 18 <= hour < 24:
            time_key = 'evening'
        else:
            time_key = 'night'
        
        # Traduz o período do dia
        time_translated = translate_time_of_day(time_key)
        processed = processed.replace('+time', time_translated)
    
    # Processa +date (data atual)
    if '+date' in processed:
        month_name = translate_month(now.month - 1)
        date_str = f"{month_name} {now.day}"
        processed = processed.replace('+date', date_str)
    
    # Processa +day (dia da semana)
    if '+day' in processed:
        day_name = translate_day(now.weekday())
        processed = processed.replace('+day', day_name)
    
    # Processa +weather (condição climática)
    if '+weather' in processed and glock_info:
        weather_key = glock_info.get('weather_cond', 'sunny')
        weather_translated = translate_weather(weather_key)
        processed = processed.replace('+weather', weather_translated)
    
    # Processa +temp (temperatura)
    if '+temp' in processed and glock_info:
        temp = glock_info.get('weather_temp', 'N/A')
        processed = processed.replace('+temp', str(temp))
    
    # Processa +city (cidade)
    if '+city' in processed and glock_info:
        city = glock_info.get('city', 'Unknown')
        processed = processed.replace('+city', city)
    
    return processed

# DEPRECATED: get_random_line() - não mais usado
# def get_random_line():
#     """Retorna uma linha aleatória processada com conversores"""
#     line = random.choice(DICT['lines']['eng'])
#     return process_line_converters(line)
class Glock:
    def __init__(self):
        self.vals={}
        self.info={}
        self.last_minute=None
        self.player=audio.MusicPlayer()
        # Inicializa monitoramento de CPU (importante para Raspberry Pi)
        psutil.cpu_percent(interval=None)  # Primeira chamada para inicializar
        self.update()
    def refresh_info(self):
        net = psutil.net_io_counters()
        disk= psutil.disk_usage('/')
        memory= psutil.virtual_memory()
        loc=self.get_real_location()
        
        # Obtém uso da CPU (não bloqueante)
        # No Raspberry Pi, interval=0.1 pode retornar 0 na primeira chamada
        # Usa interval=None para pegar o valor desde a última chamada
        cpu_usage = psutil.cpu_percent(interval=None)
        if cpu_usage == 0.0:
            # Fallback: força uma medição rápida
            cpu_usage = psutil.cpu_percent(interval=0.1)
        
        # Obtém temperatura da CPU
        cpu_temp = get_cpu_temperature()
        
        # Calcula barra de temperatura (0-100%)
        # Normaliza temperatura para barra visual
        if cpu_temp == "N/A":
            # Simula temperatura baseada no uso da CPU (para sistemas sem sensor)
            # 0% uso = 30°C, 100% uso = 70°C
            simulated_temp = 30 + (cpu_usage * 0.4)
            cpu_temp = round(simulated_temp, 1)
            cpu_temp_bar = int((simulated_temp - 30) / 50 * 100)
        else:
            # Temperatura real do sensor
            # Normaliza para 0-100% (30°C = 0%, 80°C = 100%)
            temp_min = 30
            temp_max = 80
            cpu_temp_bar = max(0, min(100, int((cpu_temp - temp_min) / (temp_max - temp_min) * 100)))
        
        self.info.update({
            'subtitle': "",  # Removido get_random_line() deprecated
            'cpu_temp': cpu_temp,
            'cpu_temp_bar': cpu_temp_bar,
            'cpu_usage': cpu_usage,
            'cpu_freq': int(psutil.cpu_freq().current) if psutil.cpu_freq() else "N/A",
            'disk_total': round(disk.total / (1024**3), 2),      # GB
            'disk_used': round(disk.used / (1024**3), 2),        # GB
            'disk_percent': disk.percent,
            'memory_total': round(memory.total / (1024**3), 2),  # GB
            'memory_used': round(memory.used / (1024**3), 2),    # GB
            'memory_percent': memory.percent,
            'net_sent': round(net.bytes_sent / (1024**2), 2),    # MB
            'net_recv': round(net.bytes_recv / (1024**2), 2),    # MB
            'map_lat': loc['lat'],
            'map_lon': loc['lon'],
            'map_zoom': getVars('zoom'),
            'weather_temp': self.get_weather_temp(),
            'weather_rain': self.get_weather_rain(),
            'weather_cond': self.get_weather_condition(),
            'music_queue': "Random",
        })        

    def get_weather_temp(self):
        """Simula temperatura baseada na hora"""
        import random
        base_temp = 20
        hour = datetime.datetime.now().hour
        # Mais quente ao meio dia (12-14), mais frio a noite
        variation = -abs(hour - 14) + 5 
        return base_temp + variation + random.randint(-2, 2)

    def get_weather_rain(self):
        """Simula chance de chuva"""
        import random
        return random.randint(0, 100)

    def get_weather_condition(self):
        """Simula condição do tempo"""
        import random
        # Retorna chaves traduzíveis ao invés de strings em inglês
        conditions = ["sunny", "cloudy", "rainy", "partly cloudy"]
        return random.choice(conditions)
    def update(self):
        now = datetime.datetime.now()
        
        # Importa sistema de tradução
        from translations import translate_day, translate_month
        
        self.vals={
            'week_day': translate_day(now.weekday()),  # Traduzido
            'time_12hr': now.strftime("%I:%M:%S %p"),  # 02:30:45 PM
            'time_24hr': now.strftime("%H:%M:%S"),     # 14:30:45
            'time_short': now.strftime("%H:%M"),       # 14:30
            'short_date': now.strftime("%m/%d/%Y"),      # 01/15/2024
            'month_name': translate_month(now.month - 1),  # Traduzido
            'month': translate_month(now.month - 1),   # Traduzido
            'days_left': (datetime.date(now.year, 12, 31) - now.date()).days, # 365
            'map_zoom': getVars('zoom'),
            'music_volume': getVars('volume'),

        }
        #print(self.vals,self.info)
        
        # Garante que map_status existe
        if 'map_status' not in self.info:
            self.info['map_status'] = ""

        # Atualiza info a cada minuto
        if self.last_minute != now.minute:
            self.refresh_info()
            self.last_minute = now.minute
    def _load_location_cache(self):
        """Carrega cache de localização do arquivo .env"""
        try:
            env_file = '.env'
            if os.path.exists(env_file):
                load_dotenv(env_file)
                
                lat = os.getenv('LOCATION_LAT')
                lon = os.getenv('LOCATION_LON')
                city = os.getenv('LOCATION_CITY')
                country = os.getenv('LOCATION_COUNTRY')
                region = os.getenv('LOCATION_REGION')
                
                if lat and lon and city:
                    cache_data = {
                        'lat': float(lat),
                        'lon': float(lon),
                        'city': city,
                        'country': country or 'Unknown',
                        'region': region or 'Unknown'
                    }
                    print(f"[CACHE] Localização carregada do .env: {city}")
                    return cache_data
        except Exception as e:
            print(f"[CACHE] Erro ao carregar .env: {e}")
        return None
    
    def _save_location_cache(self, location):
        """Salva localização no arquivo .env"""
        try:
            env_file = '.env'
            
            # Cria .env se não existir
            if not os.path.exists(env_file):
                with open(env_file, 'w') as f:
                    f.write('# TeeVee Configuration\n')
                    f.write('# Auto-generated location cache\n\n')
            
            # Salva cada campo
            set_key(env_file, 'LOCATION_LAT', str(location['lat']))
            set_key(env_file, 'LOCATION_LON', str(location['lon']))
            set_key(env_file, 'LOCATION_CITY', location['city'])
            set_key(env_file, 'LOCATION_COUNTRY', location['country'])
            set_key(env_file, 'LOCATION_REGION', location['region'])
            set_key(env_file, 'LOCATION_TIMESTAMP', datetime.datetime.now().isoformat())
            
            print(f"[CACHE] Localização salva no .env")
        except Exception as e:
            print(f"[CACHE] Erro ao salvar .env: {e}")
    
    def get_real_location(self):
        """Obtém localização real por IP com múltiplos serviços e cache"""
        
        # Lista de serviços de geolocalização (em ordem de preferência)
        services = [
            {
                'name': 'ipapi.co',
                'url': 'http://ipapi.co/json/',
                'parser': lambda data: {
                    'lat': data.get('latitude'),
                    'lon': data.get('longitude'),
                    'city': data.get('city', 'Unknown'),
                    'country': data.get('country_name', 'Unknown'),
                    'region': data.get('region', 'Unknown')
                }
            },
            {
                'name': 'ip-api.com',
                'url': 'http://ip-api.com/json/',
                'parser': lambda data: {
                    'lat': data.get('lat'),
                    'lon': data.get('lon'),
                    'city': data.get('city', 'Unknown'),
                    'country': data.get('country', 'Unknown'),
                    'region': data.get('regionName', 'Unknown')
                }
            },
            {
                'name': 'ipinfo.io',
                'url': 'http://ipinfo.io/json',
                'parser': lambda data: {
                    'lat': float(data.get('loc', '0,0').split(',')[0]) if data.get('loc') else None,
                    'lon': float(data.get('loc', '0,0').split(',')[1]) if data.get('loc') else None,
                    'city': data.get('city', 'Unknown'),
                    'country': data.get('country', 'Unknown'),
                    'region': data.get('region', 'Unknown')
                }
            }
        ]
        
        # Tenta cada serviço
        for service in services:
            try:
                print(f"[GEO] Tentando {service['name']}...")
                with urllib.request.urlopen(service['url'], timeout=3) as response:
                    data = json.loads(response.read().decode())
                    location = service['parser'](data)
                    
                    # Valida se obteve coordenadas válidas
                    if location['lat'] is not None and location['lon'] is not None:
                        print(f"✓ Localização obtida via {service['name']}: {location['city']}, {location['region']}, {location['country']} (lat: {location['lat']}, lon: {location['lon']})")
                        
                        # Salva em cache para uso futuro
                        self._save_location_cache(location)
                        self.location_cache = location
                        return location
                    else:
                        print(f"[GEO] {service['name']} retornou dados inválidos")
                        
            except Exception as e:
                print(f"[GEO] Falha em {service['name']}: {type(e).__name__}")
                continue
        
        # Se todos os serviços falharam, tenta usar cache persistente
        print("[GEO] Todos os serviços falharam, tentando cache...")
        cached_location = self._load_location_cache()
        if cached_location:
            print(f"✓ Usando localização do cache (pode estar desatualizada)")
            self.location_cache = cached_location
            return cached_location
        
        # Último recurso: coordenadas de Boston
        print("[GEO] ⚠️ Nenhum serviço disponível e sem cache - usando coordenadas padrão (Boston)")
        fallback_location = {
            'lat': 42.355, 
            'lon': -71.065,
            'city': 'Boston Common',
            'country': 'Commonwealth',
            'region': 'Massachusetts'
        }
        return fallback_location
