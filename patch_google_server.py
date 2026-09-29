import sys, re
sys.stdout.reconfigure(encoding='utf-8')

google_api_code = '''
# ==================== GOOGLE SEARCH OFFICIAL APIS ====================

@app.get("/api/google/suggest")
def google_suggest(q: str = ""):
    query = (q or "").strip().lower()
    
    trending = [
        "Google Gemini 2.0 release date",
        "ICC Cricket World Cup standings",
        "Python 3.13 new features",
        "Weather forecast today",
        "Chandrayaan ISRO space mission",
        "Google Pixel 9 Pro Fold review",
        "Best movies streaming this week",
        "Stock market trends Nifty Sensex",
        "Machine Learning roadmap 2026",
        "Translate English to Tamil"
    ]
    
    suggestions_map = {
        "g": ["google", "gmail", "google drive", "google maps", "google translate", "google flights", "gemini ai", "google sheets"],
        "go": ["google", "google search", "google finance", "google photos", "google classroom", "golang tutorial", "google store"],
        "goo": ["google", "google account", "google docs", "google meet", "google news", "google trends", "google play"],
        "goog": ["google", "google search engine", "google cloud", "google workspace", "google scholar"],
        "p": ["python", "pinterest", "paypal", "premier league", "play store", "perplexity ai", "pixel 9"],
        "py": ["python download", "python documentation", "python tutorial w3schools", "pytorch", "pyside6", "python compiler"],
        "pyt": ["python tutorial", "python list methods", "python dict comprehension", "python virtualenv"],
        "w": ["weather", "wikipedia", "wordle", "whatsapp web", "world clock", "wall street journal"],
        "c": ["calculator", "canva", "chatgpt", "cricket score", "currency converter", "coursera", "cricbuzz"],
        "t": ["translate", "twitter", "time now", "timer 5 minutes", "top news", "tiktok", "tamil news"],
        "a": ["amazon", "apple", "artificial intelligence", "air india", "airbnb", "adobe"],
        "i": ["india weather", "instagram", "imdb", "isro missions", "income tax portal", "iphone 16"]
    }
    
    if not query:
        return {"query": "", "suggestions": trending[:6]}
        
    if query in suggestions_map:
        return {"query": query, "suggestions": suggestions_map[query]}
        
    # Generic filter
    matches = [t for t in trending if query in t.lower()]
    if not matches:
        matches = [
            f"{query}",
            f"{query} download",
            f"{query} online",
            f"{query} meaning",
            f"{query} official website",
            f"{query} tutorial",
            f"{query} wikipedia"
        ]
    return {"query": query, "suggestions": matches[:6]}


@app.get("/api/google/search")
def google_search(q: str = "", category: str = "all"):
    query = (q or "").strip()
    if not query:
        query = "Google"

    import time
    start_time = time.time()
    
    q_lower = query.lower()
    
    # Specific knowledge graphs
    knowledge = None
    if any(k in q_lower for k in ["google", "alphabet"]):
        knowledge = {
            "title": "Google",
            "subtitle": "Technology company",
            "description": "Google LLC is an American multinational corporation and technology company focusing on online advertising, search engine technology, cloud computing, computer software, quantum computing, e-commerce, consumer electronics, and artificial intelligence.",
            "image": "https://images.unsplash.com/photo-1573804633927-bfcbcd909acd?w=600&q=80",
            "attributes": [
                {"label": "Founders", "value": "Larry Page, Sergey Brin"},
                {"label": "CEO", "value": "Sundar Pichai (Oct 2, 2015–)"},
                {"label": "Parent organization", "value": "Alphabet Inc."},
                {"label": "Founded", "value": "September 4, 1998, Menlo Park, California, USA"},
                {"label": "Headquarters", "value": "Mountain View, California, United States"}
            ]
        }
    elif any(k in q_lower for k in ["python", "programming"]):
        knowledge = {
            "title": "Python",
            "subtitle": "High-level programming language",
            "description": "Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation. Python is dynamically typed and garbage-collected.",
            "image": "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=600&q=80",
            "attributes": [
                {"label": "Designed by", "value": "Guido van Rossum"},
                {"label": "First appeared", "value": "February 20, 1991 (35 years ago)"},
                {"label": "Typing discipline", "value": "Duck, dynamic, strong typing"},
                {"label": "Major implementations", "value": "CPython, PyPy, Jython, IronPython"}
            ]
        }
    elif any(k in q_lower for k in ["ai", "artificial intelligence", "gemini"]):
        knowledge = {
            "title": "Artificial Intelligence",
            "subtitle": "Academic discipline & field of computer science",
            "description": "Artificial intelligence (AI) is the intelligence of machines or software, as opposed to the intelligence of living beings, primarily of humans. It is also an academic field of study in computer science.",
            "image": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=600&q=80",
            "attributes": [
                {"label": "Leading Labs", "value": "Google DeepMind, Google Research"},
                {"label": "State-of-the-Art", "value": "Gemini 2.0, Transformer Architectures"},
                {"label": "Key Applications", "value": "Computer vision, Natural language processing, Robotics, Autonomous vehicles"}
            ]
        }
    elif any(k in q_lower for k in ["india"]):
        knowledge = {
            "title": "India",
            "subtitle": "Country in South Asia",
            "description": "India, officially the Republic of India, is a country in South Asia. It is the seventh-largest country by area; the most populous country in the world; and since the time of its independence in 1947, the world's most populous democracy.",
            "image": "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=600&q=80",
            "attributes": [
                {"label": "Capital", "value": "New Delhi"},
                {"label": "Prime Minister", "value": "Narendra Modi"},
                {"label": "President", "value": "Droupadi Murmu"},
                {"label": "Currency", "value": "Indian Rupee (₹)"}
            ]
        }
    
    # Organic results generator
    organic_results = [
        {
            "title": f"{query} — Official Overview & Latest Updates",
            "url": f"https://www.google.com/search?q={query}",
            "displayed_url": f"https://www.google.com › {query.lower().replace(' ', '-')}",
            "snippet": f"Explore official information, features, documentation, and the latest news about {query}. Find comprehensive insights, guides, and related resources.",
            "sitelinks": [
                {"title": "Documentation & Guides", "snippet": "Official technical specifications and getting started manuals."},
                {"title": "Latest News & Releases", "snippet": "Recent developments, announcements, and version updates."},
                {"title": "Community & Support", "snippet": "Official discussion forums, FAQ, and global user community."},
                {"title": "Downloads & Tools", "snippet": "Certified tools, SDKs, and developer kits."}
            ]
        },
        {
            "title": f"{query} - Wikipedia, the free encyclopedia",
            "url": f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}",
            "displayed_url": f"https://en.wikipedia.org › wiki › {query.replace(' ', '_')}",
            "snippet": f"{query} is a prominent subject with extensive global recognition. Read the historical background, development timeline, applications, and verified citations on Wikipedia.",
            "sitelinks": []
        },
        {
            "title": f"Top News, Trends, and Stories on {query}",
            "url": f"https://news.google.com/search?q={query}",
            "displayed_url": f"https://news.google.com › stories › {query.lower()}",
            "snippet": f"Real-time news updates, editorial analysis, and press releases about {query}. Follow breaking headlines and expert opinions from leading international publications.",
            "sitelinks": []
        },
        {
            "title": f"Google Cloud & DeepMind Innovations in {query}",
            "url": f"https://cloud.google.com/solutions/{query.lower()}",
            "displayed_url": f"https://cloud.google.com › solutions › {query.lower()}",
            "snippet": f"Harness Google's world-class cloud infrastructure, AI models, and enterprise security to accelerate your projects with {query}.",
            "sitelinks": []
        },
        {
            "title": f"GitHub - Trending Open-Source Projects for {query}",
            "url": f"https://github.com/topics/{query.lower()}",
            "displayed_url": f"https://github.com › topics › {query.lower()}",
            "snippet": f"Explore open-source repositories, libraries, star ratings, and community contributions for {query}. Collaborate with developers worldwide.",
            "sitelinks": []
        }
    ]
    
    # Image results
    images_results = [
        {"title": f"{query} Showcase 1", "thumbnail": "https://images.unsplash.com/photo-1573804633927-bfcbcd909acd?w=400&q=80", "source": "google.com"},
        {"title": f"{query} Technology", "thumbnail": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=400&q=80", "source": "techcrunch.com"},
        {"title": f"{query} Infrastructure", "thumbnail": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=400&q=80", "source": "wikipedia.org"},
        {"title": f"{query} Future Concept", "thumbnail": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=400&q=80", "source": "theverge.com"},
        {"title": f"{query} Global Impact", "thumbnail": "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?w=400&q=80", "source": "nature.com"},
        {"title": f"{query} Innovation Lab", "thumbnail": "https://images.unsplash.com/photo-1531482615713-2afd69097998?w=400&q=80", "source": "wired.com"}
    ]
    
    # Video results
    videos_results = [
        {"title": f"What is {query}? Complete Beginner to Master Guide", "channel": "Google Developers", "duration": "14:28", "views": "1.4M views", "thumbnail": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=500&q=80"},
        {"title": f"The Evolution of {query} in 2026 and Beyond", "channel": "Tech Vision", "duration": "21:05", "views": "850K views", "thumbnail": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=500&q=80"},
        {"title": f"{query} Keynote Demonstration & Deep Dive", "channel": "Google I/O", "duration": "48:12", "views": "3.2M views", "thumbnail": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=500&q=80"}
    ]
    
    # News results
    news_results = [
        {"title": f"Major Breakthrough Announced for {query} Ecosystem", "source": "Reuters", "time": "2 hours ago", "snippet": f"Industry leaders convene as groundbreaking innovations around {query} redefine speed, accessibility, and scalability."},
        {"title": f"How {query} is Transforming Global Enterprise Operations", "source": "Bloomberg", "time": "5 hours ago", "snippet": f"A comprehensive report reveals a 45% productivity surge among early adopters of modern {query} architectures."},
        {"title": f"Next Generation Technologies: What {query} Means for Tomorrow", "source": "The Verge", "time": "14 hours ago", "snippet": f"Analysts highlight pivotal trends and anticipated feature sets scheduled for rollout across international markets."}
    ]
    
    # People Also Ask
    people_also_ask = [
        {"question": f"What is {query} used for?", "answer": f"{query} is widely adopted for accelerating digital transformation, engineering scalable solutions, and providing streamlined access to knowledge and tools worldwide."},
        {"question": f"Is {query} free to access and use?", "answer": f"Yes, core public features, documentation, and standard services for {query} are freely accessible to users across all major platforms."},
        {"question": f"How can I get started with {query}?", "answer": f"You can get started by visiting the official documentation or platform portal, exploring introductory tutorials, and following community best practices."},
        {"question": f"What are the best alternatives to {query}?", "answer": f"Depending on your workflow, related solutions offer specialized capabilities, though {query} remains the industry benchmark for overall reliability and coverage."}
    ]
    
    # Related searches
    related = [
        f"{query} official website",
        f"{query} download windows",
        f"{query} tutorial for beginners",
        f"{query} github open source",
        f"{query} latest news 2026",
        f"{query} price & specs",
        f"{query} vs competitor comparison",
        f"{query} api documentation"
    ]
    
    duration = round(time.time() - start_time + 0.32, 2)
    
    return {
        "query": query,
        "category": category,
        "total_results": "3,420,000,000",
        "search_time": f"{duration} seconds",
        "knowledge_panel": knowledge,
        "organic_results": organic_results,
        "images_results": images_results,
        "videos_results": videos_results,
        "news_results": news_results,
        "people_also_ask": people_also_ask,
        "related_searches": related
    }

# ==================== END GOOGLE SEARCH APIS ====================
'''

with open('server.py', 'r', encoding='utf-8') as f:
    server_code = f.read()

target = '@app.get("/{full_path:path}")'
if target in server_code and '/api/google/search' not in server_code:
    server_code = server_code.replace(target, google_api_code + '\n' + target)
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(server_code)
    print("Google Search APIs added to server.py successfully!")
else:
    print("Target not found or already added")
