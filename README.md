# Azure AI Speech Transcription Suite

This project provides Python scripts to transcribe audio files using Azure AI Speech Service with multiple transcription methods, speaker diarization, and PDF generation.

## Features

### 🆕 LLM-Enhanced Transcription 
- **🧠 AI-Powered Intelligence**: Large language model enhanced transcription with deep contextual understanding
- **🎯 Prompt Tuning**: Customize output style and formatting with 12+ pre-configured prompts
- **⚡ Ultra-Fast Processing**: GPU-accelerated inference (faster than real-time)
- **🌍 Translation Support**: Translate audio to 9 different languages
- **🗣️ Speaker Diarization**: Identify and label different speakers
- **📝 Advanced Formatting**: Better punctuation, capitalization, and structure
- **🎨 Flexible Styles**: Meeting summaries, call center, medical, legal, technical, casual, and more

### Standard Batch Transcription
- **📦 Batch Processing**: Automatically transcribe all `.wav` files from Azure Blob Storage
- **🔄 Reliable Processing**: Proven batch transcription API for multiple files
- **⏱️ Word-level Timestamps**: Precise timing information for each word
- **🗣️ Speaker Diarization**: Identify and label different speakers

### PDF Generation
- **📄 Formatted PDFs**: Convert raw JSON transcriptions to nicely formatted PDFs
- **👥 Speaker Labels**: Clear speaker identification in documents
- **☁️ Automatic Upload**: PDFs saved locally and uploaded to Azure Blob Storage

## Prerequisites

- Python 3.8 or higher
- Azure Speech Service subscription or Microsoft Foundry Project Resource 
   - For Foundry Project resource, navigate to the Azure Portal, navigate to your Foundry project, and under "Resource Management", navigate to "Keys and Endpoint", under "AI Services", copy "KEY 1" and the "Speech to Text (Standard)" endpoint to use the Azure AI Speech APIs 
- Azure Storage Account with blob containers

## Installation and Setup

Follow these steps to set up your environment and run the transcription scripts:

### Step 1: Create a Virtual Environment

Create a Python virtual environment to isolate project dependencies:

```powershell
python -m venv venv
```

### Step 2: Activate the Virtual Environment

Activate the virtual environment (PowerShell):

```powershell
.\venv\Scripts\Activate.ps1
```

> **Note**: If you encounter an execution policy error, run PowerShell as Administrator and execute:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

For other shells:
- **Command Prompt (Windows)**: `venv\Scripts\activate.bat`
- **Bash (Linux/Mac)**: `source venv/bin/activate`

### Step 3: Authenticate with Azure

Log in to your Azure account using Azure Developer CLI:

```powershell
azd auth login
```

This will open a browser window for you to authenticate. Make sure you're logged into the correct Azure subscription that contains your Speech Service and Storage Account.

### Step 4: Install Python Dependencies

Install all required Python packages:

```powershell
pip install -r requirements.txt
```

This will install:
- `azure-storage-blob` - For Azure Blob Storage operations
- `azure-cognitiveservices-speech` - For Azure Speech Service
- `requests` - For HTTP API calls
- `reportlab` - For PDF generation
- `python-dotenv` - For environment variable management

### Step 5: Configure Environment Variables

Your `.env` file is already configured with Azure credentials. Verify it contains:

```env
AZURE_SPEECH_KEY=your_speech_key
AZURE_SPEECH_REGION=swedencentral
SPEECH_TO_TEXT_ENDPOINT=https://swedencentral.stt.speech.microsoft.com
AZURE_STORAGE_CONNECTION_STRING=your_connection_string
AZURE_STORAGE_ACCOUNT_NAME=your_storage_account
AZURE_STORAGE_SAS_TOKEN=your_sas_token
```

## Project Structure

```
TranscriptionCode/
├── 📜 Scripts
│   ├── llm_transcription.py           # 🆕 LLM-enhanced transcription (RECOMMENDED)
│   ├── run_llm_transcription.py       # 🆕 Easy-to-use LLM runner
│   ├── batch_transcription.py         # Standard batch transcription
│   ├── convert_to_pdf.py              # PDF conversion script
│   ├── fix_wav.py                     # Audio format converter (FFmpeg)
│   └── test_llm_api.py                # Test LLM API availability
│
├── ⚙️ Configuration
│   ├── .env                           # Environment variables (DO NOT commit)
│   ├── env-example                    # Example environment file
│   ├── requirements.txt               # Python dependencies
│   └── prompt_config.json             # 🆕 Prompt templates configuration
│
├── 📖 Documentation
│   ├── README.md                      # This file - comprehensive guide
│   ├── LLM_TRANSCRIPTION_GUIDE.md     # Detailed LLM guide
│   ├── QUICK_REFERENCE.md             # Quick reference
│   └── WHATS_NEW_LLM.md               # LLM features summary
│
├── 📁 Output Folders
│   ├── outputRawTranscription/        # Raw JSON transcriptions
│   └── outputPDF/                     # Generated PDF files
│
└── 🎵 Sample Data
    └── demodata/                      # Sample audio files
```

