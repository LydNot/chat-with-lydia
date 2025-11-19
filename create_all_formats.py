#!/usr/bin/env python3
"""
Create multiple training formats from blog posts:
1. Completion format (already done)
2. Instruction-following format
3. Q&A format
"""

import json


def load_posts():
    """Load the structured blog posts."""
    with open('/Users/mox/lydia-clone/blogposts.json', 'r') as f:
        return json.load(f)


def create_instruction_format(posts):
    """
    Format: Model learns to write blog posts given a topic/title
    Good for: Generating new blog posts in your style
    """
    examples = []
    
    for post in posts:
        # Extract first paragraph or sentence as a prompt hint
        content_lines = post['content'].split('\n\n')
        first_para = content_lines[0] if content_lines else ""
        
        # Multiple instruction variations for diversity
        instructions = [
            f"Write a blog post titled '{post['title']}'",
            f"Create a blog post about: {post['title']}",
            f"Compose a thoughtful essay on '{post['title']}'",
        ]
        
        # Pick one instruction (could rotate through all for more data)
        instruction = instructions[0]
        
        example = {
            "instruction": instruction,
            "output": post['content']
        }
        examples.append(example)
        
        # Optional: Add a variant with a hint from first paragraph
        if len(first_para) > 20 and len(first_para) < 200:
            example_with_hint = {
                "instruction": f"Write a blog post titled '{post['title']}'. Start with: {first_para[:100]}...",
                "output": post['content']
            }
            examples.append(example_with_hint)
    
    return examples


def create_qa_format(posts):
    """
    Format: Model learns to answer questions about your work
    Good for: Creating a chatbot that knows your blog content
    """
    examples = []
    
    for post in posts:
        # Split content into paragraphs
        paragraphs = [p.strip() for p in post['content'].split('\n\n') if p.strip()]
        
        # Generate multiple Q&A pairs per post
        
        # Q1: What did you write about [title]?
        examples.append({
            "question": f"What did you write about {post['title']}?",
            "answer": post['content']
        })
        
        # Q2: Summarize your post on [title]
        # Use first 2-3 paragraphs as summary
        summary = '\n\n'.join(paragraphs[:3]) if len(paragraphs) >= 3 else post['content']
        examples.append({
            "question": f"Can you summarize your thoughts on '{post['title']}'?",
            "answer": summary
        })
        
        # Q3: Tell me about [topic extracted from title]
        examples.append({
            "question": f"Tell me about '{post['title']}'",
            "answer": post['content']
        })
        
        # Q4: What are your views on [title]?
        if len(paragraphs) > 0:
            examples.append({
                "question": f"What are your views on {post['title'].lower()}?",
                "answer": post['content']
            })
    
    return examples


def save_formats(posts):
    """Save all formats."""
    
    print("Creating instruction-following format...")
    instruction_data = create_instruction_format(posts)
    with open('/Users/mox/lydia-clone/blogposts_instruction.jsonl', 'w') as f:
        for example in instruction_data:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')
    print(f"✓ Created {len(instruction_data)} instruction examples")
    
    print("\nCreating Q&A format...")
    qa_data = create_qa_format(posts)
    with open('/Users/mox/lydia-clone/blogposts_qa.jsonl', 'w') as f:
        for example in qa_data:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')
    print(f"✓ Created {len(qa_data)} Q&A examples")
    
    return instruction_data, qa_data


def estimate_tokens(text):
    """Rough token estimation (1 token ≈ 4 characters for English)."""
    return len(text) // 4


def analyze_formats(posts, instruction_data, qa_data):
    """Analyze token counts and statistics for each format."""
    
    # Format 1: Completion (already created)
    completion_tokens = sum(estimate_tokens(f"Title: {p['title']}\n\n{p['content']}") 
                           for p in posts)
    
    # Format 2: Instruction-following
    instruction_tokens = sum(estimate_tokens(
        f"{ex['instruction']}\n{ex['output']}"
    ) for ex in instruction_data)
    
    # Format 3: Q&A
    qa_tokens = sum(estimate_tokens(
        f"{ex['question']}\n{ex['answer']}"
    ) for ex in qa_data)
    
    print("\n" + "="*80)
    print("FORMAT COMPARISON")
    print("="*80)
    
    formats = [
        ("Completion", len(posts), completion_tokens, "blogposts_finetuning.jsonl"),
        ("Instruction-Following", len(instruction_data), instruction_tokens, "blogposts_instruction.jsonl"),
        ("Q&A", len(qa_data), qa_tokens, "blogposts_qa.jsonl"),
    ]
    
    for name, count, tokens, filename in formats:
        print(f"\n{name}:")
        print(f"  File: {filename}")
        print(f"  Examples: {count:,}")
        print(f"  Est. tokens: {tokens:,}")
        print(f"  Avg tokens/example: {tokens // count:,}")
    
    print("\n" + "="*80)
    print("TOTAL ACROSS ALL FORMATS")
    print("="*80)
    total_examples = sum(f[1] for f in formats)
    total_tokens = sum(f[2] for f in formats)
    print(f"Total examples: {total_examples:,}")
    print(f"Total tokens: {total_tokens:,}")
    
    return {
        'completion': {'examples': len(posts), 'tokens': completion_tokens},
        'instruction': {'examples': len(instruction_data), 'tokens': instruction_tokens},
        'qa': {'examples': len(qa_data), 'tokens': qa_tokens},
    }


def main():
    posts = load_posts()
    print(f"Loaded {len(posts)} blog posts\n")
    
    instruction_data, qa_data = save_formats(posts)
    stats = analyze_formats(posts, instruction_data, qa_data)
    
    print("\n" + "="*80)
    print("FILES CREATED")
    print("="*80)
    print("1. blogposts_finetuning.jsonl    - Completion format")
    print("2. blogposts_instruction.jsonl   - Instruction-following format")
    print("3. blogposts_qa.jsonl            - Q&A format")
    
    # Save stats for cost estimation
    with open('/Users/mox/lydia-clone/format_stats.json', 'w') as f:
        json.dump(stats, f, indent=2)
    print("\n✓ Stats saved to format_stats.json")


if __name__ == '__main__':
    main()

