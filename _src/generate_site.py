import os
import json
import shutil
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import markdown

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_data(file_name):
    path = os.path.join('_data', file_name)
    with open(path, 'r') as f:
        return json.load(f)

def build_site():
    print("Building site...")
    
    # Setup Jinja2 env
    env = Environment(loader=FileSystemLoader('_templates'))
    env.filters['markdown'] = lambda text: markdown.markdown(text)
    
    # Output dir is root
    output_dir = '..'
    
    # Load Data
    site_info = load_data('site.json')
    categories = load_data('categories.json')
    articles = load_data('articles.json')
    
    # Create search index
    search_index = []
    
    # Pre-process articles
    for article in articles:
        # Convert markdown to html for content
        article['content_html'] = markdown.markdown(article['content'])
        search_index.append({
            "title": article['title'],
            "url": f"/{article['slug']}.html",
            "description": article['meta_description'],
            "category": article['category']
        })
        
    # Render index.html
    index_template = env.get_template('index.html')
    with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_template.render(
            site=site_info, 
            categories=categories, 
            articles=articles[:10],
            all_articles=articles
        ))
        
    # Render static pages
    static_pages = [
        ('about.html', 'About Us', 'Learn more about Pet Insurance Comparison Guide and our expert team.', 'about'),
        ('contact.html', 'Contact Us', 'Get in touch with the Pet Insurance Comparison Guide team.', 'contact'),
        ('privacy-policy.html', 'Privacy Policy', 'Read our privacy policy and learn how we protect your data.', 'privacy'),
        ('terms.html', 'Terms of Service', 'Terms of Service for Pet Insurance Comparison Guide.', 'terms'),
        ('disclaimer.html', 'Disclaimer', 'Important disclaimers and FTC disclosures.', 'disclaimer'),
        ('404.html', 'Page Not Found', 'The page you are looking for does not exist.', '404'),
        ('search.html', 'Search', 'Search for pet insurance by breed.', 'search')
    ]
    page_template = env.get_template('page.html')
    for filename, title, desc, page_id in static_pages:
        with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
            f.write(page_template.render(
                site=site_info, 
                title=title, 
                meta_description=desc, 
                page_id=page_id,
                categories=categories
            ))
            
    # Render categories
    cat_template = env.get_template('category.html')
    for cat in categories:
        cat_articles = [a for a in articles if a['category'] == cat['name']]
        with open(os.path.join(output_dir, f"{cat['slug']}.html"), 'w', encoding='utf-8') as f:
            f.write(cat_template.render(
                site=site_info, 
                category=cat, 
                articles=cat_articles,
                categories=categories
            ))
            
    # Render articles
    article_template = env.get_template('article.html')
    for article in articles:
        # Get related articles
        related = [a for a in articles if a['category'] == article['category'] and a['id'] != article['id']][:3]
        
        with open(os.path.join(output_dir, f"{article['slug']}.html"), 'w', encoding='utf-8') as f:
            f.write(article_template.render(
                site=site_info, 
                article=article, 
                related_articles=related,
                categories=categories
            ))
            
    # Write search index
    with open(os.path.join(output_dir, 'search_index.json'), 'w', encoding='utf-8') as f:
        json.dump(search_index, f)
        
    # Render Sitemap
    sitemap_template = env.get_template('sitemap.xml')
    with open(os.path.join(output_dir, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(sitemap_template.render(
            site=site_info, 
            articles=articles, 
            categories=categories,
            static_pages=static_pages,
            date=datetime.utcnow().strftime("%Y-%m-%d")
        ))
        
    # Render RSS
    rss_template = env.get_template('rss.xml')
    with open(os.path.join(output_dir, 'rss.xml'), 'w', encoding='utf-8') as f:
        f.write(rss_template.render(
            site=site_info, 
            articles=articles,
            date=datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        ))
        
    # Copy Assets
    print("Copying assets...")
    assets_src = '_assets'
    
    # Copy directories
    for d in ['css', 'js', 'images']:
        src_d = os.path.join(assets_src, d)
        dst_d = os.path.join(output_dir, d)
        if os.path.exists(dst_d):
            shutil.rmtree(dst_d)
        shutil.copytree(src_d, dst_d)
        
    # Copy root level assets (sw.js, manifest.json, robots.txt)
    for f in ['sw.js', 'manifest.json', 'robots.txt']:
        src_f = os.path.join(assets_src, f)
        if os.path.exists(src_f):
            shutil.copy2(src_f, os.path.join(output_dir, f))
            
    print("Build complete.")

if __name__ == '__main__':
    build_site()
