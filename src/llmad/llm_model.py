from langchain_community.llms import Ollama

llm = Ollama(model='llama3:70b')
llm.base_url = 'http://172.28.105.30/backend'
