from pathlib import Path
import uuid
import hashlib

ALLOWED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif')
MAX_FILE_SIZE = 5 * 1024 * 1024

def is_allowed_file(filename: Path) -> bool:
    return filename.suffix.lower() in ALLOWED_EXTENSIONS

def get_unique_name(content, filename: Path):
    return f'{calculate_sha256(content)}{filename.suffix.lower()}'


def calculate_sha256(content):
    return hashlib.sha256(content).hexdigest()

def get_images_in_dir(directory):
    dir = Path(directory)
    files = [file for file in dir.iterdir() if file.is_file() and file.suffix.lower() in ALLOWED_EXTENSIONS]
    return files

if __name__ == "__main__":
    print(is_allowed_file(Path('test.jpg')))
    print(is_allowed_file(Path('test.gg')))
    print(get_unique_name(Path('test.png')))