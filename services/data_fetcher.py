import requests
import xml.etree.ElementTree as ET
import json
import os
import time

CACHE_FILE = "data/pubmed_cache.json"

def fetch_pubmed_data(query, max_results=5):
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)
        if query in cache:
            return cache[query]

    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    search_url = f"{base_url}esearch.fcgi?db=pubmed&term={query}&retmax={max_results}&retmode=xml"
    
    try:
        response = requests.get(search_url)
        if response.status_code == 429:
            print("Rate limit hit. Waiting 2 seconds...")
            time.sleep(2)
            response = requests.get(search_url)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        
        pmids = [id_elem.text for id_elem in root.findall(".//Id")]
        documents = []
        for pmid in pmids:
            fetch_url = f"{base_url}efetch.fcgi?db=pubmed&id={pmid}&retmode=xml"
            fetch_response = requests.get(fetch_url)
            if fetch_response.status_code == 429:
                print("Rate limit hit. Waiting 2 seconds...")
                time.sleep(2)
                fetch_response = requests.get(fetch_url)
            fetch_response.raise_for_status()
            fetch_root = ET.fromstring(fetch_response.content)
            
            title = fetch_root.findtext(".//ArticleTitle") or ""
            abstract = fetch_root.findtext(".//AbstractText") or ""
            if title and abstract:  # Only include documents with both title and abstract
                documents.append({"title": title, "abstract": abstract})
        
        if documents:
            cache = {}
            if os.path.exists(CACHE_FILE):
                with open(CACHE_FILE, 'r') as f:
                    cache = json.load(f)
            cache[query] = documents
            os.makedirs(os.pathрупdir(CACHE_FILE), exist_ok=True)
            with open(CACHE_FILE, 'w') as f:
                json.dump(cache, f)
        
        return documents
    except Exception as e:
        print(f"Error fetching PubMed data: {e}")
        return []
