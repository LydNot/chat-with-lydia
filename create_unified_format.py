#!/usr/bin/env python3
"""
Create a unified training format that combines all three datasets.
Converts everything to a consistent instruction-following format.
"""

import json


def load_jsonl(filepath):
    """Load JSONL file."""
    data = []
    with open(filepath, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data


def create_unified_format():
    """Create a single unified format combining all training data."""
    
    print("Loading datasets...")
    completion_data = load_jsonl('/Users/mox/lydia-clone/blogposts_finetuning.jsonl')
    instruction_data = load_jsonl('/Users/mox/lydia-clone/blogposts_instruction.jsonl')
    qa_data = load_jsonl('/Users/mox/lydia-clone/blogposts_qa.jsonl')
    
    unified_data = []
    
    # Option 1: Unified instruction-following format (most versatile)
    print("\nCreating unified instruction-following format...")
    
    # Convert completion format to instruction format
    for item in completion_data:
        # Extract title from text
        text = item['text']
        if text.startswith('Title: '):
            lines = text.split('\n', 1)
            title = lines[0].replace('Title: ', '').strip()
            content = lines[1].strip() if len(lines) > 1 else text
            
            unified_data.append({
                "prompt": f"Write a blog post titled '{title}':",
                "completion": content
            })
    
    # Instruction format already good, just rename fields
    for item in instruction_data:
        unified_data.append({
            "prompt": item['instruction'],
            "completion": item['output']
        })
    
    # Convert Q&A format to instruction format
    for item in qa_data:
        unified_data.append({
            "prompt": item['question'],
            "completion": item['answer']
        })
    
    return unified_data


def create_simple_text_format():
    """Alternative: Simple text format (for basic completion training)."""
    
    print("\nCreating simple text format...")
    
    completion_data = load_jsonl('/Users/mox/lydia-clone/blogposts_finetuning.jsonl')
    instruction_data = load_jsonl('/Users/mox/lydia-clone/blogposts_instruction.jsonl')
    qa_data = load_jsonl('/Users/mox/lydia-clone/blogposts_qa.jsonl')
    
    simple_data = []
    
    # Completion format - keep as is
    for item in completion_data:
        simple_data.append({
            "text": item['text']
        })
    
    # Instruction format - combine into text
    for item in instruction_data:
        combined_text = f"Instruction: {item['instruction']}\n\nResponse: {item['output']}"
        simple_data.append({
            "text": combined_text
        })
    
    # Q&A format - combine into text
    for item in qa_data:
        combined_text = f"Question: {item['question']}\n\nAnswer: {item['answer']}"
        simple_data.append({
            "text": combined_text
        })
    
    return simple_data


def save_jsonl(data, filepath):
    """Save data as JSONL."""
    with open(filepath, 'w') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')


def main():
    print("="*80)
    print("CREATING UNIFIED TRAINING FORMATS")
    print("="*80)
    
    # Create instruction-following format (RECOMMENDED)
    unified_data = create_unified_format()
    save_jsonl(unified_data, '/Users/mox/lydia-clone/blogposts_unified_instruction.jsonl')
    print(f"✓ Created unified instruction format: {len(unified_data)} examples")
    
    # Create simple text format (ALTERNATIVE)
    simple_data = create_simple_text_format()
    save_jsonl(simple_data, '/Users/mox/lydia-clone/blogposts_unified_simple.jsonl')
    print(f"✓ Created simple text format: {len(simple_data)} examples")
    
    # Calculate stats
    total_chars_inst = sum(len(item['prompt']) + len(item['completion']) for item in unified_data)
    total_chars_simple = sum(len(item['text']) for item in simple_data)
    
    print("\n" + "="*80)
    print("UNIFIED FORMAT COMPARISON")
    print("="*80)
    
    print("\n1. Instruction-Following Format (RECOMMENDED)")
    print("   File: blogposts_unified_instruction.jsonl")
    print(f"   Examples: {len(unified_data)}")
    print(f"   Estimated tokens: {total_chars_inst // 4:,}")
    print(f"   Avg tokens/example: {total_chars_inst // 4 // len(unified_data):,}")
    print("   Format: {'prompt': '...', 'completion': '...'}")
    print("   Best for: Most flexible, works with instruction-following training")
    
    print("\n2. Simple Text Format (ALTERNATIVE)")
    print("   File: blogposts_unified_simple.jsonl")
    print(f"   Examples: {len(simple_data)}")
    print(f"   Estimated tokens: {total_chars_simple // 4:,}")
    print(f"   Avg tokens/example: {total_chars_simple // 4 // len(simple_data):,}")
    print("   Format: {'text': '...'}")
    print("   Best for: Basic completion training")
    
    # Show samples
    print("\n" + "="*80)
    print("SAMPLE FROM UNIFIED INSTRUCTION FORMAT")
    print("="*80)
    for i in [0, len(unified_data)//3, len(unified_data)*2//3]:
        ex = unified_data[i]
        print(f"\nExample {i+1}:")
        print(f"  Prompt: {ex['prompt'][:80]}...")
        print(f"  Completion: {ex['completion'][:100]}...")
    
    print("\n" + "="*80)
    print("✅ UNIFIED FORMATS CREATED!")
    print("="*80)
    print("\nRECOMMENDED: Use blogposts_unified_instruction.jsonl")
    print("             for maximum flexibility with Tinker")


if __name__ == '__main__':
    main()

