# 🎤 Google Cloud Speech API Setup Guide

This guide will help you set up Google Cloud Speech-to-Text and Text-to-Speech APIs for your MCP chatbot.

## 📋 Prerequisites

- Google account
- Credit card (for billing verification - Google Cloud offers free tier)
- Basic familiarity with web interfaces

## 🚀 Step-by-Step Setup

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" at the top
3. Click "New Project"
4. Enter a project name (e.g., "mcp-chatbot-speech")
5. Click "Create"

### 2. Enable Required APIs

1. In your project, go to "APIs & Services" > "Library"
2. Search for and enable these APIs:
   - **Speech-to-Text API**
   - **Text-to-Speech API**
3. Click "Enable" for each API

### 3. Create Service Account

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Fill in the details:
   - **Name**: `mcp-chatbot-speech`
   - **Description**: `Service account for MCP chatbot speech features`
4. Click "Create and Continue"
5. For roles, add:
   - **Speech-to-Text Admin**
   - **Text-to-Speech Admin**
6. Click "Continue" and then "Done"

### 4. Download Credentials

1. Click on your newly created service account
2. Go to "Keys" tab
3. Click "Add Key" > "Create new key"
4. Choose "JSON" format
5. Click "Create" - this will download a JSON file
6. **Important**: Keep this file secure and never commit it to version control

### 5. Configure Environment Variables

1. Copy the downloaded JSON file to your project directory
2. Rename it to something like `google-credentials.json`
3. Update your `.env` file:

```bash
# Google Cloud Configuration
GOOGLE_APPLICATION_CREDENTIALS=./google-credentials.json
GOOGLE_CLOUD_PROJECT=your-project-id-here
```

4. Replace `your-project-id-here` with your actual project ID

### 6. Test the Setup

1. Run the speech chatbot:
   ```bash
   python speech_chatbot.py
   ```

2. Check the console output for:
   ```
   Google Cloud: Google Cloud credentials configured successfully.
   ```

## 🔧 Troubleshooting

### Common Issues

#### 1. "GOOGLE_APPLICATION_CREDENTIALS not set"
- **Solution**: Make sure the environment variable is set correctly
- **Check**: Verify the path in your `.env` file

#### 2. "Credentials file not found"
- **Solution**: Ensure the JSON file exists at the specified path
- **Check**: Use absolute path if relative path doesn't work

#### 3. "Permission denied" errors
- **Solution**: Verify the service account has the correct roles
- **Check**: Go to IAM & Admin > IAM and verify roles

#### 4. API quota exceeded
- **Solution**: Check your billing and quota limits
- **Check**: Go to APIs & Services > Quotas

### Billing Setup

1. Go to "Billing" in Google Cloud Console
2. Link a billing account to your project
3. Set up billing alerts to avoid unexpected charges
4. Monitor usage in the "Billing" section

## 💰 Cost Information

### Free Tier (Monthly)
- **Speech-to-Text**: 60 minutes
- **Text-to-Speech**: 4 million characters

### Paid Tier (After Free Tier)
- **Speech-to-Text**: $0.006 per 15 seconds
- **Text-to-Speech**: $4.00 per 1 million characters

### Cost Optimization Tips
1. Use shorter audio clips for speech recognition
2. Limit text-to-speech to essential responses
3. Monitor usage in Google Cloud Console
4. Set up billing alerts

## 🔒 Security Best Practices

1. **Never commit credentials to version control**
2. **Use environment variables for sensitive data**
3. **Restrict service account permissions to minimum required**
4. **Regularly rotate service account keys**
5. **Monitor API usage for unusual activity**

## 📱 Testing Speech Features

### 1. Start the Speech Chatbot
```bash
python speech_chatbot.py
```

### 2. Open Browser
Navigate to `http://localhost:8002`

### 3. Test Microphone
1. Click the microphone button
2. Allow microphone access when prompted
3. Speak a question (e.g., "What's the weather in Tokyo?")
4. Click stop when done

### 4. Verify Features
- ✅ Speech-to-text transcription
- ✅ Bot response generation
- ✅ Text-to-speech audio playback

## 🎯 Example Queries to Test

### Weather
- "What's the weather in London?"
- "How's the weather in New York?"
- "Weather forecast for Tokyo"

### Stocks
- "What's the stock price of Apple?"
- "Show me Tesla stock price"
- "Stock price of Microsoft"

### News
- "Get me technology news"
- "Show me sports headlines"
- "Latest business news"

## 🆘 Getting Help

### Google Cloud Support
- [Google Cloud Documentation](https://cloud.google.com/docs)
- [Speech-to-Text API Guide](https://cloud.google.com/speech-to-text/docs)
- [Text-to-Speech API Guide](https://cloud.google.com/text-to-speech/docs)

### Community Resources
- [Google Cloud Community](https://cloud.google.com/community)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/google-cloud-speech)

### Project Issues
- Check the console output for error messages
- Verify all environment variables are set
- Ensure the JSON credentials file is valid

## 🎉 Success Indicators

When everything is working correctly, you should see:

1. **Console Output**:
   ```
   Google Cloud: Google Cloud credentials configured successfully.
   🚀 Starting MCP Speech Chatbot...
   🌐 Web interface will be available at: http://localhost:8002
   ```

2. **Browser Interface**:
   - Clean, modern chat interface
   - Microphone button enabled
   - WebSocket connection established

3. **Speech Features**:
   - Microphone access granted
   - Audio recording works
   - Speech recognition accurate
   - Text-to-speech playback

## 🔄 Next Steps

Once speech features are working:

1. **Customize Voices**: Try different voice options
2. **Language Support**: Test with other languages
3. **Audio Quality**: Adjust recording parameters
4. **Integration**: Add speech to other chatbot interfaces

---

**Happy coding! 🎤🤖**