## Usage

Now that your environment is set up, you can choose between LLM-enhanced transcription (recommended) or standard batch transcription.

> **Important**: Make sure your virtual environment is activated before running the scripts:
> ```powershell
> .\venv\Scripts\Activate.ps1
> ```

---

## 🚀 Method 1: LLM-Enhanced Transcription 

The LLM Speech API provides **enhanced transcription** powered by large language models with deep contextual understanding, prompt tuning, and ultra-fast GPU-accelerated processing.

```powershell
python llm_transcription.py
```

This will process the demo file with example configurations.

### 🎯 Available Prompt Styles

Choose the right style for your content:

| Style | Best For | Description |
|-------|----------|-------------|
| **`casual`** ⭐ | Casual conversations | Natural tone, preserves informal language and expressions |
| **`meeting_summary`** | Business meetings | Speaker ID, decisions, action items, deadlines |
| **`call_center`** | Customer service | Customer concerns, agent responses, resolution steps |
| **`medical`** | Medical consultations | Medical terminology, medications, dosages, diagnoses |
| **`legal`** | Legal conversations | Precise accuracy, legal terms, case numbers, dates |
| **`interview`** | Interviews, Q&A | Clear Q&A structure, key insights |
| **`lecture`** | Educational content | Organized sections, technical terms, definitions |
| **`technical`** | Technical discussions | Acronyms, specifications, industry jargon |
| **`sales_call`** | Sales conversations | Needs, objections, features, next steps |
| **`training_session`** | Training content | Instruction steps, procedures, best practices |
| **`podcast`** | Podcast episodes | Natural flow, speaker identification |
| **`professional`** | Business conversations | Professional formatting, key discussion points |
| **`custom`** | Your specific needs | Define your own prompts |

### Translation Feature

Translate audio to a different language:

**Supported languages:**
- `en` - English
- `es` - Spanish
- `fr` - French
- `de` - German
- `it` - Italian
- `pt` - Portuguese
- `zh` - Chinese
- `ja` - Japanese
- `ko` - Korean

### Custom Prompts

Create your own prompts for specific needs:

**Example 1: Financial Advisory Call**
```python
PROMPT_STYLE = "custom"
CUSTOM_PROMPTS = [
    "Transcribe this financial advisory conversation.",
    "Pay attention to investment products, account numbers, and dollar amounts.",
    "Identify client questions and advisor recommendations clearly.",
    "Highlight any compliance-related statements or disclosures."
]
```

**Example 2: Technical Support Call**
```python
PROMPT_STYLE = "custom"
CUSTOM_PROMPTS = [
    "Transcribe this technical support conversation.",
    "Pay attention to error codes, software versions, and troubleshooting steps.",
    "Identify the problem description and solution provided.",
    "Format as a clear problem-solution documentation."
]
```

### 📊 What Makes LLM Transcription Different?

| Feature | Standard Batch | LLM Transcription |
|---------|---------------|-------------------|
| **Speed** | Slower (1-2x audio length) | ⚡ Ultra-fast (GPU accelerated) |
| **Context** | Basic word recognition | 🧠 Deep contextual understanding |
| **Customization** | Limited | 🎯 Prompt tuning for style/format |
| **Output Quality** | Good | ✨ Enhanced with LLM intelligence |
| **Translation** | ❌ Not available | ✅ 9 languages supported |
| **Use Cases** | General transcription | Meetings, calls, summaries, specialized content |

### 📝 LLM Output Format

The LLM transcription produces JSON output with:

