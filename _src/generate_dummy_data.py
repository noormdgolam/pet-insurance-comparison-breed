import json
import os
import random
from datetime import datetime, timedelta

# US Regions and States for Categories
REGIONS = {
    "Northeast": ["New York", "Pennsylvania", "Massachusetts", "New Jersey", "Connecticut", "Maine", "New Hampshire", "Rhode Island", "Vermont"],
    "Midwest": ["Illinois", "Ohio", "Michigan", "Indiana", "Missouri", "Wisconsin", "Minnesota", "Iowa", "Kansas", "Nebraska", "South Dakota", "North Dakota"],
    "South": ["Texas", "Florida", "Georgia", "North Carolina", "Virginia", "Tennessee", "Maryland", "South Carolina", "Alabama", "Louisiana", "Kentucky", "Oklahoma", "Arkansas", "Mississippi", "West Virginia", "Delaware", "Washington DC"],
    "West": ["California", "Washington", "Colorado", "Arizona", "Oregon", "Utah", "Nevada", "New Mexico", "Idaho", "Montana", "Wyoming", "Alaska", "Hawaii"]
}

# 50 States
STATES = [state for region in REGIONS.values() for state in region]

# Top 50 Cities with State and a prominent ZIP Code for flavor
CITIES = [
    ("New York", "NY", "10001"), ("Los Angeles", "CA", "90001"), ("Chicago", "IL", "60601"), 
    ("Houston", "TX", "77001"), ("Phoenix", "AZ", "85001"), ("Philadelphia", "PA", "19101"), 
    ("San Antonio", "TX", "78201"), ("San Diego", "CA", "92101"), ("Dallas", "TX", "75201"), 
    ("San Jose", "CA", "95101"), ("Austin", "TX", "73301"), ("Jacksonville", "FL", "32099"), 
    ("Fort Worth", "TX", "76101"), ("Columbus", "OH", "43201"), ("Charlotte", "NC", "28201"), 
    ("San Francisco", "CA", "94101"), ("Indianapolis", "IN", "46201"), ("Seattle", "WA", "98101"), 
    ("Denver", "CO", "80201"), ("Washington", "DC", "20001"), ("Boston", "MA", "02101"), 
    ("El Paso", "TX", "79901"), ("Nashville", "TN", "37201"), ("Detroit", "MI", "48201"), 
    ("Oklahoma City", "OK", "73101"), ("Portland", "OR", "97201"), ("Las Vegas", "NV", "89101"), 
    ("Memphis", "TN", "38101"), ("Louisville", "KY", "40201"), ("Baltimore", "MD", "21201"), 
    ("Milwaukee", "WI", "53201"), ("Albuquerque", "NM", "87101"), ("Tucson", "AZ", "85701"), 
    ("Fresno", "CA", "93701"), ("Mesa", "AZ", "85201"), ("Sacramento", "CA", "95801"), 
    ("Atlanta", "GA", "30301"), ("Kansas City", "MO", "64101"), ("Colorado Springs", "CO", "80901"), 
    ("Miami", "FL", "33101"), ("Raleigh", "NC", "27601"), ("Omaha", "NE", "68101"), 
    ("Long Beach", "CA", "90801"), ("Virginia Beach", "VA", "23450"), ("Oakland", "CA", "94601"), 
    ("Minneapolis", "MN", "55401"), ("Tulsa", "OK", "74101"), ("Arlington", "TX", "76001"), 
    ("Tampa", "FL", "33601"), ("New Orleans", "LA", "70112")
]

def get_region(state_name):
    for region, states in REGIONS.items():
        if state_name in states:
            return region
    return "National"

