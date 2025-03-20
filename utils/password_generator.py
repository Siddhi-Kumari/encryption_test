import random
import string

def generate_password(length=12):
    """Generates a random password."""
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))
