#!/usr/bin/env python3
"""
Remove low-quality training examples (incomplete summaries, etc.)
"""

import json


def is_bad_example(item):
    """Check if an example is low-quality and should be removed."""
    
    prompt = item.get('prompt', item.get('question', item.get('instruction', '')))
    completion = item.get('completion', item.get('answer', item.get('output', '')))
    
    # Filter out "summarize" prompts with short/incomplete completions
    if 'summarize' in prompt.lower() or 'summary' in prompt.lower():
        # If completion is too short (less than 500 chars), it's probably incomplete
        if len(completion) < 500:
            return True
    
    # Filter out very short completions (likely incomplete)
    if len(completion.strip()) < 200:
        return True
    
    return False


def clean_file(input_file, output_file, format_type='instruction'):
    """Clean a JSONL file by removing bad examples."""
    
    good_examples = []
    bad_examples = []
    
    with open(input_file, 'r') as f:
        for i, line in enumerate(f, 1):
            item = json.loads(line)
            
            if is_bad_example(item):
                bad_examples.append((i, item))
            else:
                good_examples.append(item)
    
    # Save cleaned file
    with open(output_file, 'w') as f:
        for item in good_examples:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    return good_examples, bad_examples


def main():
    print("="*80)
    print("CLEANING BAD TRAINING EXAMPLES")
    print("="*80)
    
    files_to_clean = [
        ('blogposts_qa.jsonl', 'blogposts_qa_cleaned.jsonl', 'qa'),
        ('blogposts_unified_instruction.jsonl', 'blogposts_unified_instruction_cleaned.jsonl', 'instruction'),
        ('blogposts_unified_simple.jsonl', 'blogposts_unified_simple_cleaned.jsonl', 'simple'),
    ]
    
    total_removed = 0
    
    for input_file, output_file, format_type in files_to_clean:
        print(f"\n{'─'*80}")
        print(f"Processing: {input_file}")
        print(f"{'─'*80}")
        
        try:
            good, bad = clean_file(
                f'/Users/mox/lydia-clone/{input_file}',
                f'/Users/mox/lydia-clone/{output_file}',
                format_type
            )
            
            print(f"  Original examples: {len(good) + len(bad)}")
            print(f"  ✓ Good examples kept: {len(good)}")
            print(f"  ✗ Bad examples removed: {len(bad)}")
            
            if bad:
                print(f"\n  Examples of removed items:")
                for i, (line_num, item) in enumerate(bad[:3], 1):
                    prompt = item.get('prompt', item.get('question', item.get('text', '')))
                    completion = item.get('completion', item.get('answer', item.get('text', '')))
                    print(f"    {i}. Line {line_num}:")
                    print(f"       Prompt: {prompt[:70]}...")
                    print(f"       Completion: {completion[:70]}...")
                    print(f"       (Completion length: {len(completion)} chars)")
                
                if len(bad) > 3:
                    print(f"       ... and {len(bad) - 3} more")
            
            total_removed += len(bad)
            
        except FileNotFoundError:
            print(f"  ⚠️  File not found, skipping")
    
    print("\n" + "="*80)
    print(f"CLEANING COMPLETE - Removed {total_removed} bad examples total")
    print("="*80)
    
    print("\n✓ Cleaned files created:")
    print("  - blogposts_qa_cleaned.jsonl")
    print("  - blogposts_unified_instruction_cleaned.jsonl")
    print("  - blogposts_unified_simple_cleaned.jsonl")
    
    print("\nNext: Regenerating unified format with only good examples...")


if __name__ == '__main__':
    main()

