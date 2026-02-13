"""
Teste: Google News + Llama
Busca notícia, traduz e explica de forma simples
"""
import feedparser
import random

def fetch_google_news(category='top', max_results=5):
    """
    Busca notícias do Google News RSS
    
    Args:
        category: 'top', 'tech', 'science', 'world'
        max_results: Número máximo de notícias
    
    Returns:
        list: Lista de dicionários com title, link, published
    """
    urls = {
        'top': 'https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en',
        'tech': 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en',
        'science': 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFptZHpJU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en',
        'world': 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en'
    }
    
    url = urls.get(category, urls['top'])
    
    print(f"🔍 Buscando notícias: {category}")
    print(f"   URL: {url[:60]}...")
    print()
    
    feed = feedparser.parse(url)
    
    news_list = []
    for entry in feed.entries[:max_results]:
        news_list.append({
            'title': entry.title,
            'link': entry.link if hasattr(entry, 'link') else '',
            'published': entry.published if hasattr(entry, 'published') else 'Unknown'
        })
    
    return news_list

def translate_and_explain_news(news_title, target_language='Portuguese'):
    """
    Usa Llama para traduzir e explicar uma notícia
    
    Args:
        news_title: Título da notícia em inglês
        target_language: Idioma alvo (Portuguese, Spanish, etc.)
    
    Returns:
        str: Explicação traduzida e simplificada
    """
    try:
        import ollama
        
        prompt = f"""Translate and briefly explain this news headline to someone in {target_language}:

"{news_title}"

Instructions:
1. Translate the headline to {target_language}
2. Explain what it means in 1-2 simple sentences
3. Keep it conversational and easy to understand

Format:
Título: [translated headline]
Explicação: [brief explanation]"""
        
        print("🤖 Enviando para Llama...")
        
        response = ollama.chat(
            model='llama3.2',
            messages=[
                {
                    'role': 'system',
                    'content': f'You are a helpful translator and explainer. Respond ONLY in {target_language}. Be clear, concise, and conversational.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        )
        
        return response['message']['content'].strip()
        
    except ImportError:
        return "❌ Ollama não disponível"
    except Exception as e:
        return f"❌ Erro: {e}"

def main():
    print("="*60)
    print("📰 Teste: Google News + Llama Translation")
    print("="*60)
    print()
    
    # Busca notícias
    print("📡 Buscando notícias do Google News...")
    print()
    
    categories = ['top', 'tech', 'science']
    category = random.choice(categories)
    
    news_list = fetch_google_news(category=category, max_results=5)
    
    if not news_list:
        print("❌ Nenhuma notícia encontrada")
        return
    
    print(f"✅ Encontradas {len(news_list)} notícias na categoria '{category}'")
    print()
    
    # Mostra todas as notícias
    print("📋 Notícias disponíveis:")
    print("-" * 60)
    for i, news in enumerate(news_list, 1):
        print(f"{i}. {news['title'][:70]}...")
        print(f"   Data: {news['published']}")
        print()
    
    # Escolhe uma aleatória para traduzir
    selected_news = random.choice(news_list)
    
    print("="*60)
    print("🎯 Notícia selecionada para tradução:")
    print("="*60)
    print()
    print(f"📰 Original (English):")
    print(f"   {selected_news['title']}")
    print()
    
    # Traduz e explica
    print("🌍 Traduzindo e explicando em Português...")
    print()
    
    explanation = translate_and_explain_news(selected_news['title'], 'Portuguese')
    
    print("✅ Resultado:")
    print("-" * 60)
    print(explanation)
    print("-" * 60)
    print()
    
    # Testa em outro idioma
    print("="*60)
    print("🌍 Testando em Espanhol...")
    print("="*60)
    print()
    
    another_news = random.choice(news_list)
    print(f"📰 Original: {another_news['title'][:70]}...")
    print()
    
    explanation_es = translate_and_explain_news(another_news['title'], 'Spanish')
    
    print("✅ Resultado:")
    print("-" * 60)
    print(explanation_es)
    print("-" * 60)
    print()
    
    print("="*60)
    print("✅ Teste concluído!")
    print("="*60)
    print()
    print("💡 O Llama consegue:")
    print("   ✅ Traduzir notícias para qualquer idioma")
    print("   ✅ Explicar de forma simples e conversacional")
    print("   ✅ Adaptar o tom para o público")

if __name__ == "__main__":
    main()
