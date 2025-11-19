#!/usr/bin/env python3
"""
Train a Tinker model on your blog posts using the actual Tinker API.
Based on official Tinker documentation and quickstart example.
"""

import json
import os
from typing import List
import tinker
from tinker import types
import numpy as np


def load_training_data(filepath: str) -> List[dict]:
    """Load training data from JSONL file."""
    data = []
    with open(filepath, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data


def process_example(example: dict, tokenizer) -> types.Datum:
    """
    Convert a training example to Tinker's Datum format.
    
    Example input format:
    {
        "prompt": "Write a blog post titled 'AI Safety':",
        "completion": "Today I want to talk about..."
    }
    
    Returns a Datum with:
    - model_input: the input tokens (prompt + completion, shifted)
    - loss_fn_inputs: dict with 'weights' (0 for prompt, 1 for completion) and 'target_tokens'
    """
    
    # Encode prompt and completion separately
    prompt_tokens = tokenizer.encode(example['prompt'], add_special_tokens=True)
    # Add space before completion for natural separation
    completion_tokens = tokenizer.encode(f" {example['completion']}", add_special_tokens=False)
    
    # Weights: 0 for prompt (don't train), 1 for completion (do train)
    prompt_weights = [0] * len(prompt_tokens)
    completion_weights = [1] * len(completion_tokens)
    
    # Combine tokens and weights
    tokens = prompt_tokens + completion_tokens
    weights = prompt_weights + completion_weights
    
    # Shift for next-token prediction
    input_tokens = tokens[:-1]  # Input: all but last token
    target_tokens = tokens[1:]  # Target: all but first token (shifted by 1)
    weights = weights[1:]       # Weights also shift
    
    # Create Datum object
    # Convert to numpy arrays for Tinker
    return types.Datum(
        model_input=types.ModelInput.from_ints(tokens=input_tokens),
        loss_fn_inputs=dict(
            weights=np.array(weights, dtype=np.float32),
            target_tokens=np.array(target_tokens, dtype=np.int64)
        )
    )


def main():
    print("="*80)
    print("TINKER TRAINING - LYDIA'S BLOG")
    print("="*80)
    
    # Configuration
    TRAINING_FILE = "/Users/mox/lydia-clone/blogposts_unified_instruction.jsonl"
    BASE_MODEL = "meta-llama/Llama-3.1-70B"  # Start with 8B model
    NUM_EPOCHS = 3
    LEARNING_RATE = 5e-5
    BATCH_SIZE = 4
    MODEL_NAME = "lydia-blog-llama70b-v1"
    
    # Check for API key
    if not os.getenv('TINKER_API_KEY'):
        print("\n❌ ERROR: TINKER_API_KEY environment variable not set!")
        print("Please set it with: export TINKER_API_KEY='your-api-key-here'")
        print("Get your API key from: https://tinker-console.thinkingmachines.ai")
        return
    
    # Step 1: Connect to Tinker
    print("\n1. Connecting to Tinker...")
    service_client = tinker.ServiceClient()
    
    # List available models
    print("\nAvailable models:")
    for item in service_client.get_server_capabilities().supported_models:
        print(f"  - {item.model_name}")
    
    # Step 2: Create training client with LoRA
    print(f"\n2. Creating training client with model: {BASE_MODEL}")
    training_client = service_client.create_lora_training_client(
        base_model=BASE_MODEL
    )
    
    # Get tokenizer
    tokenizer = training_client.get_tokenizer()
    print(f"   ✓ Tokenizer loaded")
    
    # Step 3: Load and process training data
    print(f"\n3. Loading training data from: {TRAINING_FILE}")
    raw_examples = load_training_data(TRAINING_FILE)
    print(f"   ✓ Loaded {len(raw_examples)} examples")
    
    print("\n4. Processing examples into Tinker format...")
    processed_examples = []
    for i, ex in enumerate(raw_examples):
        try:
            datum = process_example(ex, tokenizer)
            processed_examples.append(datum)
            if i == 0:
                # Show first example for debugging
                print(f"\n   Sample (first example):")
                print(f"   Prompt: {ex['prompt'][:60]}...")
                print(f"   Completion: {ex['completion'][:60]}...")
                print(f"   Input tokens: {len(datum.model_input.to_ints())}")
                print(f"   Target tokens: {len(datum.loss_fn_inputs['target_tokens'])}")
        except Exception as e:
            print(f"   ⚠️  Warning: Failed to process example {i+1}: {e}")
    
    print(f"   ✓ Successfully processed {len(processed_examples)} examples")
    
    # Step 4: Calculate training statistics
    total_tokens = sum(len(ex.model_input.to_ints()) for ex in processed_examples)
    avg_tokens = total_tokens / len(processed_examples)
    total_training_tokens = total_tokens * NUM_EPOCHS
    
    print(f"\n5. Training Statistics:")
    print(f"   Examples: {len(processed_examples)}")
    print(f"   Total tokens: {total_tokens:,}")
    print(f"   Avg tokens/example: {avg_tokens:.0f}")
    print(f"   Epochs: {NUM_EPOCHS}")
    print(f"   Total training tokens: {total_training_tokens:,}")
    
    # Estimate cost (SFT with LoRA is $0.48 per million tokens)
    cost = (total_training_tokens / 1_000_000) * 0.48
    print(f"   Estimated cost: ${cost:.2f}")
    
    # Step 5: Training loop
    print(f"\n6. Starting training (BASE_MODEL: {BASE_MODEL}, EPOCHS: {NUM_EPOCHS})...")
    print("   This may take 10-30 minutes depending on queue...\n")
    
    for epoch in range(NUM_EPOCHS):
        print(f"   Epoch {epoch + 1}/{NUM_EPOCHS}")
        epoch_loss = 0
        num_batches = 0
        
        # Process in batches
        for batch_start in range(0, len(processed_examples), BATCH_SIZE):
            batch_end = min(batch_start + BATCH_SIZE, len(processed_examples))
            batch = processed_examples[batch_start:batch_end]
            
            # Forward and backward pass
            fwdbwd_future = training_client.forward_backward(batch, "cross_entropy")
            optim_future = training_client.optim_step(types.AdamParams(learning_rate=LEARNING_RATE))
            
            # Wait for results
            fwdbwd_result = fwdbwd_future.result()
            optim_result = optim_future.result()
            
            # Calculate loss
            # Convert TensorData to numpy arrays
            logprobs_list = []
            for output in fwdbwd_result.loss_fn_outputs:
                lp = output['logprobs']
                if hasattr(lp, 'tolist'):
                    logprobs_list.extend(lp.tolist())
                else:
                    logprobs_list.append(float(lp))
            
            weights_list = []
            for ex in batch:
                w = ex.loss_fn_inputs['weights']
                if hasattr(w, 'tolist'):
                    weights_list.extend(w.tolist())
                elif isinstance(w, np.ndarray):
                    weights_list.extend(w.tolist())
                else:
                    weights_list.append(float(w))
            
            logprobs = np.array(logprobs_list)
            weights = np.array(weights_list)
            batch_loss = -np.dot(logprobs, weights) / weights.sum()
            
            epoch_loss += batch_loss
            num_batches += 1
            
            if num_batches % 5 == 0:
                print(f"      Batch {num_batches}, Loss: {batch_loss:.4f}")
        
        avg_loss = epoch_loss / num_batches
        print(f"   Epoch {epoch + 1} complete. Avg loss: {avg_loss:.4f}\n")
    
    print("\n7. Training complete! 🎉")
    
    # Step 6: Save model
    print(f"\n8. Saving model as '{MODEL_NAME}'...")
    sampling_client = training_client.save_weights_and_get_sampling_client(name=MODEL_NAME)
    print(f"   ✓ Model saved!")
    
    # Step 7: Test the model
    print("\n9. Testing the finetuned model...")
    test_prompts = [
        "Write a blog post about AI safety:",
        "What are your thoughts on revealed preferences?",
        "Tell me about mutual information:",
    ]
    
    for prompt in test_prompts:
        print(f"\n   Prompt: {prompt}")
        prompt_tokens = tokenizer.encode(prompt, add_special_tokens=True)
        prompt_input = types.ModelInput.from_ints(prompt_tokens)
        params = types.SamplingParams(max_tokens=200, temperature=0.7, stop=["\n\n"])
        
        future = sampling_client.sample(prompt=prompt_input, sampling_params=params, num_samples=1)
        result = future.result()
        
        response = tokenizer.decode(result.sequences[0].tokens)
        print(f"   Response: {response[:150]}...")
    
    print("\n" + "="*80)
    print("✅ TRAINING COMPLETE!")
    print("="*80)
    print(f"\nModel '{MODEL_NAME}' is ready to use!")
    print(f"Total cost: ${cost:.2f}")
    print("\nNext steps:")
    print(f"  1. Test more prompts with your finetuned model")
    print(f"  2. Download weights: tinker download {MODEL_NAME}")
    print(f"  3. Publish weights (optional): tinker publish {MODEL_NAME}")


if __name__ == "__main__":
    main()

