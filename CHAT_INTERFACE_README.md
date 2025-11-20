# 🤖 Tinker Chat Interface

A beautiful web interface for chatting with your Tinker fine-tuned models!

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Your API Key

```bash
export TINKER_API_KEY='your-api-key-here'
```

### 3. Run the App

```bash
python app.py
```

### 4. Open in Browser

Navigate to: **http://localhost:5000**

## ✨ Features

- **Beautiful Modern UI** - Clean, responsive chat interface
- **Easy Model Loading** - Just paste your checkpoint ID
- **Real-time Chat** - Instant responses from your fine-tuned model
- **Adjustable Parameters** - Control temperature and max tokens
- **Auto-initialization** - Default model loads automatically
- **Mobile Friendly** - Works great on phones and tablets

## 🎯 How to Use

### Loading Your Model

1. Click the **"⚙️ Settings"** button
2. Enter your Tinker checkpoint ID (e.g., `416b24fb-ccc8-5e68-94c8-c080f92b4dc4:train:0`)
3. Select your base model (default: Llama 3.1 70B)
4. Adjust temperature and max tokens if needed
5. Click **"Load Model"**

### Checkpoint ID Format

You can use either format:
- Short: `416b24fb-ccc8-5e68-94c8-c080f92b4dc4:train:0`
- Full: `tinker://416b24fb-ccc8-5e68-94c8-c080f92b4dc4:train:0/sampler_weights/ephemeral_175`

The app will automatically format it correctly!

### Chatting

1. Once the model is loaded, type your message in the input box
2. Press **Enter** or click **"Send"**
3. Wait for the model to respond
4. Continue the conversation!

**Tip:** Use Shift+Enter for new lines in your message.

## ⚙️ Configuration Options

### Temperature (0.0 - 1.0)
- **0.0-0.3**: More focused and deterministic
- **0.7**: Balanced (recommended)
- **0.9-1.0**: More creative and diverse

### Max Tokens (100 - 2000)
- **100-300**: Short responses
- **500**: Medium responses (recommended)
- **1000-2000**: Long, detailed responses

### Base Model Options
- **Llama 3.1 70B**: Best quality (default)
- **Llama 3.1 8B**: Faster, cheaper
- **Llama 3.1 405B**: Highest quality, slower

## 🎨 UI Features

- **Status Indicator**: Shows if model is loaded (green dot)
- **Collapsible Settings**: Keep UI clean while chatting
- **Auto-scroll**: Always see the latest message
- **Loading States**: Visual feedback during processing
- **Error Handling**: Clear error messages if something goes wrong

## 📁 Files

- **`app.py`** - Flask backend server
- **`templates/index.html`** - Chat interface HTML
- **`static/style.css`** - Beautiful styling

## 🔧 Troubleshooting

### "Model not initialized" error
- Make sure you clicked "Load Model" in settings
- Check your checkpoint ID is correct
- Verify TINKER_API_KEY is set

### "TINKER_API_KEY not set" error
```bash
export TINKER_API_KEY='your-key-here'
```

### Model takes too long to load
- First load can take 30-60 seconds
- Subsequent requests are faster
- Check your internet connection

### Port 5000 already in use
```bash
# Kill the process using port 5000
lsof -ti:5000 | xargs kill -9

# Or change the port in app.py:
app.run(debug=True, host='0.0.0.0', port=5001)
```

## 💰 Costs

- **Model loading**: Free (one-time per session)
- **Inference**: ~$0.01 per 1,500 tokens
- Much cheaper than training!

## 🌟 Tips for Best Results

1. **Be specific** in your prompts
2. **Start conversations** with clear context
3. **Adjust temperature** based on your needs
   - Lower for factual/technical content
   - Higher for creative writing
4. **Use your training style** - the model learned from your blog posts!

## 🔒 Security Notes

- Never share your TINKER_API_KEY publicly
- The app runs locally on your machine
- No data is stored or logged
- All requests go directly to Tinker's API

## 🚀 Deployment (Optional)

To deploy to production:

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

### Environment Variables for Production
```bash
export TINKER_API_KEY='your-key'
export FLASK_ENV='production'
export FLASK_DEBUG=0
```

## 📞 Support

- **Tinker Docs**: https://tinker-docs.thinkingmachines.ai/
- **Tinker Console**: https://tinker-console.thinkingmachines.ai

## 🎉 Enjoy!

You now have a beautiful interface to chat with your fine-tuned model. Share it with colleagues, friends, or use it for your own projects!

---

*Built with Flask, Tinker API, and lots of ❤️*

