# Ephemeris - TeeVee System

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.6.1-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

**Ephemeris** é um sistema interativo retro-futurista com estética CRT, apresentando o TeeVee - um assistente virtual animado com personalidade própria.

## 📺 Características

### Interface Retro
- **Efeitos CRT autênticos**: Scanlines, distorção barrel, overlay de textura
- **Animações suaves**: TeeVee pisca, fala e reage ao ambiente
- **Estética personalizável**: Cores configuráveis via `defs.ini`

### TeeVee Interativo
- **Olhos que seguem o mouse**: Rastreamento em 2D (horizontal e vertical)
- **Estado de tontura**: Fica irritado com movimentos frenéticos do mouse
- **Animações de fala**: Boca sincronizada com texto
- **Saudação contextual**: "Bom dia/tarde/noite" baseado no horário

### Funcionalidades
- **Chat com IA**: Integração com Ollama para conversas
- **Player de música**: Reproduz MP3, M4A, WAV com extração de capa de álbum
- **Mapa em tempo real**: Geolocalização por IP com OpenStreetMap
- **Monitor de sistema**: CPU, memória, disco, rede (cross-platform)
- **Clima simulado**: Temperatura, chuva, condições

## 🚀 Instalação

### Requisitos
- Python 3.11 ou superior
- Pygame 2.6.1
- psutil 5.9.0+
- requests 2.31.0+
- numpy 1.24.0+
- mutagen 1.47.0+
- Ollama (opcional, para chat com IA)

### Instalação Rápida

```bash
# Clone o repositório
git clone https://github.com/SalmaoPinho/teevee.git
cd teevee

# Instale as dependências
pip install -r requirements.txt

# Execute
python start.py
```

### Instalação no Raspberry Pi 5

```bash
# Atualize o sistema
sudo apt update && sudo apt upgrade -y

# Instale dependências do sistema
sudo apt install python3-pip python3-pygame -y

# Clone e instale
git clone https://github.com/SalmaoPinho/teevee.git
cd teevee
pip3 install -r requirements.txt

# Execute
python3 start.py
```

### Instalação do Ollama (Opcional)

**Windows/macOS:**
1. Baixe em: https://ollama.ai
2. Instale o executável
3. Execute: `ollama pull llama2`

**Linux/Raspberry Pi:**
```bash
# Instale Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Baixe um modelo
ollama pull llama2

# Execute o handler (em terminal separado)
python ollama_handler.py
```

**Nota**: O Ollama requer ~4GB de RAM. No Raspberry Pi 5, use modelos menores como `tinyllama`.

## 🎮 Uso

### Navegação
- **Setas esquerda/direita**: Navegar entre menus
- **Mouse**: Interagir com botões e elementos
- **ESC**: Sair

### Menus Disponíveis
- **MENU**: Chat com TeeVee
- **GPS**: Mapa em tempo real
- **CPU**: Monitor de sistema
- **MUSIC**: Player de música
- **WEATHER**: Informações climáticas
- **CONFIG**: Configurações visuais

### Interação com TeeVee
- **Mova o mouse**: TeeVee segue com os olhos
- **Movimentos frenéticos**: TeeVee fica tonto (olhos de raiva)
- **Digite no chat**: TeeVee responde (requer Ollama)

## ⚙️ Configuração

### defs.ini

```ini
[SCREEN]
width = 800          # Largura da janela
height = 600         # Altura da janela
crtsize = 4          # Tamanho da textura CRT

[COLORS]
bg = (30, 30, 30)    # Cor de fundo
pri = (255, 255, 255) # Cor primária (texto)
sec = (128, 128, 128) # Cor secundária
ter = (0, 255, 0)     # Cor terciária (destaque)

[TOGGLE]
fullscreen = off     # Tela cheia
crt = on             # Efeito CRT
distortion = on      # Distorção barrel
overlay = on         # Overlay de textura
scanlines = on       # Scanlines
```

### Personalizando Cores

Edite `defs.ini` para mudar o esquema de cores:

