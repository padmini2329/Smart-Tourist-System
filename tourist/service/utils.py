import hashlib
import uuid

def generate_identity_id(name, email):

    raw = str(name) + str(email) + str(uuid.uuid4())

    return hashlib.sha256(raw.encode()).hexdigest()