#!/usr/bin/env python3
"""
Sample from your finetuned Llama 70B using the CORRECT Tinker API approach.
Based on Tinker docs: https://tinker-docs.thinkingmachines.ai/save-load
"""

import tinker
from tinker import types
import os

# Your REAL checkpoint from 9 hours ago (the original successful training)
CHECKPOINT_PATH = "tinker://5e055c1d-a64d-5886-bb21-d59f26ce83b2:train:0/sampler_weights/ephemeral_175"
BASE_MODEL = "meta-llama/Llama-3.1-70B"

def main():
    if not os.getenv('TINKER_API_KEY'):
        print("ERROR: TINKER_API_KEY not set")
        return
    
    print("="*80)
    print("SAMPLING FROM YOUR REAL FINETUNED LLAMA 70B")
    print("="*80)
    print(f"\nCheckpoint: {CHECKPOINT_PATH}\n")
    
    # Step 1: Create service client
    service_client = tinker.ServiceClient()
    
    # Step 2: Create sampling client from checkpoint (per docs)
    print("Loading sampling client from checkpoint...")
    sampling_client = service_client.create_sampling_client(model_path=CHECKPOINT_PATH)
    print("✓ Loaded!\n")
    
    # Step 3: Get tokenizer (need a separate training client just for this)
    print("Getting tokenizer...")
    tokenizer_client = service_client.create_lora_training_client(base_model=BASE_MODEL)
    tokenizer = tokenizer_client.get_tokenizer()
    print("✓ Tokenizer ready!\n")
    
    # Step 4: Sample
    prompts = [
        "Write a blog post about AI safety:",
        "What are your thoughts on revealed preferences?",
        "Tell me about mutual information:",
    ]
    
    print("="*80)
    print("GENERATING SAMPLES")
    print("="*80)
    
    for i, prompt_text in enumerate(prompts, 1):
        print(f"\n{'─'*80}")
        print(f"PROMPT {i}: {prompt_text}")
        print(f"{'─'*80}\n")
        
        # Encode
        prompt_tokens = tokenizer.encode(prompt_text, add_special_tokens=True)
        prompt_input = types.ModelInput.from_ints(prompt_tokens)
        
        # Sample
        params = types.SamplingParams(max_tokens=500, temperature=0.7, stop=["\n\n\n"])
        result = sampling_client.sample(prompt=prompt_input, sampling_params=params, num_samples=1).result()
        
        # Decode
        response = tokenizer.decode(result.sequences[0].tokens)
        print(response)
        print(f"\n[{len(result.sequences[0].tokens)} tokens]")
    
    print("\n" + "="*80)
    print("COMPLETE!")
    print("="*80)

if __name__ == "__main__":
    main()

