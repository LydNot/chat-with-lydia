"""
Example configuration file for Chat with Lydia.

Copy this to config.py and customize with your settings.
DO NOT commit config.py to version control!
"""

# Your Tinker API Key (get from https://tinker-console.thinkingmachines.ai)
# Set this as environment variable instead: export TINKER_API_KEY='your-key'
TINKER_API_KEY = None  # Leave as None to use environment variable

# Default model settings
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 1500
DEFAULT_BASE_MODEL = "meta-llama/Llama-3.1-70B"

# Server settings
HOST = '0.0.0.0'
PORT = 5001
DEBUG = True  # Set to False in production

# Model presets (optional)
# Add your frequently used checkpoints here
MODEL_PRESETS = {
    # Example:
    # 'my_model': {
    #     'name': 'My Fine-tuned Model',
    #     'checkpoint': 'your-checkpoint-id:train:0',
    #     'base_model': 'meta-llama/Llama-3.1-70B',
    #     'description': 'Model trained on my data'
    # }
}

