import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import json
from typing import List, Dict
import time


class DocumentVectorStore:
    def __init__(self, persist_directory="./chroma_db", collection_name="docs_collection"):

        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        # Initialize ChromaDB with persistence
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Load embedding model
        print("Loading embedding model...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        print(f"Vector store initialized. Current document count: {self.collection.count()}")
        
    def scrape_documentation(self, url: str, max_pages: int = 50) -> List[Dict]:
        """
        Scrape documentation from a URL
        
        Args:
            url: Starting URL to scrape
            max_pages: Maximum number of pages to scrape
            
        Returns:
            List of documents with content and metadata
        """
        visited = set()
        to_visit = [url]
        documents = []
        base_domain = urlparse(url).netloc
        
        print(f"Starting to scrape {url}...")
        
        while to_visit and len(documents) < max_pages:
            current_url = to_visit.pop(0)
            
            if current_url in visited:
                continue
                
            visited.add(current_url)
            
            try:
                response = requests.get(current_url, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style", "nav", "footer"]):
                    script.decompose()
                
                # Extract text content
                text = soup.get_text(separator=' ', strip=True)
                
                # Get title
                title = soup.find('title')
                title_text = title.get_text() if title else current_url
                
                if len(text) > 100:  # Only save if substantial content
                    documents.append({
                        'content': text,
                        'url': current_url,
                        'title': title_text
                    })
                    print(f"Scraped: {title_text} ({len(documents)}/{max_pages})")
                
                # Find more links to scrape
                for link in soup.find_all('a', href=True):
                    absolute_url = urljoin(current_url, link['href'])
                    parsed = urlparse(absolute_url)
                    
                    # Only follow links within same domain
                    if parsed.netloc == base_domain and absolute_url not in visited:
                        to_visit.append(absolute_url)
                
                time.sleep(0.5)  # Be respectful to servers
                
            except Exception as e:
                print(f"Error scraping {current_url}: {str(e)}")
                continue
        
        return documents
    
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """
        Split text into overlapping chunks
        
        Args:
            text: Text to chunk
            chunk_size: Size of each chunk in characters
            overlap: Overlap between chunks
            
        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - overlap
            
        return chunks
    
    def add_documents(self, documents: List[Dict], batch_size: int = 100):
        """
        Add documents to vector store with embeddings
        
        Args:
            documents: List of documents to add
            batch_size: Number of documents to process at once
        """
        print(f"\nAdding {len(documents)} documents to vector store...")
        
        all_chunks = []
        all_metadatas = []
        all_ids = []
        chunk_counter = 0
        
        for doc in documents:
            # Chunk the document
            chunks = self.chunk_text(doc['content'])
            
            for chunk in chunks:
                all_chunks.append(chunk)
                all_metadatas.append({
                    'url': doc['url'],
                    'title': doc['title']
                })
                all_ids.append(f"doc_{chunk_counter}")
                chunk_counter += 1
        
        # Process in batches
        for i in range(0, len(all_chunks), batch_size):
            batch_chunks = all_chunks[i:i+batch_size]
            batch_metadata = all_metadatas[i:i+batch_size]
            batch_ids = all_ids[i:i+batch_size]
            
            try :
                # Generate embeddings
                embeddings = self.embedding_model.encode(batch_chunks).tolist()
                
                # Add to collection
                self.collection.add(
                    embeddings=embeddings,
                    documents=batch_chunks,
                    metadatas=batch_metadata,
                    ids=batch_ids
                )
                
                print(f"Added batch {i//batch_size + 1}/{(len(all_chunks)-1)//batch_size + 1}")
                
                time.sleep(1)
                
            except Exception as e:
                print(f"Error processing batch: {str(e)}")
                print("Continuing with next batch...")
                continue
        
        print(f"✓ Successfully added {len(all_chunks)} chunks to vector store")
        print(f"✓ Total documents in collection: {self.collection.count()}")
        
    def query(self, query_text: str, n_results: int = 5) -> Dict:
        """
        Query the vector store
        
        Args:
            query_text: Query string
            n_results: Number of results to return
            
        Returns:
            Dictionary with results
        """
        query_embedding = self.embedding_model.encode([query_text]).tolist()
        
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        
        return results
    
    def delete_collection(self):
        """Delete the entire collection"""
        self.client.delete_collection(name=self.collection_name)
        print(f"Collection '{self.collection_name}' deleted")
        
        
    def get_stats(self):
        """Get collection statistics"""
        count = self.collection.count()
        print(f"\nVector Store Statistics:")
        print(f"Total chunks: {count}")
        print(f"Collection name: {self.collection_name}")
        print(f"Persist directory: {self.persist_directory}")
        return count