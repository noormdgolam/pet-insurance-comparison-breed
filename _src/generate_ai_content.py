import json
import os
import sys
from datetime import datetime

# Attempt to import dependencies, gracefully failing if missing
try:
    import google.generativeai as genai
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    print("Error: Missing required packages.")
    print("Please run: pip install google-generativeai scikit-learn")
    sys.exit(1)

def load_data(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def check_similarity(new_text, existing_texts):
    if not existing_texts:
        return 0.0
        
    vectorizer = TfidfVectorizer(stop_words='english')
    # Combine existing texts and the new text
    all_texts = existing_texts + [new_text]
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    # Calculate cosine similarity of the new text against all existing texts
    cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()
    max_sim = max(cosine_similarities)
    return max_sim

def generate_article(model, breed, category, attempt=1):
    print(f"Generating unique brief and article for {breed} (Attempt {attempt})...")
    
    prompt = f"""
    You are an expert veterinarian and pet insurance analyst. Write a highly specific, unique, and factual article about "Best Pet Insurance for {breed}s". 
    
    CRITICAL INSTRUCTIONS:
    - DO NOT use a generic templated structure. Vary your H2 and H3 headings.
    - If you use a list, maybe make it a checklist. If you discuss costs, maybe use a Markdown table.
    - Include specific, concrete medical facts that only apply to the {breed}. (e.g., specific genetic diseases, exact life expectancy).
    - Give a real-world scenario of a vet bill this breed might face.
    - Include a "Key Takeaways" section near the top.
    - Include an FAQ section at the bottom.
    - Write the output ENTIRELY in valid Markdown format. Do not wrap it in ```markdown code blocks, just output the raw text.
    - Do not use the exact same opening sentence structure as you would for other breeds. Start with a hook unique to this breed's history or personality.
    """
    
    response = model.generate_content(prompt)
    
    if response and response.text:
        return response.text.strip().removeprefix('```markdown').removeprefix('```').removesuffix('```').strip()
    return ""

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        api_key = input("Please enter your Google Gemini API Key: ").strip()
        
    if not api_key:
        print("API Key is required to run the AI generator.")
        sys.exit(1)
        
    genai.configure(api_key=api_key)
    # Use gemini-1.5-flash for speed and cost-effectiveness
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    articles = load_data('_data/articles.json')
    
    # We will generate in batches to allow review and prevent rate limits
    batch_size = 10
    
    # Track existing content for similarity checking
    existing_contents = []
    
    generated_count = 0
    for article in articles:
        if article['id'] == 999: # Skip pillar page for now
            continue
            
        # Check if already AI generated (you can define a flag, or just overwrite all)
        # For this script, we will just overwrite all if we run it, but we stop after batch_size
        
        breed = article['breed']
        category = article['category']
        
        # Generation Loop (retry if similarity is too high)
        max_attempts = 3
        best_content = ""
        lowest_sim = 1.0
        
        for attempt in range(1, max_attempts + 1):
            content = generate_article(model, breed, category, attempt)
            
            sim_score = check_similarity(content, existing_contents)
            print(f"Similarity Score for {breed}: {sim_score:.2f}")
            
            if sim_score < 0.4:  # Target threshold for uniqueness
                best_content = content
                break
            else:
                if sim_score < lowest_sim:
                    lowest_sim = sim_score
                    best_content = content
                print(f"Content too similar ({sim_score:.2f}). Retrying with different structure instructions...")
                
        # Save the best result we got
        article['content'] = best_content
        existing_contents.append(best_content)
        
        generated_count += 1
        print(f"✅ Successfully completed {breed}\n")
        
        if generated_count >= batch_size:
            break
            
    # Save the updated articles back to JSON
    save_data(articles, '_data/articles_ai.json') # Save to a new file so user can review before replacing
    print(f"\nGenerated a batch of {batch_size} AI articles.")
    print("They have been saved to '_src/_data/articles_ai.json'.")
    print("Please review them. If satisfied, rename the file to 'articles.json' and run 'python generate_site.py'.")

if __name__ == '__main__':
    main()
