import json
import random
from datetime import datetime, timedelta

def load_data(path):
    with open(path, 'r') as f:
        return json.load(f)

def save_data(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

# Spintax components
intros = [
    "When it comes to protecting your {breed}, choosing the right pet insurance is one of the most important decisions you'll make. With their unique traits come specific health risks that require targeted coverage.",
    "The {breed} is an incredible companion, but they aren't immune to health issues. Finding a pet insurance policy that covers the specific conditions common to this breed can save you thousands of dollars in unexpected vet bills.",
    "If you're the proud parent of a {breed}, you already know how special they are. But did you know they are predisposed to certain genetic conditions? That's why securing comprehensive pet insurance early on is vital.",
    "Navigating the world of pet insurance can be confusing, especially when you need coverage tailored for a {breed}. In this guide, we break down exactly what you need to look for to ensure your furry friend is fully protected.",
    "A healthy {breed} is a happy {breed}. To maintain their health without breaking the bank, a solid pet insurance plan is essential. Let's explore the best coverage options for this specific breed."
]

key_takeaways = [
    "- **Average Monthly Premium:** Typically ranges from ${low} to ${high}, heavily dependent on your zip code and the dog's age.\n- **Primary Risks:** Keep an eye out for {issue1} and {issue2}.\n- **Pro Tip:** Enroll while they are still a puppy to avoid pre-existing condition exclusions.",
    "- **Expected Costs:** You can expect premiums between ${low} and ${high} per month.\n- **Breed-Specific Concerns:** {issue1} is particularly prevalent in this breed.\n- **What to Look For:** Ensure your policy covers congenital and hereditary conditions without sub-limits.",
    "- **Monthly Estimate:** ${low} - ${high} depending on the provider.\n- **Common Vet Visits:** Often related to {issue2} and {issue1}.\n- **Best Strategy:** Opt for a higher deductible to lower your monthly premium if you are looking for catastrophic coverage only."
]

why_need = [
    "Like all purebreds and specific mixes, the {breed} has a genetic makeup that makes them susceptible to particular ailments. While they may appear perfectly healthy today, sudden illnesses or accidents can lead to massive veterinary costs.",
    "Every dog breed has its own set of health vulnerabilities. For the {breed}, certain hereditary conditions can lie dormant for years before presenting symptoms. Insurance acts as a financial safety net for these exact scenarios.",
    "Veterinary care costs are rising every year. For a {breed}, treatments for chronic conditions like {issue1} can quickly add up to thousands of dollars. Pet insurance ensures you never have to choose between your wallet and your pet's life."
]

health_issues_map = {
    "Small Breeds": ["dental disease", "luxating patella", "tracheal collapse", "hypoglycemia", "allergies", "heart murmurs"],
    "Large & Medium Breeds": ["hip dysplasia", "elbow dysplasia", "cruciate ligament tears", "bloat (GDV)", "allergies", "cancer"],
    "Giant Breeds": ["severe hip dysplasia", "bloat (gastric dilatation-volvulus)", "bone cancer", "arthritis", "heart conditions"]
}

providers = [
    "## Top Providers for the {breed}\n\nWhen evaluating providers for your {breed}, you should compare the fine print. \n\n- **HealthyPaws:** Excellent for fast claims and no payout caps. Great for covering {issue1}.\n- **Embrace:** Offers a diminishing deductible which is perfect if your dog remains healthy for years.\n- **Trupanion:** Provides direct-to-vet payments, which is a lifesaver for expensive treatments related to {issue2}.",
    "## Best Insurance Options for a {breed}\n\nNot all insurers are created equal. Here are our top picks:\n\n1. **Lemonade:** Incredible AI-driven app, lightning-fast claims, and very competitive rates for the {breed}.\n2. **Spot:** Highly customizable plans where you can adjust your annual limit and deductible.\n3. **ASPCA Pet Health Insurance:** A trusted name with comprehensive coverage that includes behavioral treatments."
]

cost_section = [
    "## Breaking Down the Costs\n\nInsuring a {breed} isn't a one-size-fits-all equation. Your premium is influenced by:\n- **Age:** The older the dog, the higher the risk, and thus the higher the premium.\n- **Location:** Vet care in New York City costs more than in rural Ohio.\n- **Plan Customization:** A 90% reimbursement rate will cost more per month than a 70% rate.",
    "## How Much Will It Cost?\n\nFor a {breed}, costs are generally moderate to high, depending on their risk class. Factors influencing your quote include:\n- **Deductible Choice:** Ranging from $100 to $1000.\n- **Reimbursement Level:** Usually between 70% and 90%.\n- **Local Vet Fees:** Premiums adjust based on the average cost of veterinary care in your specific zip code."
]

faqs = [
    "## Frequently Asked Questions\n\n**Does pet insurance cover routine care for my {breed}?**\nStandard accident and illness plans do not. However, most providers offer an optional wellness rider that covers vaccines, checkups, and flea prevention.\n\n**What are pre-existing conditions?**\nAny illness or injury your {breed} showed symptoms of before the policy effective date (or during the waiting period) is considered pre-existing and won't be covered.",
    "## Common Questions\n\n**Is it too late to insure an older {breed}?**\nWhile it's never too late, premiums for senior dogs are significantly higher, and any existing conditions will be excluded.\n\n**How do claims work?**\nUnlike human health insurance, pet insurance typically requires you to pay the vet bill upfront. You then submit the invoice to your provider for reimbursement."
]

def generate():
    articles = load_data('_data/articles.json')
    
    for article in articles:
        if article['id'] == 999: # Skip the pillar page
            continue
            
        breed = article['breed']
        category = article['category']
        
        # Get random issues based on category
        issues = health_issues_map.get(category, health_issues_map["Large & Medium Breeds"])
        issue1, issue2 = random.sample(issues, 2)
        
        # Determine pricing based on size
        if category == "Small Breeds":
            low, high = random.randint(20, 30), random.randint(45, 60)
        elif category == "Giant Breeds":
            low, high = random.randint(60, 80), random.randint(100, 150)
        else:
            low, high = random.randint(35, 50), random.randint(65, 85)
            
        intro = random.choice(intros).format(breed=breed)
        takeaway = random.choice(key_takeaways).format(low=low, high=high, issue1=issue1, issue2=issue2)
        why = random.choice(why_need).format(breed=breed, issue1=issue1)
        prov = random.choice(providers).format(breed=breed, issue1=issue1, issue2=issue2)
        cost = random.choice(cost_section).format(breed=breed)
        faq = random.choice(faqs).format(breed=breed)
        
        markdown_content = f"""
{intro}

## Key Takeaways
{takeaway}

## Why Do {breed}s Need Pet Insurance?
{why}

### Common Health Concerns for {breed}s
Because of their specific genetics, {breed}s often face:
1. **{issue1.title()}:** A frequent reason for claims among this breed.
2. **{issue2.title()}:** Can require expensive diagnostic imaging and surgery.
3. **Unexpected Accidents:** Broken bones, swallowed objects, and toxin ingestion.

{prov}

{cost}

{faq}
"""
        article['content'] = markdown_content.strip()
        
    save_data(articles, '_data/articles.json')
    print("Regenerated 105 articles with highly varied Spintax content.")

if __name__ == '__main__':
    generate()
