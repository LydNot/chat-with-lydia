# 💬 Tinker Chat Interface - Usage Examples

## What the Interface Looks Like

### Main Screen

```
┌─────────────────────────────────────────────────────┐
│                  🤖 Tinker Chat                      │
│            Chat with your fine-tuned model           │
│                                                      │
│    Status: ● Ready: 5e055c1d-a64d...                │
│                                   [⚙️ Settings]     │
└─────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────┐
│                                                      │
│  👤  Write a blog post about AI safety:             │
│  ┌──────────────────────────────────────────────┐  │
│  │  Today I was fortunate enough to hear from   │  │
│  │  a law student interested in avoiding        │  │
│  │  catastrophic existential risk from          │  │
│  │  superintelligence...                        │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  🤖  What are your thoughts on revealed             │
│      preferences?                                    │
│  ┌──────────────────────────────────────────────┐  │
│  │  Revealed preferences is a fascinating       │  │
│  │  concept that I've written about before...   │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
└─────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────┐
│  Type your message here...                    [Send]│
└─────────────────────────────────────────────────────┘
```

## Example Conversations

### Example 1: Writing a Blog Post

**You:** Write a blog post about AI alignment:

**Model:** Today I want to talk about something that's been on my mind lately - AI alignment. This is one of those topics that sounds technical but is actually deeply personal and important for all of us to think about...

### Example 2: Asking Questions

**You:** What do you think about mutual information?

**Model:** Mutual information is such an elegant concept! It captures how much knowing one variable tells you about another. In my work, I've found it particularly useful when thinking about...

### Example 3: Technical Discussion

**You:** Explain the relationship between revealed preferences and decision theory

**Model:** That's a great question! Revealed preferences give us a window into actual decision-making behavior. When we observe someone's choices, we can infer their underlying preferences...

## Common Use Cases

### 1. Content Generation

Generate blog posts in your writing style:

```
Prompt: "Write a blog post about [topic]:"
```

The model will produce content that:
- Uses your vocabulary and phrasing
- Follows your typical structure
- Maintains your conversational tone

### 2. Q&A Assistant

Ask questions about topics you've written about:

```
Prompt: "What are your thoughts on [concept]?"
Prompt: "How do you explain [idea]?"
```

### 3. Writing Practice

Get examples of how you might explain complex topics:

```
Prompt: "Explain [technical concept] in simple terms:"
```

### 4. Brainstorming

Generate ideas in your style:

```
Prompt: "What are some interesting angles on [topic]?"
```

## Settings Guide

### When to Adjust Temperature

**Temperature 0.0 - 0.3** (Focused)
- Use for: Factual content, technical explanations
- Produces: More predictable, consistent output
- Example: "Summarize the key points about..."

**Temperature 0.7** (Balanced) ⭐ Recommended
- Use for: General blog posts, Q&A
- Produces: Good mix of coherence and creativity
- Example: "Write a blog post about..."

**Temperature 0.9 - 1.0** (Creative)
- Use for: Brainstorming, creative writing
- Produces: More diverse, unexpected responses
- Example: "What's an unusual perspective on..."

### When to Adjust Max Tokens

**100-200 tokens** (Short)
- Use for: Quick answers, summaries
- ~1-2 paragraphs

**500 tokens** (Medium) ⭐ Recommended
- Use for: Standard blog post sections
- ~3-4 paragraphs

**1000-2000 tokens** (Long)
- Use for: Full blog posts, detailed explanations
- ~5-10+ paragraphs

## Tips for Best Prompts

### ✅ Good Prompts

```
"Write a blog post about AI safety:"
"What are your thoughts on revealed preferences?"
"Explain mutual information in your own words:"
"How do you think about decision-making under uncertainty?"
```

### ❌ Prompts to Avoid

```
"Hello" (too vague)
"Tell me everything" (too broad)
"What is 2+2?" (not in your domain)
"[No context]" (needs more direction)
```

## Keyboard Shortcuts

- **Enter**: Send message
- **Shift + Enter**: New line in message
- **Ctrl/Cmd + R**: Refresh page

## Troubleshooting

### Model responds slowly
- First response takes longest (model loading)
- Subsequent responses are faster
- Long prompts take more time
- Consider reducing max_tokens

### Responses seem off-topic
- Lower the temperature (try 0.5)
- Make prompts more specific
- Check if topic is in training data

### Getting generic responses
- Model might not have been trained on this topic
- Try prompts closer to your blog content
- Check that checkpoint ID is correct

## Advanced Features

### Multi-turn Conversations

The interface supports ongoing conversations. Each message you send is independent, but you can reference previous context in your prompts:

```
First: "Write about AI safety:"
Then: "Now expand on the risks you mentioned:"
Then: "Give a concrete example of that:"
```

### Experimenting with Style

Try different prompt formats to see what works best:

```
"Write a blog post titled '[Title]':"
"Here's a question: [question]. What would you say?"
"[Topic] - discuss this in your voice:"
```

## Cost Estimates

Based on typical usage:

| Activity | Tokens | Cost |
|----------|--------|------|
| Short Q&A | ~200 | < $0.001 |
| Medium blog post | ~500 | ~$0.005 |
| Long article | ~1500 | ~$0.015 |

**Daily usage (100 interactions)**: ~$0.50 - $1.50
**Monthly (3000 interactions)**: ~$15 - $45

Much more affordable than training!

## Share Your Results

The chat interface makes it easy to:

1. Generate content quickly
2. Iterate on ideas
3. Export conversations (copy/paste from browser)
4. Share with colleagues

Simply copy the generated text from the chat and use it wherever you need!

---

## Need Help?

- Check [CHAT_INTERFACE_README.md](CHAT_INTERFACE_README.md) for setup
- See [README.md](README.md) for training details
- Visit [Tinker Docs](https://tinker-docs.thinkingmachines.ai/) for API reference

Happy chatting! 🎉

