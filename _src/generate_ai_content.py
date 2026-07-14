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
    if not existing_texts or not new_text.strip():
        return 0.0
        
    vectorizer = TfidfVectorizer(stop_words='english')
    # Combine existing texts and the new text
    all_texts = existing_texts + [new_text]
    
    try:
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        # Calculate cosine similarity of the new text against all existing texts
        cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()
        max_sim = max(cosine_similarities)
        return max_sim
    except ValueError:
        return 0.0

def generate_article(model, location_name, location_type, category, local_data, attempt=1):
    print(f"Generating unique brief and article for {location_name} (Attempt {attempt})...")
    
    # Extract data securely
    avg_premium = local_data.get('avg_premium_usd', 'N/A')
    avg_vet_visit = local_data.get('avg_vet_visit_usd', 'N/A')
    common_claim = local_data.get('common_local_claim', 'N/A')
    
    prompt = f"""
    You are an editorial assistant writing a data-driven report about "Pet Insurance Rates in {location_name}". 
    
    CRITICAL INSTRUCTIONS:
    - Base your article on the following provided data points for {location_name}:
      - Average Monthly Premium: ${avg_premium}
      - Average Cost of a Vet Visit: ${avg_vet_visit}
      - Common Local Claim/Hazard: {common_claim}
    - DO NOT use a generic templated structure. Vary your H2 and H3 headings.
    - Write an objective analysis explaining WHY these costs exist in this {location_type}.
    - Do not invent or hallucinate other specific costs or statistics. Use only the provided data and general industry knowledge.
    - Give a real-world scenario of a vet bill related to the {common_claim}.
    - Include a "Data Summary" section near the top.
    - Include an FAQ section at the bottom.
    - Write the output ENTIRELY in valid Markdown format. Do not wrap it in ```markdown code blocks.
    """
    
    import time
    
    try:
        response = model.generate_content(prompt)
        time.sleep(15) # Prevent rate limiting (Free tier limit is 5 RPM)
        if response and response.text:
            return response.text.strip().removeprefix('```markdown').removeprefix('```').removesuffix('```').strip()
    except Exception as e:
        print(f"API Error: {e}")
        time.sleep(60) # Wait a full minute on rate limit errors
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
    model = genai.GenerativeModel('gemini-flash-latest')
    
    articles = load_data('_data/articles.json')
    
    # We will generate in batches to allow review and prevent rate limits
    batch_size = 150
    
    # Track existing content for similarity checking
    existing_contents = []
    
    generated_count = 0
    for article in articles:
        if article['id'] == 999: # Skip pillar page for now
            continue
            
        # Check if already AI generated (you can define a flag, or just overwrite all)
        # For this script, we will just overwrite all if we run it, but we stop after batch_size
        
        location_name = article.get('location_name', 'Unknown Location')
        location_type = article.get('location_type', 'Region')
        category = article['category']
        local_data = article.get('local_data', {})
        
        # Generation Loop (retry if similarity is too high)
        max_attempts = 3
        best_content = ""
        lowest_sim = 1.0
        
        for attempt in range(1, max_attempts + 1):
            content = generate_article(model, location_name, location_type, category, local_data, attempt)
            
            sim_score = check_similarity(content, existing_contents)
            print(f"Similarity Score for {location_name}: {sim_score:.2f}")
            
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
        print(f"Successfully completed {location_name}\n")
        
        if generated_count >= batch_size:
            break
            
    # Save the updated articles back to JSON
    save_data(articles, '_data/articles_ai.json') # Save to a new file so user can review before replacing
    print(f"\nGenerated a batch of {batch_size} AI articles.")
    print("They have been saved to '_src/_data/articles_ai.json'.")
    print("Please review them. If satisfied, rename the file to 'articles.json' and run 'python generate_site.py'.")

if __name__ == '__main__':
    main()
