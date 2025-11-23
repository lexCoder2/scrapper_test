"""
Product Image Downloader
Downloads all product images from MongoDB and saves them locally
Updates database with local image paths
"""

import requests
import os
import sys
import time
from datetime import datetime
from urllib.parse import urlparse
from pymongo import MongoClient
from pathlib import Path

class ProductImageDownloader:
    def __init__(self, mongodb_uri, images_dir='product_images', batch_size=100):
        self.mongodb_uri = mongodb_uri
        self.images_dir = images_dir
        self.batch_size = batch_size
        self.db = None
        self.collection = None
        
        # Statistics
        self.stats = {
            'total': 0,
            'already_downloaded': 0,
            'downloaded': 0,
            'failed': 0,
            'no_url': 0,
            'updated_db': 0
        }
        
        # Create images directory
        os.makedirs(self.images_dir, exist_ok=True)
        
        # HTTP headers
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Language': 'es-MX,es;q=0.9'
        }
    
    def connect_db(self):
        """Connect to MongoDB"""
        try:
            client = MongoClient(self.mongodb_uri)
            self.db = client['products']
            self.collection = self.db['grocery_products']
            print("[OK] Connected to MongoDB")
            
            # Get total count
            self.stats['total'] = self.collection.count_documents({})
            print(f"[INFO] Total products in database: {self.stats['total']}")
            
            return True
        except Exception as e:
            print(f"[ERROR] MongoDB connection failed: {e}")
            return False
    
    def download_image(self, image_url, sku, store):
        """Download a single product image"""
        if not image_url:
            return None, 'no_url'
        
        try:
            # Handle protocol-relative URLs
            if image_url.startswith('//'):
                image_url = 'https:' + image_url
            
            # Validate URL
            if not image_url.startswith(('http://', 'https://')):
                return None, 'invalid_url'
            
            # Get file extension from URL
            parsed = urlparse(image_url)
            ext = os.path.splitext(parsed.path)[1]
            if not ext or ext not in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
                ext = '.jpg'
            
            # Create filename: store_sku.ext
            safe_store = store.replace(' ', '_').lower()
            filename = f"{safe_store}_{sku}{ext}"
            filepath = os.path.join(self.images_dir, filename)
            
            # Check if already exists
            if os.path.exists(filepath):
                file_size = os.path.getsize(filepath)
                if file_size > 0:  # Valid file exists
                    return filepath, 'exists'
            
            # Download image with shorter timeout
            response = requests.get(
                image_url, 
                headers=self.headers, 
                timeout=5,
                stream=True,
                allow_redirects=True
            )
            
            if response.status_code == 200:
                # Save image
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                # Verify file was saved and has content
                if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                    return filepath, 'downloaded'
                else:
                    return None, 'empty_file'
            else:
                return None, f'http_{response.status_code}'
        
        except requests.exceptions.Timeout:
            return None, 'timeout'
        except requests.exceptions.ConnectionError:
            return None, 'connection_error'
        except requests.exceptions.SSLError:
            return None, 'ssl_error'
        except KeyboardInterrupt:
            raise
        except Exception as e:
            return None, f'error'
    
    def process_products(self, skip_existing=True):
        """Process all products and download images"""
        print("\n" + "="*70)
        print("STARTING IMAGE DOWNLOAD")
        print("="*70)
        print(f"Images directory: {os.path.abspath(self.images_dir)}")
        print(f"Batch size: {self.batch_size}")
        print(f"Skip existing: {skip_existing}")
        print("="*70 + "\n")
        
        start_time = time.time()
        processed = 0
        
        # Query filter - find products where local_image is a URL (starts with http)
        query = {}
        if skip_existing:
            query = {
                '$or': [
                    {'local_image': {'$exists': False}},
                    {'local_image': ''},
                    {'local_image': None},
                    {'local_image': {'$regex': '^http'}}  # Matches URLs that need to be downloaded
                ]
            }
            products_to_process = self.collection.count_documents(query)
            print(f"[INFO] Products to process: {products_to_process}")
        
        # Process in batches
        cursor = self.collection.find(query).batch_size(self.batch_size)
        
        try:
            for product in cursor:
                processed += 1
                
                sku = product.get('sku', 'unknown')
                store = product.get('store', 'unknown')
                image_url = product.get('image_url', '')
                
                # Skip if no image URL
                if not image_url:
                    self.stats['no_url'] += 1
                    if processed % 100 == 0:
                        self._print_progress(processed, start_time)
                    continue
                
                # Download image
                local_path, status = self.download_image(image_url, sku, store)
                
                # Update statistics
                if status == 'exists':
                    self.stats['already_downloaded'] += 1
                elif status == 'downloaded':
                    self.stats['downloaded'] += 1
                elif status == 'no_url':
                    self.stats['no_url'] += 1
                else:
                    self.stats['failed'] += 1
                
                # Update database with local path (even if download failed, to track attempts)
                if local_path:
                    try:
                        self.collection.update_one(
                            {'_id': product['_id']},
                            {'$set': {
                                'local_image': local_path,
                                'image_downloaded_at': datetime.now().isoformat()
                            }}
                        )
                        self.stats['updated_db'] += 1
                    except Exception as e:
                        pass
                
                # Progress report every 100 products
                if processed % 100 == 0:
                    self._print_progress(processed, start_time)
                
                # Small delay to avoid overwhelming servers
                if status == 'downloaded':
                    time.sleep(0.05)
        
        except KeyboardInterrupt:
            print("\n\n[INTERRUPTED] Download interrupted by user")
            print(f"Processed {processed} products before interruption")
        
        elapsed = time.time() - start_time
        
        # Final report
        print("\n" + "="*70)
        print("DOWNLOAD COMPLETE")
        print("="*70)
        print(f"Total products processed: {processed}")
        print(f"Already had images: {self.stats['already_downloaded']}")
        print(f"Newly downloaded: {self.stats['downloaded']}")
        print(f"Failed downloads: {self.stats['failed']}")
        print(f"No image URL: {self.stats['no_url']}")
        print(f"Database updates: {self.stats['updated_db']}")
        print(f"Time elapsed: {elapsed:.2f} seconds")
        print(f"Average: {processed/elapsed:.2f} products/second")
        print("="*70)
        
        # Show images directory size
        total_size = sum(
            os.path.getsize(os.path.join(self.images_dir, f)) 
            for f in os.listdir(self.images_dir) 
            if os.path.isfile(os.path.join(self.images_dir, f))
        )
        print(f"\nImages directory size: {total_size / (1024*1024):.2f} MB")
        print(f"Total image files: {len(os.listdir(self.images_dir))}")
    
    def _print_progress(self, processed, start_time):
        """Print progress update"""
        elapsed = time.time() - start_time
        rate = processed / elapsed if elapsed > 0 else 0
        
        print(f"\r[PROGRESS] {processed}/{self.stats['total']} | "
              f"Downloaded: {self.stats['downloaded']} | "
              f"Exists: {self.stats['already_downloaded']} | "
              f"Failed: {self.stats['failed']} | "
              f"Rate: {rate:.1f}/s", 
              end='', flush=True)
    
    def verify_images(self):
        """Verify all downloaded images"""
        print("\n" + "="*70)
        print("VERIFYING IMAGES")
        print("="*70)
        
        verified = 0
        corrupted = 0
        missing = 0
        
        cursor = self.collection.find({'local_image': {'$exists': True, '$ne': ''}})
        
        for product in cursor:
            local_image = product.get('local_image', '')
            if not local_image:
                continue
            
            if os.path.exists(local_image):
                size = os.path.getsize(local_image)
                if size > 0:
                    verified += 1
                else:
                    corrupted += 1
                    print(f"\n[WARNING] Corrupted image: {local_image}")
            else:
                missing += 1
                print(f"\n[WARNING] Missing image: {local_image}")
        
        print(f"\nVerified: {verified}")
        print(f"Corrupted: {corrupted}")
        print(f"Missing: {missing}")
        print("="*70)
        
        return verified, corrupted, missing
    
    def retry_failed(self):
        """Retry downloading images that failed"""
        print("\n" + "="*70)
        print("RETRYING FAILED DOWNLOADS")
        print("="*70)
        
        # Find products with image_url but no local_image
        query = {
            'image_url': {'$exists': True, '$ne': ''},
            '$or': [
                {'local_image': {'$exists': False}},
                {'local_image': ''},
                {'local_image': None}
            ]
        }
        
        failed_count = self.collection.count_documents(query)
        print(f"Products to retry: {failed_count}\n")
        
        # Reset stats for retry
        self.stats['downloaded'] = 0
        self.stats['failed'] = 0
        self.stats['already_downloaded'] = 0
        self.stats['total'] = failed_count
        
        # Process again
        self.process_products(skip_existing=False)

