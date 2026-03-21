import hashlib


def generate_signature(raw_value_str: str, key: str, iterations: int) -> str:
    """
    Generates a PBKDF2 HMAC SHA-256 signature for the given value.
    Treats the secret key as the password and the raw value as the salt.
    """
    password_bytes = key.encode('utf-8')
    salt_bytes = raw_value_str.encode('utf-8')
    
    # Generate the hash
    hash_bytes = hashlib.pbkdf2_hmac(
        hash_name='sha256', 
        password=password_bytes, 
        salt=salt_bytes, 
        iterations=iterations
    )
    return hash_bytes.hex()

def verify_signature(packet: dict, config: dict) -> bool:
    try:
        raw_value = round(packet["metric_value"], 2)
        raw_value_str = f"{raw_value:.2f}"

        stateless = config["processing"]["stateless_tasks"]
        key = stateless["secret_key"]
        iterations = stateless["iterations"]

        expected_signature = generate_signature(raw_value_str, key, iterations)

        return expected_signature == packet['signature']
    
    except Exception:
        return False
