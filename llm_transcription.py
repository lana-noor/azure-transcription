"""
Azure AI Speech LLM Transcription with Prompt Tuning
Enhanced transcription using LLM-powered speech model with contextual understanding.
"""

import os
import json
import requests
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION", "swedencentral")
LLM_SPEECH_ENDPOINT = f"https://{SPEECH_REGION}.api.cognitive.microsoft.com/speechtotext/transcriptions:transcribe?api-version=2025-10-15"

STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
INPUT_CONTAINER = os.getenv("INPUT_CONTAINER")
OUTPUT_FOLDER = r"C:\Users\lananoor\OneDrive - Microsoft\ADIC\TranscriptionCode\outputRawTranscription"

# Ensure output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ===================================
# PROMPT TUNING TEMPLATES
# ===================================

PROMPT_TEMPLATES = {
    "professional": [
        "Format the output as a professional business conversation.",
        "Use proper punctuation and capitalization.",
        "Identify key discussion points and action items."
    ],
    
    "meeting_summary": [
        "Transcribe this meeting conversation with clear speaker identification.",
        "Highlight important decisions, action items, and deadlines.",
        "Use professional business language and proper formatting."
    ],
    
    "call_center": [
        "Transcribe this customer service call with clear speaker labels.",
        "Identify customer concerns, agent responses, and resolution steps.",
        "Pay attention to product names, account numbers, and technical terms."
    ],
    
    "medical": [
        "Transcribe this medical conversation with attention to medical terminology.",
        "Pay attention to medication names, dosages, symptoms, and diagnoses.",
        "Maintain professional medical documentation standards."
    ],
    
    "legal": [
        "Transcribe this legal conversation with precise accuracy.",
        "Pay attention to legal terms, case numbers, dates, and proper names.",
        "Use formal legal documentation style."
    ],
    
    "interview": [
        "Transcribe this interview with clear question and answer formatting.",
        "Identify interviewer and interviewee responses separately.",
        "Capture key insights and important statements verbatim."
    ],
    
    "lecture": [
        "Transcribe this educational lecture or presentation.",
        "Organize content into clear sections and key points.",
        "Pay attention to technical terms, definitions, and examples."
    ],
    
    "casual": [
        "Transcribe this casual conversation naturally.",
        "Preserve the conversational tone and informal language.",
        "Include natural speech patterns and expressions."
    ],
    
    "technical": [
        "Transcribe this technical discussion with attention to technical terminology.",
        "Pay attention to acronyms, technical specifications, and industry jargon.",
        "Maintain technical accuracy and precision."
    ],
    
    "custom": [
        # Users can modify this for their specific needs
        "Transcribe the conversation with high accuracy.",
        "Use appropriate formatting and punctuation."
    ]
}


def get_prompt_for_style(style="casual", custom_prompts=None):
    """
    Get prompt tuning text based on the desired output style.
    
    Args:
        style: One of the predefined styles or 'custom'
        custom_prompts: List of custom prompt strings (used when style='custom')
    
    Returns:
        List of prompt strings
    """
    if style == "custom" and custom_prompts:
        return custom_prompts
    
    return PROMPT_TEMPLATES.get(style, PROMPT_TEMPLATES["casual"])