def main():
    """Main execution"""
    # Configuration
    mongodb_uri = "mongodb://admin:productdb2025@localhost:27017/products?authSource=admin"
    images_dir = "product_images"
    batch_size = 100
    
    # Parse command line arguments
    skip_existing = True
    verify_only = False
    retry_failed = False
    
    if len(sys.argv) > 1:
        if '--no-skip' in sys.argv:
            skip_existing = False
        if '--verify' in sys.argv:
            verify_only = True
        if '--retry' in sys.argv:
            retry_failed = True
        if '--help' in sys.argv:
            print("Usage: python download_product_images.py [OPTIONS]")
            print("\nOptions:")
            print("  --no-skip    Download all images, even if they exist")
            print("  --verify     Only verify existing images, don't download")
            print("  --retry      Retry failed downloads only")
            print("  --help       Show this help message")
            return
    
    # Create downloader
    downloader = ProductImageDownloader(
        mongodb_uri=mongodb_uri,
        images_dir=images_dir,
        batch_size=batch_size
    )
    
    # Connect to database
    if not downloader.connect_db():
        print("[ERROR] Could not connect to database")
        return
    
    # Execute requested operation
    if verify_only:
        downloader.verify_images()
    elif retry_failed:
        downloader.retry_failed()
    else:
        downloader.process_products(skip_existing=skip_existing)
        
        # Verify after download
        print("\n")
        downloader.verify_images()

if __name__ == "__main__":
    main()