def generate_articles():
    articles = []
    base_date = datetime.utcnow()
    article_id = 1
    
    # Generate 50 States
    for state in STATES:
        region = get_region(state)
        slug = f"pet-insurance-rates-in-{state.lower().replace(' ', '-')}"
        title = f"Pet Insurance Rates in {state}: Compare Top Plans & Vet Costs"
        meta_desc = f"Looking for the best pet insurance in {state}? Compare average monthly rates, local vet costs, and top-rated providers to protect your dog or cat."
        
        publish_date = (base_date - timedelta(days=random.randint(1, 300))).strftime("%Y-%m-%dT%H:%M:%SZ")
        
        markdown_content = f"""
Finding affordable pet insurance in **{state}** requires understanding how local vet costs influence your monthly premiums. Whether you live in a bustling city or a quiet rural area, your zip code plays a major role in what you pay.

## Key Takeaways
- **Average Monthly Cost in {state}:** Typically between $40 to $85, heavily influenced by your specific zip code and pet's breed.
- **Local Vet Costs:** Veterinary care in {state} varies; emergency surgeries can cost upwards of $3,000 to $5,000 depending on the clinic.
- **Top Providers:** The best companies in {state} offer flexible deductibles, high reimbursement rates, and comprehensive accident/illness coverage.

## Why Your {state} Zip Code Matters
Pet insurance companies calculate premiums based on the average cost of veterinary care in your specific area. If you live in a high-cost-of-living region within {state}, vets charge more for rent, staff, and supplies, which translates to higher insurance premiums.

### Average Costs by Coverage Type
| Coverage Type | Average Premium | Best For |
| ------------- | --------------- | -------- |
| Accident Only | $15 - $25 / mo  | Budget-conscious owners |
| Accident & Illness | $45 - $80 / mo | Comprehensive protection |
| Wellness Add-on | +$15 - $30 / mo | Routine care & vaccines |

## Top Factors Influencing Rates in {state}
1. **Breed of your pet:** Larger dogs or breeds prone to genetic conditions cost more to insure.
2. **Age:** Enrolling your pet while they are a puppy or kitten locks in lower rates and ensures no pre-existing conditions are excluded.
3. **Coverage Limits:** Choosing a $5,000 annual limit vs. unlimited payouts changes your premium drastically.

## How to Lower Your Pet Insurance Premium
If the rates in {state} feel too high, consider adjusting your policy parameters:
- **Increase your deductible:** Moving from a $250 to a $500 deductible can significantly lower your monthly bill.
- **Lower your reimbursement rate:** Choosing 80% instead of 90% reduces costs.
- **Pay annually:** Many insurers offer a discount for paying your annual premium upfront.

## FAQs
**Is pet insurance required by law in {state}?**
No, pet insurance is entirely optional, but highly recommended to avoid financial stress during medical emergencies.

**Does any {state} pet insurance cover pre-existing conditions?**
Virtually no pet insurance provider covers pre-existing conditions, which is why early enrollment is critical.
"""
        # Generate structured dummy data
        avg_premium = random.randint(35, 75)
        avg_vet_visit = random.randint(150, 300)
        common_local_claim = random.choice(["Lyme Disease", "Heartworm", "Heat Stroke", "Allergic Dermatitis"])

        articles.append({
            "id": article_id,
            "title": title,
            "slug": slug,
            "location_type": "State",
            "location_name": state,
            "region": region,
            "meta_description": meta_desc,
            "category": region,
            "author": "Data Aggregation Team",
            "publish_date": publish_date,
            "content": markdown_content.strip(),
            "local_data": {
                "avg_premium_usd": avg_premium,
                "avg_vet_visit_usd": avg_vet_visit,
                "common_local_claim": common_local_claim
            }
        })
        article_id += 1
        
    # Generate 50 Cities
    for city, state_abbr, zip_code in CITIES:
        slug = f"pet-insurance-rates-in-{city.lower().replace(' ', '-')}-{state_abbr.lower()}-{zip_code}"
        title = f"Pet Insurance Rates in {city}, {state_abbr} (ZIP {zip_code})"
        meta_desc = f"Compare pet insurance rates for {city}, {state_abbr} (ZIP {zip_code}). Find the cheapest and best coverage options for local vet costs in {city}."
        
        publish_date = (base_date - timedelta(days=random.randint(1, 300))).strftime("%Y-%m-%dT%H:%M:%SZ")
        
        markdown_content = f"""
Living in **{city}, {state_abbr} (ZIP {zip_code})** means you have access to some great local veterinarians, but those services can come with a high price tag. Finding the right pet insurance ensures you never have to choose between your wallet and your pet's health.

## Key Takeaways
- **Average Cost for ZIP {zip_code}:** Expect to pay between $45 and $95 per month.
- **Why {city} Rates Differ:** Urban centers typically see higher veterinary costs than rural areas due to higher clinic overhead.
- **Top Picks:** Providers offering fast claims processing and flexible coverage limits are highly rated by {city} pet parents.

## Understanding Vet Costs in {city}
When an emergency strikes in {city}, an unexpected trip to the vet can quickly escalate into the thousands. 

For example, treating a swallowed object or a torn ACL can cost anywhere from $2,500 to $6,000 at a local {city} animal hospital. Pet insurance mitigates these sudden financial shocks by reimbursing up to 90% of your vet bill.

### What Does Pet Insurance Cover?
A standard accident and illness policy in {city} typically covers:
- Emergency care and hospitalizations
- Surgeries and specialist visits
- Prescription medications
- Diagnostic tests (X-rays, MRIs, bloodwork)
- Cancer treatments

*Note: Pre-existing conditions, grooming, and boarding are almost never covered.*

## Finding the Best Rate in {zip_code}
To get the most value out of your pet insurance plan:
1. **Compare Multiple Quotes:** Don't settle for the first quote. Rates can vary wildly between providers for the exact same address in {city}.
2. **Check the Network:** Most pet insurances operate on a reimbursement model, meaning you can visit ANY licensed veterinarian in {city} or anywhere else in the US.
3. **Review the Fine Print:** Look out for arbitrary per-incident limits or restrictive waiting periods.

## FAQs
**Can I use my pet insurance at any vet in {city}?**
Yes! Because pet insurance typically reimburses you directly after you pay the vet, you can use any licensed veterinarian, specialist, or emergency clinic in the country.

**Is it cheaper to insure a cat or a dog in {city}?**
Cats are generally much cheaper to insure than dogs, often costing 30% to 50% less per month.
"""
        avg_premium = random.randint(45, 95)
        avg_vet_visit = random.randint(200, 450)
        common_local_claim = random.choice(["Gastric Torsion", "Hit by Car", "Ingested Foreign Object", "Torn ACL"])

        articles.append({
            "id": article_id,
            "title": title,
            "slug": slug,
            "location_type": "City",
            "location_name": f"{city}, {state_abbr}",
            "region": "Cities",
            "meta_description": meta_desc,
            "category": "Cities",
            "author": "Data Aggregation Team",
            "publish_date": publish_date,
            "content": markdown_content.strip(),
            "local_data": {
                "avg_premium_usd": avg_premium,
                "avg_vet_visit_usd": avg_vet_visit,
                "common_local_claim": common_local_claim,
                "zip_code": zip_code
            }
        })
        article_id += 1
        
    # Also add a massive pillar page
    pillar_title = "The Ultimate Guide to Pet Insurance Rates by ZIP Code"
    articles.append({
        "id": 999,
        "title": pillar_title,
        "slug": "pet-insurance-rates-by-zip-code",
        "location_type": "National",
        "location_name": "United States",
        "region": "Guides",
        "meta_description": "The comprehensive guide to understanding how your ZIP code affects your pet insurance premiums. Compare rates across all 50 states and major cities.",
        "category": "Guides",
        "author": "Data Aggregation Team",
        "publish_date": base_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "content": "This is our massive pillar page linking out to all state and city-specific rate guides...",
        "local_data": {
            "avg_premium_usd": 50,
            "avg_vet_visit_usd": 200,
            "common_local_claim": "General Illness"
        }
    })
    
    with open('_src/_data/articles.json', 'w') as f:
        json.dump(articles, f, indent=4)
        
    print(f"Generated {len(articles)} articles in _src/_data/articles.json")

