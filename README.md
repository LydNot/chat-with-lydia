# 🤖 Chat with Lydia

A beautiful web interface for chatting with fine-tuned AI models using [Tinker AI](https://tinker-docs.thinkingmachines.ai/).

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)

## ✨ Features

- 🎨 **Beautiful Modern UI** - Clean purple gradient design with smooth animations
- 💬 **Real-time Chat** - Instant responses from your fine-tuned models
- ⚙️ **Flexible Settings** - Control temperature, max tokens, and model selection
- 📱 **Mobile Responsive** - Works perfectly on phones, tablets, and desktop
- 🔧 **Easy Setup** - Get started in under 5 minutes
- 🚀 **Production Ready** - Deploy to any cloud platform

## 🎯 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/LydNot/chat-with-lydia.git
cd chat-with-lydia
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Your Tinker API Key

```bash
export TINKER_API_KEY='your-api-key-here'
```

Get your API key from the [Tinker Console](https://tinker-console.thinkingmachines.ai).

### 4. Run the App

```bash
python3 app.py
```

### 5. Open in Browser

Navigate to: **http://localhost:5001**

## 📖 Usage

### Loading a Model

1. Click the **"⚙️ Settings"** button
2. Enter your Tinker checkpoint ID (format: `xxxxx-xxxxx-xxxxx:train:0`)
3. Select your base model (Llama 3.1 8B/70B/405B)
4. Adjust temperature and max tokens as needed
5. Click **"Load Model"** (takes 15-30 seconds)
6. Start chatting!

### Checkpoint ID Format

Your Tinker checkpoint ID looks like this:
```
416b24fb-ccc8-5e68-94c8-c080f92b4dc4:train:0
```

You can find it in the Tinker Console after training your model.

### Customizing Settings

- **Temperature** (0.0-1.0): Controls creativity
  - Lower (0.3-0.5) = More focused and deterministic
  - Higher (0.7-0.9) = More creative and diverse

- **Max Tokens** (200-4000): Controls response length
  - 500 tokens ≈ 1-2 paragraphs
  - 1500 tokens ≈ 2-3 pages (recommended)
  - 4000 tokens ≈ 6-8 pages

- **Auto-stop**: When checked, stops at natural ending points

## 🎨 Adding Your Own Models

Edit `templates/index.html` to add preset models:

```javascript
const modelPresets = {
    'your_model': {
        name: "Your Model Name",
        checkpoint: 'your-checkpoint-id:train:0',
        baseModel: 'meta-llama/Llama-3.1-70B',
        description: 'Description here'
    }
};
```

Then add to the dropdown:

```html
<option value="your_model">Your Model Name (Llama 70B)</option>
```

## 🚀 Deployment

### Deploy to Render.com (Recommended)

**Get your app online in 5 minutes!**

1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repo: `chat-with-lydia`
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Environment Variable**: `TINKER_API_KEY` = your-key
5. Click "Create Web Service"
6. Wait 2-5 minutes - done! 🎉

**Full guide**: See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for detailed step-by-step instructions.

### Local Development
```bash
python3 app.py
```

### Other Deployment Options

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for:
- Railway
- Heroku
- Google Cloud Run
- AWS Elastic Beanstalk
- DigitalOcean

### Environment Variables

Required:
- `TINKER_API_KEY` - Your Tinker API key

Optional:
- `FLASK_ENV` - Set to `production` for deployment
- `PYTHON_VERSION` - Set to `3.10.0` for consistency

## 🛠️ Development

### Project Structure

```
chat-with-lydia/
├── app.py                  # Flask backend
├── templates/
│   └── index.html         # Chat interface
├── static/
│   └── style.css          # Styling
├── requirements.txt       # Dependencies
├── start_chat.sh         # Startup script
└── README.md             # This file
```

### API Endpoints

- `POST /api/initialize` - Initialize model with checkpoint
- `POST /api/chat` - Send message and get response
- `GET /api/status` - Check if model is loaded

### Technologies Used

- **Backend**: Flask, Tinker SDK, Python 3.8+
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **AI**: Tinker API for model inference

## 📚 Documentation

- **Quick Start**: See above
- **Full Guide**: [CHAT_INTERFACE_README.md](CHAT_INTERFACE_README.md)
- **Usage Examples**: [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)
- **Tinker Docs**: [tinker-docs.thinkingmachines.ai](https://tinker-docs.thinkingmachines.ai/)

## 💡 Tips

- First model load takes 15-30 seconds - this is normal
- Subsequent messages are much faster (2-5 seconds)
- Use temperature 0.7 for balanced responses
- Set max tokens to 1500-2000 for full blog posts
- Uncheck auto-stop for maximum length output

## 🔒 Security

- Never commit your `TINKER_API_KEY` to the repository
- Always use environment variables for sensitive data
- The `.gitignore` file is configured to exclude sensitive files
- In production, use HTTPS and proper authentication

## 💰 Costs

- **Model loading**: Free (one-time per session)
- **Inference**: ~$0.01 per 1,500 tokens
- Much cheaper than training!

Typical usage:
- 100 messages/day ≈ $0.50-$1.50
- 3000 messages/month ≈ $15-$45

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

MIT License - feel free to use this project for any purpose.

## 🙏 Acknowledgments

- Built with [Tinker AI](https://tinker-docs.thinkingmachines.ai/)
- Flask web framework
- Inspired by modern chat interfaces

## 📞 Support

- **Issues**: Open an issue on GitHub
- **Tinker Support**: [Tinker Console](https://tinker-console.thinkingmachines.ai)
- **Documentation**: See the docs folder

## 🎉 Demo

Want to see it in action? Check out the visual demo in [DEMO.md](DEMO.md).

---

**Built with ❤️ for the AI community**

*Ready to chat with your fine-tuned models!* 🚀

