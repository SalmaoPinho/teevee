import datetime
import json
import psutil
import urllib
import random
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
def get_random_line():
    return random.choice(DICT['lines']['eng'])
class Glock:
    def __init__(self):
        self.vals={}
        self.info={}
        self.last_minute=None
        self.player=audio.MusicPlayer()
        self.update()
    def refresh_info(self):
        net = psutil.net_io_counters()
        disk= psutil.disk_usage('/')
        memory= psutil.virtual_memory()
        loc=self.get_real_location()
        self.info.update({
            'subtitle': get_random_line(),
            'cpu_temp': get_cpu_temperature(),
            'cpu_usage': psutil.cpu_percent(interval=0.1),
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
        conditions = ["Sunny", "Cloudy", "Rainy", "Stormy", "Foggy"]
        return random.choice(conditions)
    def update(self):
        now = datetime.datetime.now()
        self.vals={
            'week_day': now.strftime("%A"),  # Monday
            'time_12hr': now.strftime("%I:%M:%S %p"),  # 02:30:45 PM
            'time_24hr': now.strftime("%H:%M:%S"),     # 14:30:45
            'time_short': now.strftime("%H:%M"),       # 14:30
            'week_day': now.strftime("%A"),  # Monday
            'short_date': now.strftime("%m/%d/%Y"),      # 01/15/2024
            'month_name': now.strftime("%B"),            # January
            'days_left': (datetime.date(now.year, 12, 31) - now.date()).days, # 365
            'map_zoom': getVars('zoom'),
            'music_volume': getVars('volume'),

        }
        
        # Garante que map_status existe
        if 'map_status' not in self.info:
            self.info['map_status'] = ""

        # Atualiza info a cada minuto
        if self.last_minute != now.minute:
            self.refresh_info()
            self.last_minute = now.minute
    def get_real_location(self):
        """Obtém localização real por IP"""
        try:
            with urllib.request.urlopen('http://ipapi.co/json/', timeout=5) as response:
                data = json.loads(response.read().decode())
                location = {
                    'lat': data.get('latitude', 42.355),
                    'lon': data.get('longitude', -71.065),
                    'city': data.get('city', 'Unknown'),
                    'country': data.get('country_name', 'Unknown'),
                    'region': data.get('region', 'Unknown')
                }
                self.location_cache = location
                return location 
        except:
            return {
                'lat': 42.355, 
                'lon': -71.065,
                'city': 'Boston Common',
                'country': 'Commonwealth',
                'region': 'Massachusetts'
            }