def generate_site_info():
    site_info = {
        "brand_name": "Pet Insurance Rates Guide",
        "domain": "pet-insurance-rates-zip.bongshai.com",
        "url": "https://pet-insurance-rates-zip.bongshai.com",
        "description": "Find the best pet insurance rates tailored to your ZIP code. We compare costs, coverage, and local vet fees.",
        "adsense_client_id": "ca-pub-0000000000000000",
        "ga4_measurement_id": "G-XXXXXXXXXX",
        "social": {
            "twitter": "@PetInsureRates",
            "facebook": "PetInsuranceRatesGuide"
        },
        "author": {
            "name": "Data Aggregation Team",
            "bio": "Our editorial team aggregates public veterinary cost data and insurance premium estimates to provide transparent, localized guides. We are not licensed financial advisors or veterinarians."
        }
    }
    with open('_src/_data/site.json', 'w') as f:
        json.dump(site_info, f, indent=4)
        
    categories = [
        {"name": "Northeast", "slug": "northeast", "description": "Pet insurance rates in the Northeast US."},
        {"name": "Midwest", "slug": "midwest", "description": "Pet insurance rates in the Midwest US."},
        {"name": "South", "slug": "south", "description": "Pet insurance rates in the Southern US."},
        {"name": "West", "slug": "west", "description": "Pet insurance rates in the Western US."},
        {"name": "Cities", "slug": "cities", "description": "Pet insurance rates in major US cities."},
        {"name": "Guides", "slug": "guides", "description": "Comprehensive pet insurance rate guides."}
    ]
    with open('_src/_data/categories.json', 'w') as f:
        json.dump(categories, f, indent=4)
        
    print("Generated site.json and categories.json")

if __name__ == "__main__":
    generate_site_info()
    generate_articles()
