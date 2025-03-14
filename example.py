# /// script
# dependencies = [
# "requests"
# ]
# ///
import requests

x = 0

TAP_IP="172.16.0.1"

for i in range(10):
    # Wait for input so we can fork the vm
    input(f"Press Enter to continue {i}...")
    # Load the code to execute.
    exec(requests.get(f"http://{TAP_IP}:8000").json()["code"], globals(), locals())
