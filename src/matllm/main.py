import httpx
from ollama import Client

host = 'http://172.28.105.30/backend'
model = 'llama3:70b'

client = Client(host=host)
# ollama client doesn't handle the /backend properly
client._client = httpx.Client(base_url=host, timeout=500)


response = client.generate(model=model, prompt='Why is the sky blue')
print(response.get('response'))
