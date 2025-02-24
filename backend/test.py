import os

file_path = "uploaded_images/test_images/amazon.jpg"
file_size = os.path.getsize(file_path)
print(f"File size: {file_size} bytes")