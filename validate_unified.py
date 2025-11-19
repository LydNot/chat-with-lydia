#!/usr/bin/env python3
"""Quick validation of unified formats."""

import json

files = [
    ('blogposts_unified_instruction.jsonl', ['prompt', 'completion']),
    ('blogposts_unified_simple.jsonl', ['text']),
]

for filename, required_fields in files:
    print(f"\n{'='*70}")
    print(f"Validating: {filename}")
    print(f"{'='*70}")
    
    with open(f'/Users/mox/lydia-clone/{filename}', 'r') as f:
        lines = f.readlines()
        print(f"✓ Total examples: {len(lines)}")
        
        # Check first few lines
        for i in range(min(3, len(lines))):
            data = json.loads(lines[i])
            missing = [field for field in required_fields if field not in data]
            if missing:
                print(f"  ❌ Line {i+1}: Missing fields: {missing}")
            else:
                print(f"  ✓ Line {i+1}: All fields present")
        
        # Check last line
        data = json.loads(lines[-1])
        missing = [field for field in required_fields if field not in data]
        if missing:
            print(f"  ❌ Line {len(lines)}: Missing fields: {missing}")
        else:
            print(f"  ✓ Line {len(lines)}: All fields present")

print(f"\n{'='*70}")
print("✅ VALIDATION COMPLETE!")
print(f"{'='*70}")

