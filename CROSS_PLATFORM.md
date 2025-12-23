# Sistema de Informações Cross-Platform

## Resumo

O TeeVee usa `psutil` para coletar informações do sistema de forma cross-platform, funcionando em Windows, Linux e macOS.

## Informações Coletadas

### ✅ Sempre Disponíveis (Cross-Platform)

| Informação | Função | Plataformas |
|------------|--------|-------------|
| **CPU Usage** | `psutil.cpu_percent()` | Windows, Linux, macOS |
| **CPU Frequency** | `psutil.cpu_freq()` | Windows, Linux, macOS |
| **Memory Total/Used** | `psutil.virtual_memory()` | Windows, Linux, macOS |
| **Disk Total/Used** | `psutil.disk_usage('/')` | Windows, Linux, macOS |
| **Network Sent/Recv** | `psutil.net_io_counters()` | Windows, Linux, macOS |

### ⚠️ Dependente de Plataforma

| Informação | Linux | Windows | macOS |
|------------|-------|---------|-------|
| **CPU Temperature** | ✅ `/sys/class/thermal` | ⚠️ `psutil.sensors_temperatures()` | ⚠️ `psutil.sensors_temperatures()` |

## Implementação da Temperatura

```python
def get_cpu_temperature():
    system = platform.system()
    
    # Linux
    if system == "Linux":
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            return float(f.read()) / 1000.0
    
    # Windows
    elif system == "Windows":
        if hasattr(psutil, "sensors_temperatures"):
            temps = psutil.sensors_temperatures()
            # Tenta: coretemp, cpu_thermal, acpitz
            ...
    
    # macOS
    elif system == "Darwin":
        if hasattr(psutil, "sensors_temperatures"):
            temps = psutil.sensors_temperatures()
            ...
    
    # Fallback
    return "N/A"
```

## Notas Importantes

### Windows
- Temperatura pode não estar disponível em todos os sistemas
- Requer drivers de sensor instalados
- Alguns laptops não expõem sensores via software

### macOS
- Temperatura geralmente não disponível via `psutil`
- Requer ferramentas específicas (ex: `osx-cpu-temp`)
- Retorna "N/A" na maioria dos casos

### Linux
- Funciona na maioria dos sistemas
- Raspberry Pi: `/sys/class/thermal/thermal_zone0/temp`
- Outros: pode variar o caminho do sensor

## Garantindo Compatibilidade

1. **Sempre use `psutil`** para informações básicas
2. **Detecte o OS** com `platform.system()`
3. **Tenha fallbacks** para quando sensores não estão disponíveis
4. **Trate exceções** silenciosamente (retorne "N/A")

## Dependências

```txt
psutil>=5.9.0  # Cross-platform system info
```

## Testando

```python
import psutil
import platform

print(f"OS: {platform.system()}")
print(f"CPU: {psutil.cpu_percent()}%")
print(f"Memory: {psutil.virtual_memory().percent}%")
print(f"Temp: {get_cpu_temperature()}°C")
```

O sistema funciona em **qualquer plataforma** com degradação graciosa quando recursos não estão disponíveis!
