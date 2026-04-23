import json
import random

def main():
    # Load base items
    with open("data/hotpot_mini.json", "r", encoding="utf-8") as f:
        base_data = json.load(f)
        
    easy_bases = [item for item in base_data if item["difficulty"] == "easy"]
    medium_bases = [item for item in base_data if item["difficulty"] == "medium"]
    hard_bases = [item for item in base_data if item["difficulty"] == "hard"]
    
    # We want 33 easy, 33 medium, 34 hard
    generated = []
    
    # Easy
    for i in range(1, 34):
        base = random.choice(easy_bases)
        new_item = dict(base)
        new_item["qid"] = f"generated_easy_{i}"
        generated.append(new_item)
        
    # Medium
    for i in range(1, 34):
        base = random.choice(medium_bases)
        new_item = dict(base)
        new_item["qid"] = f"generated_medium_{i}"
        generated.append(new_item)
        
    # Hard
    for i in range(1, 35):
        base = random.choice(hard_bases)
        new_item = dict(base)
        new_item["qid"] = f"generated_hard_{i}"
        generated.append(new_item)
        
    with open("data/hotpotqa.json", "w", encoding="utf-8") as f:
        json.dump(generated, f, indent=2, ensure_ascii=False)
        
    print(f"Generated {len(generated)} items and saved to data/hotpotqa.json")

if __name__ == "__main__":
    main()
