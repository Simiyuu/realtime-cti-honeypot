import requests
import time

_cache = {}
FAIL_RETRY_SECONDS = 300

def get_ip_geolocation(ip_address):
    cached = _cache.get(ip_address)
    if cached:
        result, expires = cached
        if expires is None or time.time() < expires:
            return result

    result = _lookup_ip(ip_address)
    failed = result["country"] == "Lookup Failed" or (
        result["country"] == "Unknown" and not result["is_private"]
    )
    expires = time.time() + FAIL_RETRY_SECONDS if failed else None
    _cache[ip_address] = (result, expires)
    return result

def _lookup_ip(ip_address):
    
    private_ranges = [
        "127.", "10.", "172.16.", "172.17.", 
        "172.18.", "192.168.", "::1"
    ]
    
    for private in private_ranges:
        if ip_address.startswith(private):
            return {
                "ip": ip_address,
                "country": "Local Network",
                "country_code": "LN",
                "region": "Internal",
                "city": "Local",
                "isp": "Internal Network",
                "latitude": 0.0,
                "longitude": 0.0,
                "is_private": True
            }
    
    try:
        response = requests.get(
            f"http://ip-api.com/json/{ip_address}",
            timeout=5
        )
        data = response.json()
        
        if data.get("status") == "success":
            return {
                "ip": ip_address,
                "country": data.get("country", "Unknown"),
                "country_code": data.get("countryCode", "XX"),
                "region": data.get("regionName", "Unknown"),
                "city": data.get("city", "Unknown"),
                "isp": data.get("isp", "Unknown"),
                "latitude": data.get("lat", 0.0),
                "longitude": data.get("lon", 0.0),
                "is_private": False
            }
        else:
            return {
                "ip": ip_address,
                "country": "Unknown",
                "country_code": "XX",
                "region": "Unknown",
                "city": "Unknown",
                "isp": "Unknown",
                "latitude": 0.0,
                "longitude": 0.0,
                "is_private": False
            }
            
    except Exception as e:
        return {
            "ip": ip_address,
            "country": "Lookup Failed",
            "country_code": "XX",
            "region": "Unknown",
            "city": "Unknown",
            "isp": "Unknown",
            "latitude": 0.0,
            "longitude": 0.0,
            "is_private": False
        }

if __name__ == "__main__":
    test_ip = "8.8.8.8"
    result = _lookup_ip(test_ip)
    print(f"Geolocation for {test_ip}:")
    for key, value in result.items():
        print(f"  {key}: {value}")
        