```json
{
  "source_audio": "filename.wav",
  "transcription_type": "llm_enhanced",
  "timestamp": "2026-01-28T...",
  "duration_ms": 57187,
  "transcription_data": {
    "durationMilliseconds": 57187,
    "combinedPhrases": [
      {
        "text": "Full transcription text here..."
      }
    ],
    "phrases": [
      {
        "offsetMilliseconds": 80,
        "durationMilliseconds": 6960,
        "text": "Segment text here...",
        "words": [...],
        "locale": "en-us",
        "speaker": 1
      }
    ]
  }
}
```
---

## Method 2: Standard Batch Transcription

For processing multiple files from blob storage:

```powershell
python batch_transcription.py
```

This script will:
1. List all `.wav` files in the Azure Blob Storage container
2. Create a batch transcription job for each file with diarization enabled
3. Wait for transcription to complete
4. Download the results as JSON files to `outputRawTranscription/`

**Note**: Transcription can take several minutes depending on audio length.

**When to use:**
- Processing many files at once
- Don't need prompt customization
- Standard quality is sufficient

---

## 📄 Convert to PDF

Run the PDF conversion script to convert all JSON transcriptions to formatted PDFs:

```powershell
python convert_to_pdf.py
```

This script will:
1. Read all JSON files from `outputRawTranscription/`
2. Parse the transcription data with speaker information
3. Generate nicely formatted PDFs with:
   - Document metadata (source file, duration, timestamp)
   - Speaker-labeled transcription
   - Timestamps for each speaker segment
4. Save PDFs to `outputPDF/` locally
5. Upload PDFs to the blob container specified in `OUTPUT_CONTAINER`

## Configuration

### Azure Blob Storage Containers

Configure these in your `.env` file:

- **`INPUT_CONTAINER`**: Container with your `.wav` files
- **`OUTPUT_CONTAINER`**: Container for PDF output

### Speech Service Settings

#### LLM Transcription Settings
- **API Version**: 2025-10-15
- **Enhanced Mode**: Enabled (LLM-powered)
- **Prompt Tuning**: Customizable (12+ styles)
- **Diarization**: Optional (identifies different speakers)
- **Translation**: Optional (9 languages)
- **Profanity Filter**: Masked, Removed, or None
- **Max Duration**: 2 hours
- **Max File Size**: 300 MB

#### Standard Batch Transcription Settings
- **Locale**: en-US (English - United States)
- **Diarization**: Enabled (identifies different speakers)
- **Word-level Timestamps**: Enabled
- **Punctuation**: Automatic
- **Profanity Filter**: Masked

## Output Format

### LLM Transcription Output (JSON)
Enhanced output with:
- **Full transcription text** in `combinedPhrases`
- **Speaker-segmented phrases** with timestamps
- **Word-level details** with confidence scores
- **Language detection** per segment
- **Metadata**: source file, duration, timestamp
- **Transcription type**: `llm_enhanced`

Example structure:
```json
{
  "source_audio": "audio.wav",
  "transcription_type": "llm_enhanced",
  "timestamp": "2026-01-28T...",
  "duration_ms": 57187,
  "transcription_data": {
    "combinedPhrases": [...],
    "phrases": [...]
  }
}
```

### Standard Batch Transcription Output (JSON)
Contains detailed information including:
- Speaker identification
- Word-level timestamps
- Confidence scores
- Multiple recognition alternatives

### PDF Format
Formatted document with:
- Title and metadata section
- Speaker-labeled transcription
- Timestamps for each segment
- Professional styling and layout

## Quick Reference

### 🚀 Complete Setup (First Time)

```powershell
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 3. Authenticate with Azure
azd auth login

# 4. Install dependencies
pip install -r requirements.txt
```

### 📝 Running Transcriptions

**LLM Transcription (Recommended):**
```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

python llm_transcription.py
```

**Batch Transcription (Multiple Files):**
```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Process all files in blob storage
python batch_transcription.py
```

**Convert to PDF:**
```powershell
python convert_to_pdf.py
```

### 💡 Tips

- ⭐ Use **LLM transcription** for single files and better quality
- 📦 Use **batch transcription** for processing many files at once
- 🎯 Choose the right **prompt style** for your content type
- 🗣️ Enable **diarization** to identify different speakers
- 📁 Check **outputRawTranscription/** for JSON results
- 📄 Use **convert_to_pdf.py** to create readable documents
- 🌍 Use **translation** feature to convert audio to different languages

## 📚 API References

- [Azure LLM Speech API](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/llm-speech)
- [Azure Speech Batch Transcription](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/batch-transcription)
- [Batch Transcription REST API](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/batch-transcription-get?pivots=rest-api)
- [Supported Regions](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/regions)


