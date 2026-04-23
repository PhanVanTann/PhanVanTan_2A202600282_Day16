import json
import urllib.request

def main():
    url = "http://curtis.ml.cmu.edu/datasets/hotpot/hotpot_dev_distractor_v1.json"
    print(f"Downloading HotpotQA from {url}...")
    req = urllib.request.urlopen(url)
    data = json.loads(req.read().decode('utf-8'))
    
    print(f"Downloaded {len(data)} items. Parsing...")
    easy_items = []
    medium_items = []
    hard_items = []
    
    for item in data:
        level = item.get("level", "medium").lower()
        
        ctx_list = []
        for ctx in item.get("context", []):
            title = ctx[0]
            sentences = ctx[1]
            ctx_list.append({
                "title": title,
                "text": " ".join(sentences)
            })
            
        formatted_item = {
            "qid": item["_id"],
            "difficulty": level,
            "question": item["question"],
            "gold_answer": item["answer"],
            "context": ctx_list
        }
        
        if level == "easy" and len(easy_items) < 33:
            easy_items.append(formatted_item)
        elif level == "medium" and len(medium_items) < 33:
            medium_items.append(formatted_item)
        elif level == "hard" and len(hard_items) < 34:
            hard_items.append(formatted_item)
            
        if len(easy_items) == 33 and len(medium_items) == 33 and len(hard_items) == 34:
            break
            
    # Sort by difficulty
    result = easy_items + medium_items + hard_items
    
    with open("data/hotpotqa.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
        
    print(f"Saved {len(result)} items to data/hotpotqa.json")

if __name__ == "__main__":
    main()
