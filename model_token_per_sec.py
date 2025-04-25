import requests
import time

prompt = "Write a 100-word summary of the Pokémon franchise."

payload = {"model": "mistral", "prompt": prompt, "stream": False}

start_time = time.time()
response = requests.post("http://localhost:11434/api/generate", json=payload)
end_time = time.time()

elapsed = end_time - start_time
data = response.json()

# Estimate output token count as word count or fallback
output = data.get("response", "")
output_tokens = len(output.split())

# Compute real tokens/sec
tps = output_tokens / elapsed if elapsed > 0 else 0

print("\n--- Benchmark ---")
print(f"Output tokens (approx): {output_tokens}")
print(f"Time taken: {elapsed:.2f} sec")
print(f"Tokens/sec: {tps:.2f}")
