#!/usr/bin/env python3
"""
Parse Substack RSS feed and convert blog posts to plaintext.
Strips HTML tags and extracts clean text content.
"""

import xml.etree.ElementTree as ET
from html.parser import HTMLParser
import json
import re


class HTMLTextExtractor(HTMLParser):
    """Extract text content from HTML, ignoring tags."""
    
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.skip_tags = {'script', 'style'}
        self.current_tag = None
        
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        
    def handle_endtag(self, tag):
        self.current_tag = None
        
    def handle_data(self, data):
        if self.current_tag not in self.skip_tags:
            # Clean up whitespace but preserve paragraph breaks
            cleaned = data.strip()
            if cleaned:
                self.text_parts.append(cleaned)
    
    def get_text(self):
        return '\n\n'.join(self.text_parts)


def clean_text(text):
    """Additional text cleaning."""
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Remove special HTML entities that might have been missed
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    text = text.replace('&#8217;', "'")
    text = text.replace('&#8220;', '"')
    text = text.replace('&#8221;', '"')
    text = text.replace('&nbsp;', ' ')
    return text.strip()


def parse_rss_to_plaintext(rss_file):
    """Parse RSS feed and extract blog posts as plaintext."""
    
    # Parse the XML
    tree = ET.parse(rss_file)
    root = tree.getroot()
    
    # Find all items (blog posts)
    posts = []
    
    # RSS namespace handling
    namespaces = {
        'content': 'http://purl.org/rss/1.0/modules/content/',
        'dc': 'http://purl.org/dc/elements/1.1/'
    }
    
    for item in root.findall('.//item'):
        # Extract basic info
        title_elem = item.find('title')
        description_elem = item.find('description')
        content_elem = item.find('content:encoded', namespaces)
        pub_date_elem = item.find('pubDate')
        link_elem = item.find('link')
        
        # Get the full content (prefer content:encoded over description)
        html_content = ''
        if content_elem is not None and content_elem.text:
            html_content = content_elem.text
        elif description_elem is not None and description_elem.text:
            html_content = description_elem.text
            
        # Extract text from HTML
        extractor = HTMLTextExtractor()
        extractor.feed(html_content)
        text_content = extractor.get_text()
        text_content = clean_text(text_content)
        
        # Get title (also clean CDATA)
        title = ''
        if title_elem is not None and title_elem.text:
            title = title_elem.text.strip()
        
        # Get date
        pub_date = ''
        if pub_date_elem is not None and pub_date_elem.text:
            pub_date = pub_date_elem.text.strip()
            
        # Get link
        link = ''
        if link_elem is not None and link_elem.text:
            link = link_elem.text.strip()
        
        post = {
            'title': title,
            'date': pub_date,
            'link': link,
            'content': text_content
        }
        
        posts.append(post)
    
    return posts


def save_as_plaintext(posts, output_file):
    """Save posts as a simple plaintext file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, post in enumerate(posts, 1):
            f.write(f"{'='*80}\n")
            f.write(f"POST {i}: {post['title']}\n")
            f.write(f"Date: {post['date']}\n")
            f.write(f"Link: {post['link']}\n")
            f.write(f"{'='*80}\n\n")
            f.write(post['content'])
            f.write('\n\n\n')


def save_as_json(posts, output_file):
    """Save posts as JSON (useful for finetuning)."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)


def save_for_finetuning(posts, output_file):
    """
    Save in JSONL format suitable for finetuning.
    Each line is a training example with the full blog post.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for post in posts:
            # Format: Each post as a complete text generation example
            training_example = {
                "text": f"Title: {post['title']}\n\n{post['content']}"
            }
            f.write(json.dumps(training_example, ensure_ascii=False) + '\n')


def main():
    rss_file = '/Users/mox/lydia-clone/substack-feed.rss'
    
    print("Parsing RSS feed...")
    posts = parse_rss_to_plaintext(rss_file)
    print(f"Found {len(posts)} blog posts")
    
    # Save in different formats
    print("\nSaving outputs...")
    
    # 1. Plaintext format (human-readable)
    save_as_plaintext(posts, '/Users/mox/lydia-clone/blogposts.txt')
    print("✓ Saved to blogposts.txt (plaintext)")
    
    # 2. JSON format (structured)
    save_as_json(posts, '/Users/mox/lydia-clone/blogposts.json')
    print("✓ Saved to blogposts.json (structured)")
    
    # 3. JSONL format for finetuning
    save_for_finetuning(posts, '/Users/mox/lydia-clone/blogposts_finetuning.jsonl')
    print("✓ Saved to blogposts_finetuning.jsonl (for finetuning)")
    
    # Print summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    print(f"Total posts: {len(posts)}")
    
    total_chars = sum(len(post['content']) for post in posts)
    total_words = sum(len(post['content'].split()) for post in posts)
    
    print(f"Total characters: {total_chars:,}")
    print(f"Total words: {total_words:,}")
    print(f"Average words per post: {total_words // len(posts):,}")
    
    print(f"\n{'='*80}")
    print("RECENT POSTS")
    print(f"{'='*80}")
    for i, post in enumerate(posts[:5], 1):
        print(f"{i}. {post['title']}")
        print(f"   Date: {post['date']}")
        print(f"   Words: {len(post['content'].split()):,}")
        print()


if __name__ == '__main__':
    main()

