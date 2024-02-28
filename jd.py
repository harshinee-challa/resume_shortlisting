from openai import OpenAI

class ChatBotModel:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.messages = [{"role": "system", "content": "You are a kind helpful assistant and will act as a human resource managerwho is recruiting potential candidates for the company.You will assist in creating a good job description."}]

    def prompt(self, jd):
        message=f" This is a small description of the job role.<Job Description:{jd}>. I want you to enhance this and add more details to it like the technologies that are usually required for this.Add highly technical language and improve the description as efficiently as possible.You are free to make it 200 words."
        self.messages.append({"role": "user", "content": message})

        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages, #type:ignore
        )
        ans = completion.choices[0].message.content
        print(ans)
        return ans
    
    