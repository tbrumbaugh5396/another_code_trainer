import requests
from bs4 import BeautifulSoup
import sqlite3
from deep_translator import GoogleTranslator

def init_db():
    conn = sqlite3.connect("trainer.db")
    conn.execute("""CREATE TABLE IF NOT EXISTS problems 
                 (id INTEGER PRIMARY KEY, title TEXT, description TEXT, 
                  tech_clues TEXT, complexity TEXT, source TEXT)""")
    conn.close()

def translate_chunks(text, chunk_size=3000):
    """
    Splits long text into chunks to avoid API limits.
    """
    translator = GoogleTranslator(source='auto', target='en')
    
    # Split by double newlines to try and keep paragraphs/code blocks together
    paragraphs = text.split('\n\n')
    translated_text = ""
    current_chunk = ""

    for p in paragraphs:
        if len(current_chunk) + len(p) < chunk_size:
            current_chunk += p + "\n\n"
        else:
            # Translate current chunk and reset
            translated_text += translator.translate(current_chunk) + "\n\n"
            current_chunk = p + "\n\n"
            
    # Translate the final remaining chunk
    if current_chunk:
        translated_text += translator.translate(current_chunk)
        
    return translated_text

def scrape_and_store(url):
    raw_url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
    try:
        res = requests.get(raw_url, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print(f"❌ Network Error for {url}: {e}")
        return

    translator = GoogleTranslator(source='auto', target='en')
    paragraphs = res.text.split('\n\n')
    
    translated_parts = []
    print(f"--- Processing: {url.split('/')[-1]} ---")

    for i, p in enumerate(paragraphs):
        if not p.strip(): continue
        try:
            # Fix for the 'NoneType' error: 
            # If translation fails or returns None, we skip or use empty string
            result = translator.translate(p)
            if result:
                translated_parts.append(result)
                print(f"  [Chunk {i+1}] Done")
        except Exception as e:
            print(f"  [Chunk {i+1}] Warning: {e}")

    if not translated_parts:
        print("⚠️ No content was translated. Skipping save.")
        return

    # Join the list into one final string
    final_description = "\n\n".join(translated_parts)
    
    # Simple Title Extraction
    title = url.split('/')[-1] # Fallback title
    if "\n" in final_description:
        first_line = final_description.split('\n')[0].replace('#', '').strip()
        if first_line: title = first_line

    # SAVE TO DATABASE
    try:
        conn = sqlite3.connect("trainer.db")
        cursor = conn.cursor()
        
        # We use INSERT OR REPLACE to ensure we don't get duplicates 
        # but also to update existing entries if the URL matches
        cursor.execute("""
            INSERT OR REPLACE INTO problems (title, description, source) 
            VALUES (?, ?, ?)""", (title, final_description, url))
        
        conn.commit()
        conn.close()
        print(f"✅ SUCCESSFULLY STORED: {title}")
    except Exception as e:
        print(f"❌ Database Error: {e}")


def scrape_and_store_structured(url):
    raw_url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
    res = requests.get(raw_url)
    if res.status_code != 200: return

    # 1. Translate the whole text in chunks first (in-memory)
    translator = GoogleTranslator(source='auto', target='en')
    raw_chunks = res.text.split('\n\n')
    full_text = ""
    for chunk in raw_chunks:
        full_text += (translator.translate(chunk) or "") + "\n\n"

    # 1. Improved Title Extraction
    title_match = re.search(r"Sum of (.*?)\)", full_text)
    title = title_match.group(1) if title_match else url.split('/')[-1]

    # 2. Flexible Section Extraction
    # We look for "Prerequisite knowledge" or "Prerequisites"
    prereq_match = re.search(r"## (?:Prerequisite knowledge|Prerequisites)\n+(.*?)\n+##", full_text, re.S | re.I)
    
    # Extracting Description (everything between Title and Prerequisite)
    desc_match = re.search(r"Title description\n+```(.*?)```", full_text, re.S)
    
    # Complexity is often at the bottom or missing in this repo
    time_match = re.search(r"Time complexity[:：]\s*(O\(.*?\))", full_text, re.I)
    space_match = re.search(r"Space complexity[:：]\s*(O\(.*?\))", full_text, re.I)

    # 3. Clean and Save
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO problems 
        (title, description, prerequisites, complexity_time, complexity_space, source) 
        VALUES (?, ?, ?, ?, ?, ?)""", 
        (
            title,
            desc_match.group(1).strip() if desc_match else "No description parsed",
            prereq_match.group(1).strip().replace('-', '').strip() if prereq_match else "General Logic",
            time_match.group(1) if time_match else "O(N)",
            space_match.group(1) if space_match else "O(N)",
            url
        ))
    conn.commit()
    conn.close()
    print(f"✅ Structural Save Complete: {title}")


def crawl_repo(main_url):
    res = requests.get(main_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    # Find all links ending in .md (common for problem sets)
    links = soup.find_all('a', href=True)
    for link in links:
        href = link['href']
        print(href)
        if href.endswith('.md') and '/problems/' in href:
            full_url = "https://github.com" + href
            scrape_and_store(full_url)

if __name__ == "__main__":
    init_db()
    # Point this to a 'Summary' or 'README' page of a problem repo
    crawl_repo("https://github.com/azl397985856/leetcode/")