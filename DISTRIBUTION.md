# TeeVee - Guia de Distribuição

## Opções de Distribuição

### 1. PyInstaller (Recomendado)

Cria um executável standalone que funciona sem Python instalado.

#### Instalação
```bash
pip install pyinstaller
```

#### Build
```bash
# Windows
build.bat

# Ou manualmente
pyinstaller teevee.spec --clean
```

#### Resultado
- Executável em `dist/TeeVee.exe`
- Tamanho: ~50-100MB
- Funciona sem instalação

#### Distribuição
1. Compacte a pasta `dist/TeeVee/` em ZIP
2. Usuários extraem e executam `TeeVee.exe`

---

### 2. Docker (Para Desenvolvedores)

#### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia arquivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

**Nota**: GUI em Docker é complexo e requer X11 forwarding.

---

### 3. Instalação Manual (Atual)

#### Windows
```bash
# Instalar Python 3.11+
# Clonar repositório
git clone <repo>
cd teevee

# Instalar dependências
pip install -r requirements.txt

# Executar
python start.py
```

---

## Comparação

| Método | Facilidade | Tamanho | Cross-Platform | Requer Python |
|--------|-----------|---------|----------------|---------------|
| PyInstaller | ⭐⭐⭐⭐⭐ | ~80MB | ❌ (build por OS) | ❌ |
| Docker | ⭐⭐ | ~500MB | ✅ | ❌ |
| Manual | ⭐⭐⭐ | ~10MB | ✅ | ✅ |

## Recomendação

**Para usuários finais**: Use PyInstaller
**Para desenvolvedores**: Use instalação manual
**Para servidores**: Considere Docker (sem GUI)
