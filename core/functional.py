import hashlib
from typing import List, Dict, Any
from crypto import generate_signature
#all pure functions
#take sinput retuns output
#is data trsted , verifying
def verify_signature(value: float, signature: str, secret_key: str, iterations: int = 100000) -> bool:
    value_str = str(round(value, 2)) if value is not None else "0"
    #rounding val to 2 decimal places
    computed = generate_signature(value_str, secret_key, iterations)
    return computed.hex() == signature #cmp hash values


#sliding window
def running_average(values: List[float], window_size: int) -> List[float]:
    def compute_window(i):#where doe swindow start 
        start = max(0, i - window_size + 1)
        window = values[start:i+1]
        return sum(window) / len(window) if window else None #avg

    return list(map(compute_window, range(len(values)))) #apply to every pos


# checks if valid and filters invalid and returns list
def filter_verified(packets: List[Dict[str, Any]], secret_key: str, iterations: int):
    return list(
        filter(
            lambda p: verify_signature(
                p["metric_value"],
                p["security_hash"],
                secret_key,
                iterations
            ),
            packets
        )
    )