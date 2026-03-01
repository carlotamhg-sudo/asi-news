import feedparser
import google.generativeai as genai
import time

print("🚀 A iniciar a Teia de RSS do All Sides Included (Estilo Minimalista Zen)...\n")

# 1. A TUA CHAVE SECRETA DO GEMINI
MINHA_CHAVE = ''
genai.configure(api_key=MINHA_CHAVE)
modelo_ia = genai.GenerativeModel('gemini-2.5-flash')

# 2. A TUA TEIA DE FONTES (Podes adicionar os links que quiseres!)
lista_de_feeds = [
    "http://feeds.bbci.co.uk/news/world/rss.xml",       # BBC World
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml", # NY Times
    "https://www.theguardian.com/world/rss"             # The Guardian
]

# 3. O PROMPT MÁGICO PARA HTML
instrucao_base = """Act as an impartial news analyst. Read the headline and excerpt. 
Respond ONLY with this exact HTML structure, filling in the content in English:
<div class="box fact"><strong>The Core Fact:</strong> [2-sentence factual summary]</div>
<div class="box advocate"><strong>The Advocate:</strong> [Persuasive paragraph defending it]</div>
<div class="box skeptic"><strong>The Skeptic:</strong> [Critical paragraph against it]</div>
<div class="box observer"><strong>The Observer:</strong> [Neutral paragraph explaining context]</div>
"""

# 4. O CABEÇALHO DO SITE (O Design Minimalista Zen)
html_completo = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>All Sides Included News</title>
    <style>
        body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #FAFAFA; color: #333; max-width: 800px; margin: 0 auto; padding: 40px 20px; }
        h1 { text-align: center; font-size: 36px; border-bottom: 2px solid #ddd; padding-bottom: 20px; letter-spacing: -1px; }
        .fonte { font-size: 14px; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; display: block; }
        .noticia { background: white; padding: 30px; margin-bottom: 40px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
        .titulo-noticia { font-size: 24px; margin-top: 0; color: #111; }
        .box { padding: 15px; margin-bottom: 15px; border-radius: 4px; background-color: #fcfcfc; line-height: 1.6; }
        .fact { border-left: 4px solid #555; }
        .advocate { border-left: 4px solid #2ecc71; background-color: #f4fdf8; }
        .skeptic { border-left: 4px solid #e74c3c; background-color: #fdf4f3; }
        .observer { border-left: 4px solid #3498db; background-color: #f4f9fd; }
    </style>
</head>
<body>
    <h1>All Sides Included News</h1>
    <p style="text-align: center; color: #777;">Different perspectives, one place. Updated daily.</p>
"""

# 5. O MOTOR QUE VAI VARRER A TEIA DE RSS
for url_feed in lista_de_feeds:
    print(f"\n📡 A ligar à fonte: {url_feed}")
    noticias = feedparser.parse(url_feed)
    nome_jornal = noticias.feed.title if 'title' in noticias.feed else "News Source"
    
    # Aqui dizemos para puxar apenas as 2 primeiras notícias de cada jornal (para testar).
    # Mais tarde, muda o [:2] para [:35] para teres mais de 100 notícias no total!
    for artigo in noticias.entries[:2]:
        titulo = artigo.title
        resumo = artigo.description if 'description' in artigo else "No description available."
        
        print(f"🔄 A analisar: {titulo}...")
        
        pergunta = f"{instrucao_base}\nHeadline: {titulo}\nExcerpt: {resumo}"
        resposta = modelo_ia.generate_content(pergunta)
        
        # Montar a caixa da notícia no site
        html_completo += f'<div class="noticia">\n<span class="fonte">{nome_jornal}</span>\n<h2 class="titulo-noticia">{titulo}</h2>\n'
        html_completo += resposta.text
        html_completo += '\n</div>\n'
        
        # Pequena pausa para a IA não bloquear o teu plano gratuito
        time.sleep(3) 

# Fechar o código da página
html_completo += "\n</body>\n</html>"

# 6. GUARDAR O SITE
with open("index.html", "w", encoding='utf-8') as site:
    site.write(html_completo)

print("\n✅ SUCESSO! A Teia funcionou. Abre o teu ficheiro 'index.html' para veres as notícias mundiais!")














