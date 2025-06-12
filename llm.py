import os
import json
import time
import sys
import requests # pip install requests
from dotenv import load_dotenv # pip install dotenv
load_dotenv()

class Typewriter:
    """
    Typewriter effect class for displaying text character by character.
    """
    def __init__(self, delay=0.03):
        """
        - delay: eng: delay between characters in seconds
        """
        self.delay = delay
        self.full_text = ""
    
    def type_text(self, text):
        """
        Display text character by character.
        """
        self.full_text += text
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(self.delay)
    
    def get_full_text(self):
        return self.full_text

def get_env_variable(var_name):
    """get env vars, else: None"""
    '''
    LLM_URL_BASE
    LLM_MODEL_NAME
    LLM_API_KEY
    '''
    return os.getenv(var_name)

def send_llm_chat_request(
        prompt,
        model: str|None=None,
        temperature: float=0.9,
        top_p: float=0.95,
        top_k: int=50,
        max_tokens: int=-1,
        stream: bool=False,
        typewriter: Typewriter=Typewriter(0.03)
    ) -> str:
    """
    send a chat request to a large language model API.
    
    params:
    - prompt: necessary string
    - model: if None then use env var LLM_MODEL_NAME
    - temperature: 0.0-1.0, higher means more random
    - top_p: 0.0-1.0, higher means more random
    - top_k: the number of highest probability tokens to keep when sampling
    - max_tokens: the maximum number of tokens to generate in the response
    - stream: whether to stream the response with typewriter effect
    - typer: Typewriter instance for streaming response
    
    returns:
    - str: the response content from the model
    """
    base_url = get_env_variable("LLM_URL_BASE")
    model_name = model if model else get_env_variable("LLM_MODEL_NAME")
    api_key = get_env_variable("LLM_API_KEY")
    
    if not base_url or not model_name or not api_key:
        raise ValueError("env error: LLM_URL_BASE, LLM_MODEL_NAME or LLM_API_KEY")
    
    url = f"{base_url.rstrip('/')}/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "stream": stream
    }
    if max_tokens > 0:
        payload["max_tokens"] = max_tokens
    
    try:
        if stream:
            response = requests.post(url, headers=headers, json=payload, stream=True)
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    # skip row 'keep-alive' and prefix
                    if line.startswith('data: ') and line != 'data: [DONE]':
                        json_str = line[6:]  # remove 'data: ' prefix
                        try:
                            chunk = json.loads(json_str)
                            if "choices" in chunk and len(chunk["choices"]) > 0:
                                content = chunk["choices"][0].get("delta", {}).get("content", "")
                                if content:
                                    typewriter.type_text(content)
                        except json.JSONDecodeError:
                            continue
            print()  # print a newline after the typewriter effect
            return typewriter.get_full_text()
        else:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"] # openai api style
            else:
                return "data structure error"
    
    except requests.exceptions.RequestException as e:
        return f"bad request: {str(e)}\n{response.text if 'response' in locals() else ''}"
    except json.JSONDecodeError:
        return f"bad data struct: {response.text if 'response' in locals() else ''}"
    except Exception as e:
        if 'response' in locals():
            print(response.text)
        return f"error: {str(e)}\n{response.text if 'response' in locals() else ''}"

if __name__ == "__main__":
    prompt = "tell me a joke" # simple test
    # prompt = "tell me a story about a brave knight and a dragon" # longer test, for streaming effect
    response = send_llm_chat_request(
        prompt=prompt,
        temperature=0.9,
        top_p=0.95,
        top_k=50,
        max_tokens=2048,
        stream=True,
        typewriter=Typewriter(0.001)
    )
    if not response.startswith("bad request") and not response.startswith("error"):
        print("\nLLM response (full):")
        print(response)