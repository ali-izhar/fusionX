import logging
import base64
import requests
import time
import os


def is_base64(data):
    """Check if the given data is base64 encoded."""
    try:
        if 'data:image' in data and ';base64,' in data:
            return True
    except Exception as e:
        logging.error(f"An error occurred while checking base64 encoding: {e}")
    return False


def convert_to_base64(url):
    """Convert an image URL to base64 encoding."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Determine the MIME type from the Content-Type header
            content_type = response.headers.get('Content-Type')
            # Fallback to a default if the MIME type is not available
            if not content_type:
                content_type = 'image/jpeg'
            
            # Create the data URL with the correct MIME type
            base64_encoded_data = base64.b64encode(response.content).decode('utf-8')
            return f"data:{content_type};base64,{base64_encoded_data}"
    except Exception as e:
        logging.error(f"An error occurred while converting image URL to base64: {e}")
    return None


def process_image_data(image_data):
    """Processes the given image data, converting URLs to base64 if necessary,
    and returns the image data and its extension.
    """
    if not is_base64(image_data):
        logging.info("Image data is not base64. Attempting to convert from URL.")
        image_data = convert_to_base64(image_data)
        if image_data is None:
            raise ValueError("Failed to convert image data to base64.")
    image_bytes = base64.b64decode(image_data.split(',')[1])
    extension = image_data.split(',')[0].split('/')[1].split(';')[0]
    return image_bytes, extension


def write_temp_file(temp_file, image_data):
    """Writes image data to a temporary file."""
    try:
        temp_file.write(image_data)
        temp_file.flush() 
    except Exception as e:
        logging.error(f"An error occurred while writing to temporary file: {e}")
        raise e


def cleanup_temp_files(file_paths):
    """Cleans up temporary files after ensuring they are not in use."""
    max_retries = 5
    retry_delay = 1  # seconds
    for file_path in file_paths:
        for attempt in range(max_retries):
            try:
                os.remove(file_path)
                break  # Successfully deleted file, break out of retry loop
            except PermissionError as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)  # Wait a bit before retrying
                else:
                    logging.error(f"An error occurred while cleaning up temporary files: {e}")


def generate_unique_file_name(base_path, original_name, img_format):
    """Generates a unique file name by appending a number if the file already exists."""
    counter = 1
    name, _ = os.path.splitext(original_name)
    new_name = original_name  # Default to the original name if not already taken
    while os.path.exists(os.path.join(base_path, new_name + img_format)):
        new_name = f"{name}_{counter}"
        counter += 1
    return new_name + img_format
