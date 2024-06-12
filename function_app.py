import azure.functions as func  
import openai  
import asyncio  
import os
import yaml
from azurefunctions.extensions.http.fastapi import Request, StreamingResponse  
  
# Azure Function App  
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)  
  
# Environment variables for Azure Open AI  
endpoint = os.environ["AZURE_OPEN_AI_ENDPOINT"]  
api_key = os.environ["AZURE_OPEN_AI_API_KEY"]  
deployment = os.environ["AZURE_OPEN_AI_DEPLOYMENT_MODEL"]  
temperature = 0.7  
  
# Initialize OpenAI client  
client = openai.AsyncAzureOpenAI(  
    azure_endpoint=endpoint,  
    api_key=api_key,  
    api_version="2024-02-01"  
) 

promtp_file_path = os.path.join(os.path.dirname(__file__), "prompts", "prompts.yaml")

# Load prompts from yaml file
def load_prompts():
    qna_prompts = ''
    with open(promtp_file_path, encoding='utf-8') as file:
        prompt = yaml.safe_load(file)
        qna_prompts = prompt.get("PROMPTS").get("General_Answers")
    return qna_prompts
  
# Get data from Azure Open AI  
async def stream_processor(response):  
    async for chunk in response:  
        if len(chunk.choices) > 0:  
            delta = chunk.choices[0].delta  
            if delta.content:  # Get remaining generated response if applicable  
                await asyncio.sleep(0.1)  
                yield f"{delta.content}"  

# HTTP streaming Azure Function  
@app.route(route="stream-openai", methods=[func.HttpMethod.GET])  
async def stream_openai_text(req: Request) -> StreamingResponse:  
    skill = req.path_params.get('skill')  
    message = req.path_params.get('message')  
  
    if not skill or not message:  
        try:  
            req_body = await req.json()  
        except ValueError:  
            pass  
        else:  
            skill = req_body.get('skill')  
            message = req_body.get('message')  
  
    if not skill or not message:  
        return func.HttpResponse(  
            "This HTTP triggered function executed successfully.",  
            status_code=200  
        )  
  
    qna_prompts = load_prompts()
    prompt = str(qna_prompts).replace("question", message)
    # prompt = message
  
    azure_open_ai_response = await client.chat.completions.create(  
        model=deployment,  
        temperature=temperature,  
        max_tokens=1000,  
        messages=[{"role": "user", "content": prompt}],  
        stream=True  
    ) 

    return StreamingResponse(stream_processor(azure_open_ai_response), media_type="text/event-stream")  
