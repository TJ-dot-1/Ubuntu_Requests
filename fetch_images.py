#!/usr/bin/env python3
"""
Image Fetcher - A Python script to download images from URLs
and organize them in a local directory.
"""

import os
import requests
from urllib.parse import urlparse, unquote
from pathlib import Path
import mimetypes

def create_directory(directory_name):
    """Create directory if it doesn't exist"""
    try:
        os.makedirs(directory_name, exist_ok=True)
        print(f"Directory '{directory_name}' is ready")
        return True
    except OSError as e:
        print(f"Error creating directory: {e}")
        return False

def extract_filename_from_url(url):
    """
    Extract filename from URL or generate one if not available
    Returns appropriate filename with extension
    """
    # Parse the URL
    parsed_url = urlparse(url)
    
    # Get the path and unquote it (handle URL encoding)
    path = unquote(parsed_url.path)
    
    # Extract filename from path
    filename = os.path.basename(path)
    
    # If no filename in URL, generate one
    if not filename or '.' not in filename:
        # Try to get content type from URL to determine extension
        content_type, _ = mimetypes.guess_type(url)
        if content_type and content_type.startswith('image/'):
            extension = content_type.split('/')[1]
            filename = f"downloaded_image.{extension}"
        else:
            filename = "downloaded_image.jpg"  # default extension
    
    return filename

def download_image(url, save_directory):
    """
    Download image from URL and save to specified directory
    """
    try:
        # Send GET request with headers to mimic browser behavior
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print(f"Connecting to: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        
        # Check for HTTP errors
        response.raise_for_status()
        
        # Check if content is actually an image
        content_type = response.headers.get('content-type', '')
        if not content_type.startswith('image/'):
            print("Warning: The URL doesn't seem to point to an image file")
            # We'll still try to save it but with a warning
        
        # Extract filename
        filename = extract_filename_from_url(url)
        filepath = os.path.join(save_directory, filename)
        
        # Handle duplicate filenames
        counter = 1
        base_name, extension = os.path.splitext(filename)
        while os.path.exists(filepath):
            filename = f"{base_name}_{counter}{extension}"
            filepath = os.path.join(save_directory, filename)
            counter += 1
        
        # Save the image in binary mode
        with open(filepath, 'wb') as file:
            file.write(response.content)
        
        print(f"Successfully downloaded: {filename}")
        print(f"Saved to: {filepath}")
        print(f"File size: {len(response.content)} bytes")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
        return False
    except IOError as e:
        print(f"Error saving file: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def main():
    """Main function to run the image downloader"""
    print("=" * 50)
    print("Image Fetcher - Download images from URLs")
    print("=" * 50)
    
    # Create directory for images
    directory_name = "Fetched_Images"
    if not create_directory(directory_name):
        return
    
    # Prompt user for URL
    while True:
        try:
            url = input("\nPlease enter the image URL (or 'quit' to exit): ").strip()
            
            if url.lower() in ['quit', 'exit', 'q']:
                print("Thank you for using Image Fetcher!")
                break
            
            if not url:
                print("Please enter a valid URL.")
                continue
            
            # Validate URL format
            if not url.startswith(('http://', 'https://')):
                print("Please enter a valid URL starting with http:// or https://")
                continue
            
            # Download the image
            success = download_image(url, directory_name)
            
            if success:
                print("Download completed successfully!")
            else:
                print("Download failed. Please check the URL and try again.")
                
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            continue

if __name__ == "__main__":
    main()