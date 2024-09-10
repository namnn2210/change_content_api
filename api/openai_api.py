from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class OpenAIAPI:
    
    def __init__(self) -> None:
        self.client = OpenAI(api_key=os.getenv('OPEN_AI_API_KEY'))
        self.model = os.getenv('OPEN_API_MODEL')
        self.temperature = 1.0
        self.frequency_penalty = 0
        self.presence_penalty = 0
        # self.option = 'Use English only'
        
    def rewrite(self, input_string, option):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": option},
                {"role": "user", "content": input_string}
            ],
            temperature=self.temperature,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
            n=1
        )
        return completion.choices[0].message.content