def transcribe_with_llm(audio_path, task="transcribe", target_language=None, 
                        prompt_style="casual", custom_prompts=None,
                        enable_diarization=True, max_speakers=None,
                        profanity_filter="Masked"):
    """
    Transcribe audio using Azure LLM Speech API with prompt tuning.
    
    Args:
        audio_path: Path to the audio file
        task: 'transcribe' or 'translate'
        target_language: Target language code for translation (e.g., 'en', 'es', 'fr')
        prompt_style: Style of transcription (see PROMPT_TEMPLATES keys)
        custom_prompts: Custom prompt list (overrides prompt_style if provided)
        enable_diarization: Enable speaker diarization
        max_speakers: Maximum number of speakers (optional)
        profanity_filter: 'Masked', 'Removed', or 'None'
    
    Returns:
        Dictionary containing transcription results
    """
    print(f"\n{'='*60}")
    print(f"LLM Speech Transcription")
    print(f"{'='*60}")
    print(f"Audio file: {os.path.basename(audio_path)}")
    print(f"Task: {task}")
    print(f"Prompt style: {prompt_style}")
    if target_language:
        print(f"Target language: {target_language}")
    print(f"Diarization: {'Enabled' if enable_diarization else 'Disabled'}")
    print(f"{'='*60}\n")
    
    # Prepare headers
    headers = {
        "Ocp-Apim-Subscription-Key": SPEECH_KEY
    }
    
    # Get prompts based on style
    prompts = custom_prompts if custom_prompts else get_prompt_for_style(prompt_style)
    
    # Build the definition
    definition = {
        "enhancedMode": {
            "enabled": True,
            "task": task,
            "prompt": prompts
        },
        "profanityFilterMode": profanity_filter
    }
    
    # Add target language for translation
    if task == "translate" and target_language:
        definition["enhancedMode"]["targetLanguage"] = target_language
    
    # Add diarization settings (only for transcribe task)
    if enable_diarization and task == "transcribe":
        definition["diarization"] = {
            "enabled": True
        }
        if max_speakers:
            definition["diarization"]["maxSpeakers"] = max_speakers

    # Prepare multipart form data
    files = {
        'audio': (os.path.basename(audio_path), open(audio_path, 'rb'), 'audio/wav'),
        'definition': (None, json.dumps(definition), 'application/json')
    }

    print("Sending request to Azure LLM Speech API...")
    print(f"Prompts being used:")
    for i, prompt in enumerate(prompts, 1):
        print(f"  {i}. {prompt}")
    print()

    # Make the API request
    try:
        response = requests.post(LLM_SPEECH_ENDPOINT, headers=headers, files=files)

        # Close the file
        files['audio'][1].close()

        if response.status_code == 200:
            result = response.json()
            print("✓ Transcription completed successfully!")
            return result
        else:
            raise Exception(f"API request failed: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"✗ Error during transcription: {str(e)}")
        raise


def save_transcription_result(result, output_filename, audio_filename):
    """Save the LLM transcription result to a JSON file."""
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    # Add metadata
    result_with_metadata = {
        "source_audio": audio_filename,
        "transcription_type": "llm_enhanced",
        "timestamp": datetime.now().isoformat(),
        "duration_ms": result.get("durationMilliseconds", 0),
        "transcription_data": result
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result_with_metadata, f, indent=2, ensure_ascii=False)

    print(f"✓ Transcription saved to: {output_path}")
    return output_path


def display_transcription_summary(result):
    """Display a summary of the transcription results."""
    print(f"\n{'='*60}")
    print("TRANSCRIPTION SUMMARY")
    print(f"{'='*60}")

    duration_ms = result.get("durationMilliseconds", 0)
    duration_sec = duration_ms / 1000
    print(f"Duration: {duration_sec:.2f} seconds ({duration_ms} ms)")

    combined_phrases = result.get("combinedPhrases", [])
    if combined_phrases:
        print(f"\nFull Transcription:")
        print("-" * 60)
        for phrase in combined_phrases:
            text = phrase.get("text", "")
            print(f"{text}\n")

    phrases = result.get("phrases", [])
    print(f"\nSegments: {len(phrases)}")

    # Show language detection
    languages_detected = set()
    for phrase in phrases:
        locale = phrase.get("locale", "")
        if locale:
            languages_detected.add(locale)

    if languages_detected:
        print(f"Languages detected: {', '.join(languages_detected)}")

    print(f"{'='*60}\n")


def process_local_file(audio_path, **kwargs):
    """Process a local audio file with LLM transcription."""
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    print(f"Processing local file: {audio_path}")

    # Transcribe
    result = transcribe_with_llm(audio_path, **kwargs)

    # Display summary
    display_transcription_summary(result)

    # Save result
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    output_filename = f"{base_name}_llm_transcription.json"
    save_transcription_result(result, output_filename, os.path.basename(audio_path))

    return result


def process_blob_file(blob_name, **kwargs):
    """Download and process a file from Azure Blob Storage."""
    print(f"Downloading from blob storage: {blob_name}")

    # Download blob to temp file
    blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container=INPUT_CONTAINER, blob=blob_name)

    # Create temp directory
    temp_dir = os.path.join(OUTPUT_FOLDER, "temp")
    os.makedirs(temp_dir, exist_ok=True)

    temp_path = os.path.join(temp_dir, blob_name)

    with open(temp_path, "wb") as f:
        download_stream = blob_client.download_blob()
        f.write(download_stream.readall())

    print(f"✓ Downloaded to: {temp_path}")

    # Process the file
    result = process_local_file(temp_path, **kwargs)

    # Clean up temp file
    os.remove(temp_path)

    return result


def main():
    """Main function with example usage."""
    print("Azure AI Speech LLM Transcription with Prompt Tuning")
    print("=" * 60)

    # Example: Process the demo file with casual style
    demo_file = r"C:\Users\lananoor\OneDrive - Microsoft\ADIC\TranscriptionCode\demodata\sampledata_audiofiles_katiesteve.wav"

    if os.path.exists(demo_file):
        print("\n📝 Casual Conversation Transcription")
        process_local_file(
            demo_file,
            task="transcribe",
            prompt_style="casual",
            enable_diarization=True,
            max_speakers=5,
            profanity_filter="Masked"
        )
    else:
        print(f"Demo file not found: {demo_file}")


if __name__ == "__main__":
    main()

