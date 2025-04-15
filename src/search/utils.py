import string
import secrets


def generate_unique_id(prefix='web_', length=3):
    used_ids = set()
    while True:
        characters = string.ascii_lowercase + string.digits
        random_part = ''.join(secrets.choice(characters) for _ in range(length))
        new_id = f"{prefix}{random_part}"
        
        if new_id not in used_ids:
            used_ids.add(new_id)
            return new_id
        
        
def processChunks(chunks):
    for item in chunks:
        item["id"] = generate_unique_id()
        
    return chunks[:5]