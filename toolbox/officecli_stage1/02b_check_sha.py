"""Check SHA256 against official release."""
import urllib.request
url = "https://github.com/iOfficeAI/OfficeCLI/releases/download/v1.0.135/SHA256SUMS"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
data = urllib.request.urlopen(req, timeout=30).read().decode('utf-8')
print("=== Official SHA256SUMS ===")
print(data)
print()
print("=== Local hash ===")
print("1C3AB6421A6301086483046D1AA42B1C01A4AC005D44DE1F9755B50AE3B93A9E")
