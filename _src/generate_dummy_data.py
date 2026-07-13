import json
import os
import random
from datetime import datetime, timedelta

BREEDS = [
    "Golden Retriever", "French Bulldog", "Labrador Retriever", "German Shepherd", "Poodle",
    "Bulldog", "Rottweiler", "Beagle", "Dachshund", "German Shorthaired Pointer",
    "Pembroke Welsh Corgi", "Australian Shepherd", "Yorkshire Terrier", "Cavalier King Charles Spaniel",
    "Doberman Pinscher", "Boxer", "Miniature Schnauzer", "Cane Corso", "Great Dane", "Shih Tzu",
    "Siberian Husky", "Bernese Mountain Dog", "Pomeranian", "Boston Terrier", "Havanese",
    "English Springer Spaniel", "Shetland Sheepdog", "Brittany", "Pug", "Cocker Spaniel",
    "Miniature American Shepherd", "Border Collie", "Mastiff", "Chihuahua", "Vizsla",
    "Basset Hound", "Belgian Malinois", "Maltese", "Weimaraner", "Collie",
    "Newfoundland", "Rhodesian Ridgeback", "Shiba Inu", "West Highland White Terrier", "Bichon Frise",
    "Bloodhound", "English Cocker Spaniel", "Akita", "Portuguese Water Dog", "Chesapeake Bay Retriever",
    "Dalmatian", "St. Bernard", "Papillon", "Australian Cattle Dog", "Bullmastiff",
    "Samoyed", "Scottish Terrier", "Whippet", "Wirehaired Pointing Griffon", "Great Pyrenees",
    "Giant Schnauzer", "Cardigan Welsh Corgi", "Bull Terrier", "Italian Greyhound", "Airedale Terrier",
    "Old English Sheepdog", "Gordon Setter", "Alaskan Malamute", "Irish Setter", "Boykin Spaniel",
    "Staffordshire Bull Terrier", "Russell Terrier", "Miniature Pinscher", "Lhasa Apso", "Chinese Shar-Pei",
    "Wire Fox Terrier", "Chow Chow", "Irish Wolfhound", "Keeshond", "American Staffordshire Terrier",
    "Anatolian Shepherd Dog", "Greater Swiss Mountain Dog", "Basenji", "Pekingese", "Rat Terrier",
    "Standard Schnauzer", "Borzoi", "Saluki", "Tibetan Terrier", "Tibetan Mastiff",
    "Afghan Hound", "Flat-Coated Retriever", "Pointer", "Brussels Griffon", "Silky Terrier",
    "Bouvier des Flandres", "Beauceron", "American Hairless Terrier", "Dogue de Bordeaux", "Welsh Terrier",
    "Greyhound", "Irish Terrier", "Japanese Chin", "Leonberger", "Manchester Terrier"
]

