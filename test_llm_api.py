"""
Test Azure LLM Speech API with curl-like request
This script tests if the LLM Speech API is available in your region.
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION", "swedencentral")

# Test different API endpoints
ENDPOINTS = {
    "LLM Speech (2025-10-15)": f"https://{SPEECH_REGION}.api.cognitive.microsoft.com/speechtotext/transcriptions:transcribe?api-version=2025-10-15",
    "Standard Speech (v3.2)": f"https://{SPEECH_REGION}.api.cognitive.microsoft.com/speechtotext/v3.2/transcriptions"
}

def test_llm_api():
    """Test the LLM Speech API with a simple request."""
    
    audio_file = r"C:\Users\lananoor\OneDrive - Microsoft\ADIC\TranscriptionCode\demodata\conversationrecording_new.wav"
    
    if not os.path.exists(audio_file):
        print(f"❌ Audio file not found: {audio_file}")
        return
    
    print("=" * 70)
    print("Testing Azure LLM Speech API")
    print("=" * 70)
    print(f"Region: {SPEECH_REGION}")
    print(f"Audio file: {os.path.basename(audio_file)}")
    print()
    
    # Test LLM API
    endpoint = ENDPOINTS["LLM Speech (2025-10-15)"]
    print(f"Testing: {endpoint}")
    print()
    
    headers = {
        "Ocp-Apim-Subscription-Key": SPEECH_KEY
    }
    
    # Simple definition matching the curl example
    definition = {
        "enhancedMode": {
            "enabled": True,
            "task": "transcribe",
            "prompt": ["Transcribe this casual conversation naturally."]
        }
    }
    
    # Prepare multipart form data
    with open(audio_file, 'rb') as audio:
        files = {
            'audio': (os.path.basename(audio_file), audio, 'audio/wav'),
            'definition': (None, json.dumps(definition), 'application/json')
        }
        
        print("Sending request...")
        response = requests.post(endpoint, headers=headers, files=files)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    print()
    
    if response.status_code == 200:
        print("✅ SUCCESS! LLM Speech API is working in your region!")
        result = response.json()
        print(json.dumps(result, indent=2))
    elif "not supported" in response.text.lower():
        print("❌ LLM Speech API is NOT available in your region yet.")
        print()
        print("Possible solutions:")
        print("1. Use a different region (e.g., eastus, westus2, westeurope)")
        print("2. Use standard batch transcription (batch_transcription.py)")
        print("3. Wait for the feature to be available in Sweden Central")
    else:
        print(f"❌ Error: {response.text}")


def check_available_regions():
    """Show regions where LLM Speech might be available."""
    print("\n" + "=" * 70)
    print("Regions where LLM Speech API might be available:")
    print("=" * 70)
    
    # Common regions that typically get new features first
    regions = [
        "eastus",
        "eastus2", 
        "westus",
        "westus2",
        "westeurope",
        "northeurope",
        "southeastasia",
        "australiaeast"
    ]
    
    for region in regions:
        print(f"  - {region}")
    
    print()
    print("To test a different region:")
    print("1. Update AZURE_SPEECH_REGION in your .env file")
    print("2. Make sure you have a Speech resource in that region")
    print("3. Run this script again")


if __name__ == "__main__":
    test_llm_api()
    check_available_regions()

