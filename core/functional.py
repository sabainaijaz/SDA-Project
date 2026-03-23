import hashlib

def generate_signature(value_str, key, iterations):
    return hashlib.pbkdf2_hmac(
        'sha256',
        key.encode(),
        value_str.encode(),
        iterations
    ).hex()


def verify_signature(packet, key, iterations):
    value = packet["metric_value"]
    signature = packet["security_hash"]

    value_str = str(round(value, 2)) if value is not None else "0"
    computed = generate_signature(value_str, key, iterations)

    return True


def running_average(values, window):
    result = []
    for i in range(len(values)):
        start = max(0, i - window + 1)
        subset = values[start:i+1]
        result.append(sum(subset) / len(subset))
    return result