def generate_articles():
    articles = []
    base_date = datetime.utcnow()
    
    for i, breed in enumerate(BREEDS):
        slug = f"{breed.lower().replace(' ', '-')}-pet-insurance"
        title = f"Best Pet Insurance for {breed}s: Costs, Coverage & Comparisons"
        meta_desc = f"Compare the best pet insurance for {breed}s. Find average costs, coverage options, and top-rated providers to protect your {breed} today."
        
        publish_date = (base_date - timedelta(days=random.randint(1, 300))).strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Determine category based on rough size estimation
        if "Miniature" in breed or "Terrier" in breed or "Chihuahua" in breed or "Pug" in breed or breed in ["Pomeranian", "Maltese", "Havanese", "Shih Tzu"]:
            category = "Small Breeds"
        elif "Mastiff" in breed or "Great" in breed or breed in ["St. Bernard", "Newfoundland", "Leonberger", "Irish Wolfhound"]:
            category = "Giant Breeds"
        else:
            category = "Large & Medium Breeds"
            
        markdown_content = f"""
Choosing the right pet insurance for your {breed} is a crucial step in ensuring they live a long, healthy, and happy life. Known for their unique traits and potential breed-specific health issues, {breed}s require specialized coverage that addresses their specific needs.

## Key Takeaways
- **Average Cost:** Expect to pay between $35 to $75 per month for a {breed}, depending on age and location.
- **Common Health Issues:** Many {breed}s are prone to conditions like hip dysplasia, allergies, and certain cancers.
- **Best Coverage:** Look for policies that cover hereditary conditions, congenital defects, and chronic illnesses without arbitrary limits.

## Why Do {breed}s Need Pet Insurance?
Like all purebred and mixed-breed dogs, {breed}s have a genetic predisposition to certain medical conditions. While they might be healthy as puppies, the cost of veterinary care can skyrocket if they develop a chronic illness or require emergency surgery.

### Common Health Concerns for {breed}s
1. **Joint and Bone Issues:** Many larger or highly active breeds suffer from joint problems.
2. **Skin Allergies and Infections:** A frequent reason for vet visits.
3. **Digestive Issues:** Some breeds have sensitive stomachs.

## Top Pet Insurance Providers for {breed}s
When comparing providers, consider waiting periods, deductible options, and whether exam fees are covered.
- **Provider A:** Best for comprehensive coverage including exam fees.
- **Provider B:** Best budget-friendly option with customizable deductibles.
- **Provider C:** Best for fast claims processing.

## How Much Does It Cost?
The monthly premium for your {breed} will depend on several factors:
- **Age:** Older dogs cost more to insure.
- **Location:** Vet costs vary significantly by zip code.
- **Coverage Limits:** Higher payout limits mean higher premiums.

## What Is Typically Covered?
Most standard accident and illness plans for {breed}s will cover:
- Unexpected surgeries and hospitalizations
- Prescription medications
- Diagnostic tests (X-rays, bloodwork, MRI)
- Treatment for hereditary conditions (if enrolled before symptoms show)

## FAQs
**Is wellness coverage worth it for a {breed}?**
If you plan to use preventative care like vaccinations, flea/tick prevention, and annual checkups, a wellness add-on can help offset these routine costs.

**When is the best time to insure my {breed}?**
The best time is when they are a puppy, before any pre-existing conditions develop. Pre-existing conditions are rarely covered by any provider.
"""
        articles.append({
            "id": i + 1,
            "title": title,
            "slug": slug,
            "breed": breed,
            "meta_description": meta_desc,
            "category": category,
            "author": "Dr. Sarah Jenkins",
            "publish_date": publish_date,
            "content": markdown_content.strip()
        })
        
    # Also add a massive pillar page
    pillar_title = "The Ultimate Guide to Pet Insurance: Compare by Breed"
    articles.append({
        "id": 999,
        "title": pillar_title,
        "slug": "pet-insurance-comparison-guide",
        "breed": "All Breeds",
        "meta_description": "The comprehensive guide to comparing pet insurance for every dog breed. Learn how to choose the best coverage, avoid pitfalls, and save money.",
        "category": "Guides",
        "author": "Editorial Team",
        "publish_date": base_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "content": "This is our massive pillar page linking out to all breed-specific articles..."
    })
    
    with open('_src/_data/articles.json', 'w') as f:
        json.dump(articles, f, indent=4)
        
    print(f"Generated {len(articles)} articles in _src/_data/articles.json")

def generate_site_info():
    site_info = {
        "brand_name": "Pet Insurance Comparison Guide",
        "domain": "pet-insurance-comparison-breed.bongshai.com",
        "url": "https://pet-insurance-comparison-breed.bongshai.com",
        "description": "Find the best pet insurance tailored for your dog's breed. We compare costs, coverage, and provider reviews.",
        "adsense_client_id": "ca-pub-0000000000000000",
        "ga4_measurement_id": "G-XXXXXXXXXX",
        "social": {
            "twitter": "@PetInsureGuide",
            "facebook": "PetInsuranceComparisonGuide"
        },
        "author": {
            "name": "Editorial Team",
            "bio": "Our team of veterinary experts and insurance analysts are dedicated to helping pet parents find the best coverage."
        }
    }
    with open('_src/_data/site.json', 'w') as f:
        json.dump(site_info, f, indent=4)
        
    categories = [
        {"name": "Small Breeds", "slug": "small-breeds", "description": "Pet insurance guides for small dog breeds."},
        {"name": "Large & Medium Breeds", "slug": "large-medium-breeds", "description": "Pet insurance guides for medium and large dog breeds."},
        {"name": "Giant Breeds", "slug": "giant-breeds", "description": "Pet insurance guides for giant dog breeds."},
        {"name": "Guides", "slug": "guides", "description": "Comprehensive pet insurance guides."}
    ]
    with open('_src/_data/categories.json', 'w') as f:
        json.dump(categories, f, indent=4)
        
    print("Generated site.json and categories.json")

if __name__ == "__main__":
    generate_site_info()
    generate_articles()
