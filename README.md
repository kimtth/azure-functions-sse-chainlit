
# Azure Functions with SSE

- This sample application demonstrates how to implement SSE (Server-Sent Events) in Azure Functions.
- The UI code has been created using Chainlit.
- The backend is developed using the Azure Function App Python SDK.
- The SDK and implementation use Azure Function Programming model v2.

## Endpoint: HTTP Trigger

- azure: `https://<APP_NAME>.azurewebsites.net/api/<FUNCTION_NAME>`
- local: `http://localhost:<PORT>/api/<FUNCTION_NAME>`
    -  [GET] http://localhost:7071/api/stream-openai

## Code and test Azure Functions locally

- [Code and test Azure Functions locally](https://learn.microsoft.com/en-us/azure/azure-functions/functions-develop-local)
- [Develop Azure Functions locally using Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local)

- Install the Azure Functions Core Tools & Visual Code : Azure Extension
- Rename `local.settings.template.json` to `local.settings.json` - Fill your values in `local.settings.json` 
- The command must be run in a virtual environment.
    - Functions: `func start` 
    - UI application: `chainlit run ui_app.py -w`
- [Optional] Change venv path > .vscode > settings.json > "azureFunctions.pythonVenv": "venv"

## Publish your local code to a function app in Azure

- cmd: `func azure functionapp publish <FunctionAppName>`

## SSE（Server-Sent Events）

- [Azure Functions: Support for HTTP Streams in Python is now in Preview!](https://techcommunity.microsoft.com/t5/azure-compute-blog/azure-functions-support-for-http-streams-in-python-is-now-in/ba-p/4146697)
    - When deploying, add the following application settings: "PYTHON_ENABLE_INIT_INDEXING": "1". If you are deploying to Linux Consumption, also add "PYTHON_ISOLATE_WORKER_DEPENDENCIES": "1". When running locally, you also need to add these same settings to the local.settings.json project file.