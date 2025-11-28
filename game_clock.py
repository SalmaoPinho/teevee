import datetime
from flask import json
import psutil
import urllib

def get_cpu_temperature():
    """Get CPU temperature in Celsius"""
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = float(f.read().strip()) / 1000.0
        return temp
    except:
        return "N/A"
class Glock:
    def __init__(self):
        self.vals={}
        self.info={}
        self.last_minute=None
        self.update()
    def refresh_info(self):
        net = psutil.net_io_counters()
        disk= psutil.disk_usage('/')
        memory= psutil.virtual_memory()
        loc=self.get_real_location()
        self.info.update({
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
            'weather_temp': self.get_weather_temp(),
            'weather_rain': self.get_weather_rain(),
            'weather_cond': self.get_weather_condition(),
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
        }
        #refresh info every minute
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
