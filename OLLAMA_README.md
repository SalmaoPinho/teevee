# Integração Ollama - Instruções de Uso

## Pré-requisitos

1. **Instalar Ollama**
   - Windows: Baixe de [ollama.ai](https://ollama.ai)
   - Ou instale via pip: `pip install ollama`

2. **Baixar modelo**
   ```bash
   ollama pull llama3.2
   ```

## Como Usar

### Opção 1: Com Script Separado (Recomendado)

1. **Inicie o handler do Ollama** (em um terminal separado):
   ```bash
   python ollama_handler.py
   ```
   
2. **Inicie a aplicação** (em outro terminal):
   ```bash
   python main.py
   ```

3. **Use o chat:**
   - Navegue para a página MENU
   - Clique no campo de input
   - Digite sua mensagem
   - Pressione Enter ou clique "Send"
   - Aguarde "Pensando..." mudar para a resposta
   - Veja o TeeVee animar!

### Opção 2: Sem Ollama (Fallback)

Se o Ollama não estiver instalado, o sistema continuará funcionando mas mostrará uma mensagem de erro no `ollama_handler.py`. A aplicação principal não será afetada.

## Arquitetura

```
[TeeVee App]
    ↓ escreve
input.txt
    ↓ lê
[ollama_handler.py]
    ↓ chama
[Ollama API]
    ↓ escreve
response.txt
    ↓ lê
[TeeVee App] → Animação!
```

## Arquivos Temporários

- `input.txt`: Criado quando usuário envia mensagem, deletado após processamento
- `response.txt`: Criado quando Ollama responde, deletado após leitura

## Troubleshooting

**Problema:** "Pensando..." não muda
- Verifique se `ollama_handler.py` está rodando
- Verifique se Ollama está instalado: `ollama --version`
- Verifique se o modelo está baixado: `ollama list`

**Problema:** Erro ao processar mensagem
- Verifique logs do `ollama_handler.py`
- Tente reiniciar o handler

**Problema:** Resposta muito lenta
- Modelo grande pode demorar
- Considere usar modelo menor: `ollama pull llama3.2:1b`