```ini
# Tema verde fosforescente (padrão)
ter = (0, 255, 0)

# Tema âmbar
ter = (255, 191, 0)

# Tema azul
ter = (0, 191, 255)
```

## 📁 Estrutura do Projeto

```
teevee/
├── assets/
│   ├── spritesheet.png      # Sprites do TeeVee e ícones
│   ├── overlay.png          # Textura CRT
│   └── fonts/               # Fontes bitmap
├── main.py                  # Loop principal
├── graphics.py              # Sistema gráfico e TeeVee
├── ui.py                    # Sistema de interface
├── game_clock.py            # Relógio e informações do sistema
├── audio.py                 # Player de música
├── map_system.py            # Sistema de mapas
├── config.py                # Gerenciamento de configuração
├── ollama_handler.py        # Handler para chat com IA
├── defs.ini                 # Configurações
├── dictionary.json          # Definições de UI
└── requirements.txt         # Dependências Python
```

## 🎨 Recursos Técnicos

### Sistema de Sprites
- Carregamento dinâmico de sprites
- Escala e rotação automáticas
- Cache de sprites para performance

### Efeitos CRT
- **Scanlines**: Linhas horizontais animadas
- **Barrel Distortion**: Curvatura de tela CRT
- **Overlay**: Textura de grade de pixels
- **Todos configuráveis** via `defs.ini`

### Sistema de Animação
- Animação de fala sincronizada
- Piscar de olhos aleatório
- Movimento de olhos em 2D
- Estados emocionais (normal, tonto)

### Cross-Platform
- Funciona em Windows, Linux e macOS
- Detecção automática de temperatura de CPU
- Fallbacks para recursos não disponíveis

## 🔧 Distribuição

### PyInstaller (Executável)

```bash
# Instale PyInstaller
pip install pyinstaller

# Compile
python build.bat  # Windows
# ou
pyinstaller teevee.spec --clean

# Executável em dist/TeeVee.exe
```

### Docker (Experimental)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

**Nota**: GUI em Docker requer X11 forwarding.

## 🐛 Solução de Problemas

### TeeVee não aparece
- Verifique se `assets/spritesheet.png` existe
- Confirme que Pygame está instalado corretamente

### Efeitos CRT não funcionam
- Verifique `defs.ini` - efeitos devem estar `on`
- Confirme que `assets/overlay.png` existe

### Chat não responde
- Certifique-se de que Ollama está instalado e rodando
- Execute `ollama_handler.py` em terminal separado
- Verifique se `input.txt` e `response.txt` são criados

### Música não toca
- Instale dependências de áudio: `pip install pygame`
- Coloque arquivos MP3/M4A na pasta de música configurada
- Verifique permissões de arquivo

## 📝 Desenvolvimento

### Adicionando Novos Sprites

```python
# Em graphics.py, função init_graphics()
SPRITE_LOADER.create_sprite(
    key="meu_sprite",
    position=(x, y),      # Posição no spritesheet
    size=(width, height), # Tamanho em pixels
    scale=1.0,            # Escala
    alpha=255,            # Transparência (0-255)
    angle=0               # Rotação em graus
)
```

### Adicionando Novos Menus

1. Adicione formato em `dictionary.json`:
```json
"meu_menu": {
    "background": false,
    "subelements": { ... }
}
```

2. Adicione em `contentvals`:
```json
"MEU_MENU": {
    "format": "meu_menu"
}
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🙏 Créditos

- **Desenvolvido por**: Salmão Pinho
- **Inspiração**: Terminais CRT vintage, Fallout Pip-Boy
- **Fontes**: Jersey10, bmspace (bitmap fonts)
- **Mapas**: OpenStreetMap
- **IA**: Ollama

## 📧 Contato

- GitHub: [@SalmaoPinho](https://github.com/SalmaoPinho)
- Projeto: [teevee](https://github.com/SalmaoPinho/teevee)

---

**Ephemeris** - *Onde o retro encontra o futuro* 📺✨
