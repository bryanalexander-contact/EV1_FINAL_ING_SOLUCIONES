import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.inference import ChatCompletionsClient

# Load environment variables from .env file in the project root
load_dotenv()

# Expected environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
ENDPOINT_URL = os.getenv("ENDPOINT_URL")

if not GITHUB_TOKEN:
    raise EnvironmentError("GITHUB_TOKEN not set in .env")
if not ENDPOINT_URL:
    raise EnvironmentError("ENDPOINT_URL not set in .env")

# Initialize the Azure AI Inference client for GitHub Models
client = ChatCompletionsClient(
    endpoint=ENDPOINT_URL,
    credential=AzureKeyCredential(GITHUB_TOKEN)
)

# Model name constant
MODEL_NAME = "gpt-4o-mini"

def get_client():
    """Return a configured ChatCompletionsClient instance.

    The client is pre‑configured with the endpoint and authentication token.
    Users can import this function to obtain the shared client.
    """
    return client
