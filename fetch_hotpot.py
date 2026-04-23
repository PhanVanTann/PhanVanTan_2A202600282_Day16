import json
import random
from datasets import load_dataset

def main():
    print("Loading HotpotQA dataset...")
    # 'distractor' split contains train/dev, we use dev
    ds = load_dataset("hotpot_qa", "distractor", split="validation")
    
    easy_items = []
    medium_items = []
    hard_items = []
    
    for item in ds:
        # hotpot_qa schema:
        # id: string
        # question: string
        # answer: string
        # type: string
        # level: string (easy, medium, hard)
        # context: dict with 'title' (list) and 'sentences' (list of lists)
        
        level = item.get("level", "medium").lower()
        
        ctx_list = []
        titles = item["context"]["title"]
        sentences = item["context"]["sentences"]
        for t, s_list in zip(titles, sentences):
            ctx_list.append({
                "title": t,
                "text": " ".join(s_list)
            })
            
        formatted_item = {
            "qid": item["id"],
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
