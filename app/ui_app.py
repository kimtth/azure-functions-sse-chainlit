import chainlit as cl
import aiohttp
  
# Azure Function URL  
AZURE_FUNCTION_URL = "http://localhost:7071/api/stream-openai"  
  
async def fetch_data(skill, message):  
    params = {  
        'skill': skill,  
        'message': message  
    } 
    # The "ssl=False" is required for http protocol to work in Azure Functions
    async with aiohttp.ClientSession() as session:
        async with session.get(AZURE_FUNCTION_URL, params=params, ssl=False) as response:
            async for line in response.content:
                if line:  
                    decoded_line = line.decode('utf-8')  
                    yield decoded_line

@cl.on_chat_start
def start_chat():
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful assistant."}],
    )

@cl.on_message  
async def on_message(message: cl.Message):  
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")
    await msg.send()

    skill = "faq"
    message_content = message.content
    async for token in fetch_data(skill, message_content):
        await msg.stream_token(token)

    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()
  
if __name__ == "__main__":  
    cl.run()
