import re


def validate_ip(ip: str) -> str:
    result = re.match(r"^((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])(\.(?!$)|$)){4}$", ip)
    return "Invalid IP-address provided" if result is None else None
