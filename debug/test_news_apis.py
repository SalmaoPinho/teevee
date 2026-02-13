"""
Teste de APIs de notícias gratuitas
Testa NewsAPI, RSS feeds e outras fontes
"""
import requests
from datetime import datetime

def test_newsapi():
    """
    Testa NewsAPI (requer chave gratuita)
    https://newsapi.org - 100 requisições/dia grátis
    """
    print("="*60)
    print("📰 Testando NewsAPI")
    print("="*60)
    print()
    
    # NOTA: Você precisa de uma API key gratuita de https://newsapi.org
    API_KEY = "YOUR_API_KEY_HERE"  # Substitua pela sua chave
    
    if API_KEY == "YOUR_API_KEY_HERE":
        print("⚠️ Configure sua API key primeiro!")
        print("   1. Acesse: https://newsapi.org")
        print("   2. Crie conta gratuita")
        print("   3. Copie sua API key")
        print("   4. Substitua em test_news_apis.py")
        return False
    
    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            'apiKey': API_KEY,
            'country': 'us',  # ou 'br' para Brasil
            'pageSize': 5
        }
        
        print("🔍 Buscando top headlines...")
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            
            print(f"✅ Encontradas {len(articles)} notícias:")
            print()
            
            for i, article in enumerate(articles[:3], 1):
                print(f"{i}. {article['title']}")
                print(f"   Fonte: {article['source']['name']}")
                print(f"   URL: {article['url'][:50]}...")
                print()
            
            return True
        else:
            print(f"❌ Erro: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_rss_feeds():
    """
    Testa RSS feeds (100% gratuito, sem API key)
    """
    print("="*60)
    print("📡 Testando RSS Feeds")
    print("="*60)
    print()
    
    feeds = {
        'BBC News': 'http://feeds.bbci.co.uk/news/rss.xml',
        'CNN': 'http://rss.cnn.com/rss/edition.rss',
        'Google News': 'https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en',
        'G1 (Brasil)': 'https://g1.globo.com/rss/g1/'
    }
    
    try:
        import feedparser
        
        for name, url in feeds.items():
            print(f"📰 {name}:")
            print(f"   URL: {url}")
            
            try:
                feed = feedparser.parse(url)
                
                if feed.entries:
                    print(f"   ✅ {len(feed.entries)} notícias encontradas")
                    print(f"   Exemplo: {feed.entries[0].title[:60]}...")
                else:
                    print("   ⚠️ Nenhuma notícia encontrada")
                    
            except Exception as e:
                print(f"   ❌ Erro: {e}")
            
            print()
        
        return True
        
    except ImportError:
        print("❌ feedparser não instalado")
        print("   Execute: pip install feedparser")
        return False

def test_google_news_rss():
    """
    Testa Google News RSS (gratuito, sem API key)
    """
    print("="*60)
    print("🔍 Testando Google News RSS (Detalhado)")
    print("="*60)
    print()
    
    try:
        import feedparser
        
        # Google News RSS por tópico
        topics = {
            'Top Stories': 'https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en',
            'Technology': 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en',
            'Science': 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFptZHpJU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en'
        }
        
        for topic, url in topics.items():
            print(f"📌 {topic}:")
            
            feed = feedparser.parse(url)
            
            if feed.entries:
                print(f"   ✅ {len(feed.entries)} notícias")
                
                # Mostra top 3
                for i, entry in enumerate(feed.entries[:3], 1):
                    print(f"   {i}. {entry.title}")
                    if hasattr(entry, 'published'):
                        print(f"      Data: {entry.published}")
            else:
                print("   ⚠️ Nenhuma notícia")
            
            print()
        
        return True
        
    except ImportError:
        print("❌ feedparser não instalado")
        print("   Execute: pip install feedparser")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    print("="*60)
    print("🌐 Teste de APIs de Notícias")
    print("="*60)
    print()
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = {}
    
    # Testa RSS (não precisa de API key)
    print("\n" + "="*60)
    print("Testando fontes GRATUITAS (sem API key)")
    print("="*60)
    results['RSS Feeds'] = test_rss_feeds()
    results['Google News RSS'] = test_google_news_rss()
    
    # Testa NewsAPI (precisa de API key)
    print("\n" + "="*60)
    print("Testando fontes com API key")
    print("="*60)
    results['NewsAPI'] = test_newsapi()
    
    # Resumo
    print("\n" + "="*60)
    print("📊 Resumo dos Testes")
    print("="*60)
    
    for source, success in results.items():
        status = "✅ Funcionou" if success else "❌ Falhou/Não configurado"
        print(f"{source:20} {status}")
    
    print("\n" + "="*60)
    print("💡 Recomendações:")
    print("="*60)
    print()
    print("1. RSS Feeds (Google News, BBC, CNN)")
    print("   ✅ Gratuito, sem limite")
    print("   ✅ Não precisa de API key")
    print("   ✅ Fácil de usar")
    print("   ⚠️ Menos controle sobre filtros")
    print()
    print("2. NewsAPI")
    print("   ✅ Muito controle (país, categoria, busca)")
    print("   ✅ 100 requisições/dia grátis")
    print("   ⚠️ Precisa de API key")
    print()
    print("📦 Dependências:")
    print("   pip install feedparser requests")

if __name__ == "__main__":
    main()
