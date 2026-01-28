# PowerShell script to test Azure LLM Speech API
# This is the PowerShell equivalent of the curl command

# Load environment variables from .env file
Get-Content .env | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') {
        $name = $matches[1]
        $value = $matches[2]
        Set-Variable -Name $name -Value $value -Scope Script
    }
}

# Configuration
$region = $AZURE_SPEECH_REGION
$apiKey = $AZURE_SPEECH_KEY
$audioFile = "C:\Users\lananoor\OneDrive - Microsoft\ADIC\TranscriptionCode\demodata\conversationrecording_new.wav"

# API endpoint
$endpoint = "https://$region.api.cognitive.microsoft.com/speechtotext/transcriptions:transcribe?api-version=2025-10-15"

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host "Testing Azure LLM Speech API" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host "Region: $region"
Write-Host "Endpoint: $endpoint"
Write-Host "Audio file: $audioFile"
Write-Host ""

# Check if audio file exists
if (-not (Test-Path $audioFile)) {
    Write-Host "Error: Audio file not found: $audioFile" -ForegroundColor Red
    exit 1
}

# Create the definition JSON
$definition = @{
    enhancedMode = @{
        enabled = $true
        task = "transcribe"
        prompt = @("Transcribe this casual conversation naturally.")
    }
} | ConvertTo-Json -Depth 10

Write-Host "Definition:" -ForegroundColor Cyan
Write-Host $definition
Write-Host ""

# Prepare multipart form data
$boundary = [System.Guid]::NewGuid().ToString()
$LF = "`r`n"

# Read audio file as bytes
$audioBytes = [System.IO.File]::ReadAllBytes($audioFile)
$audioFileName = Split-Path $audioFile -Leaf

# Build multipart form data manually
$bodyLines = @(
    "--$boundary",
    "Content-Disposition: form-data; name=`"audio`"; filename=`"$audioFileName`"",
    "Content-Type: audio/wav",
    "",
    [System.Text.Encoding]::GetEncoding("iso-8859-1").GetString($audioBytes),
    "--$boundary",
    "Content-Disposition: form-data; name=`"definition`"",
    "Content-Type: application/json",
    "",
    $definition,
    "--$boundary--"
)

$body = $bodyLines -join $LF

# Prepare headers
$headers = @{
    "Ocp-Apim-Subscription-Key" = $apiKey
    "Content-Type" = "multipart/form-data; boundary=$boundary"
}

Write-Host "Sending request..." -ForegroundColor Yellow

try {
    # Make the request
    $response = Invoke-WebRequest -Uri $endpoint -Method Post -Headers $headers -Body ([System.Text.Encoding]::GetEncoding("iso-8859-1").GetBytes($body)) -UseBasicParsing
    
    Write-Host ""
    Write-Host "SUCCESS!" -ForegroundColor Green
    Write-Host "Status Code: $($response.StatusCode)"
    Write-Host ""
    Write-Host "Response:" -ForegroundColor Cyan
    $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
    
} catch {
    Write-Host ""
    Write-Host "ERROR!" -ForegroundColor Red
    Write-Host "Status Code: $($_.Exception.Response.StatusCode.Value__)"
    Write-Host ""
    
    $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
    $responseBody = $reader.ReadToEnd()
    Write-Host "Response: $responseBody" -ForegroundColor Red
    
    if ($responseBody -like "*not supported*") {
        Write-Host ""
        Write-Host "The LLM Speech API is NOT available in region: $region" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Possible solutions:" -ForegroundColor Cyan
        Write-Host "  1. Try a different region (eastus, westus2, westeurope)"
        Write-Host "  2. Use standard batch transcription instead"
        Write-Host "  3. Wait for the feature to be available in your region"
    }
}

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan

