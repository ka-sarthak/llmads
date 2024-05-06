import httpx
from ollama import Client

host = 'http://172.28.105.30/backend'
client = Client(host=host)
# ollama client doesn't handle the /backend properly
client._client = httpx.Client(base_url=host, timeout=500)


def generate(model: str = 'llama3:70b', prompt: str = ''):
    response = client.generate(model=model, prompt=prompt)
    return response.get('response')
