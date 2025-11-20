#!/usr/bin/env python3
"""
Web interface for chatting with Tinker fine-tuned models.
Simple Flask app with a clean chat UI.
"""

from flask import Flask, render_template, request, jsonify, Response
import tinker
from tinker import types
import os
import json
from typing import Generator

app = Flask(__name__)

# Global clients (initialized once)
service_client = None
sampling_client = None
tokenizer = None
current_checkpoint = None

def initialize_model(checkpoint_id: str, base_model: str = "meta-llama/Llama-3.1-70B"):
    """Initialize the Tinker model with given checkpoint."""
    global service_client, sampling_client, tokenizer, current_checkpoint
    
    # Check for API key
    if not os.getenv('TINKER_API_KEY'):
        raise ValueError("TINKER_API_KEY environment variable not set")
    
    print(f"Initializing model with checkpoint: {checkpoint_id}")
    
    # Create service client if needed
    if service_client is None:
        service_client = tinker.ServiceClient()
    
    # Format checkpoint path
    if not checkpoint_id.startswith("tinker://"):
        checkpoint_path = f"tinker://{checkpoint_id}/sampler_weights/ephemeral_175"
    else:
        checkpoint_path = checkpoint_id
    
    # Load sampling client
    sampling_client = service_client.create_sampling_client(model_path=checkpoint_path)
    
    # Get tokenizer (need training client just for this)
    if tokenizer is None:
        tokenizer_client = service_client.create_lora_training_client(base_model=base_model)
        tokenizer = tokenizer_client.get_tokenizer()
    
    current_checkpoint = checkpoint_id
    print(f"✓ Model initialized successfully!")
    
    return True

def generate_response(prompt: str, max_tokens: int = 1500, temperature: float = 0.7, use_stop_sequence: bool = True) -> str:
    """Generate a response from the model."""
    if sampling_client is None or tokenizer is None:
        raise ValueError("Model not initialized. Please set checkpoint ID first.")
    
    # Encode prompt
    prompt_tokens = tokenizer.encode(prompt, add_special_tokens=True)
    prompt_input = types.ModelInput.from_ints(prompt_tokens)
    
    # Sample
    # Using lenient stop sequence to avoid cutting off blog posts
    # 5+ newlines indicates end of content, but allows normal paragraph breaks
    stop_sequences = ["\n\n\n\n\n"] if use_stop_sequence else []
    
    params = types.SamplingParams(
        max_tokens=max_tokens, 
        temperature=temperature, 
        stop=stop_sequences
    )
    result = sampling_client.sample(
        prompt=prompt_input, 
        sampling_params=params, 
        num_samples=1
    ).result()
    
    # Decode
    response = tokenizer.decode(result.sequences[0].tokens)
    return response

@app.route('/')
def index():
    """Render the chat interface."""
    return render_template('index.html')

@app.route('/api/initialize', methods=['POST'])
def api_initialize():
    """Initialize the model with a checkpoint ID."""
    data = request.json
    checkpoint_id = data.get('checkpoint_id', '').strip()
    base_model = data.get('base_model', 'meta-llama/Llama-3.1-70B')
    
    if not checkpoint_id:
        return jsonify({
            'success': False,
            'error': 'Checkpoint ID is required'
        }), 400
    
    try:
        initialize_model(checkpoint_id, base_model)
        return jsonify({
            'success': True,
            'message': f'Model loaded successfully!',
            'checkpoint': current_checkpoint
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """Handle chat messages."""
    data = request.json
    message = data.get('message', '').strip()
    max_tokens = data.get('max_tokens', 1500)
    temperature = data.get('temperature', 0.7)
    use_stop_sequence = data.get('use_stop_sequence', True)
    
    if not message:
        return jsonify({
            'success': False,
            'error': 'Message is required'
        }), 400
    
    if sampling_client is None:
        return jsonify({
            'success': False,
            'error': 'Model not initialized. Please set checkpoint ID first.'
        }), 400
    
    try:
        response = generate_response(message, max_tokens, temperature, use_stop_sequence)
        return jsonify({
            'success': True,
            'response': response
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/status', methods=['GET'])
def api_status():
    """Check if model is initialized."""
    return jsonify({
        'initialized': sampling_client is not None,
        'checkpoint': current_checkpoint
    })

if __name__ == '__main__':
    print("="*80)
    print("TINKER CHAT INTERFACE")
    print("="*80)
    print("\n🚀 Starting Flask server...")
    print("\nOpen http://localhost:5001 in your browser to chat with your model!\n")
    print("Note: Model will be loaded after you enter checkpoint ID in the UI.\n")
    
    # Note: Auto-initialization disabled to allow faster startup
    # Model will be loaded through the web interface
    
    app.run(debug=True, host='0.0.0.0', port=5001)

