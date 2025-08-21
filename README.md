# 🎤 MCP Speech-Enabled Chatbot

A powerful, speech-enabled chatbot built with the Model Context Protocol (MCP) that can provide real-time information about weather, stock prices, and news using voice commands.

## ✨ Features

- **🎤 Speech-to-Text**: Convert your voice to text using Google Cloud Speech-to-Text API
- **🔊 Text-to-Speech**: Listen to responses with Google Cloud Text-to-Speech API
- **🌤️ Weather Information**: Get current weather and forecasts for any city
- **📈 Stock Prices**: Real-time stock market data and company information
- **📰 News Updates**: Latest headlines and searchable news content
- **💬 Multiple Interfaces**: Web interface, terminal chatbot, and web chatbot
- **🔌 MCP Integration**: Built on the Model Context Protocol for AI assistant compatibility

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Cloud account with Speech-to-Text and Text-to-Speech APIs enabled
- Free API keys from:
  - [OpenWeatherMap](https://openweathermap.org/api) (Weather)
  - [Alpha Vantage](https://www.alphavantage.co/) (Stocks)
  - [NewsAPI.org](https://newsapi.org/) (News)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd mcp-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

4. **Configure Google Cloud credentials**
   - Download your service account credentials JSON file
   - Place it in the project directory as `google-credentials.json`
   - Update `.env` with your Google Cloud project ID

### Running the Chatbot

#### 🌐 Web Interface (Simple)
```bash
python web_interface.py
# Open http://localhost:8000
```

#### 💬 Web Chatbot (Interactive)
```bash
python web_chatbot.py
# Open http://localhost:8001
```

#### 🎤 Speech-Enabled Chatbot (Recommended)
```bash
python speech_chatbot_clean.py
# Open http://localhost:8002
```

#### 🖥️ Terminal Chatbot
```bash
python chatbot_interface.py
```

## 🏗️ Project Structure

```
mcp-chatbot/
├── services/                 # API service modules
│   ├── weather_service.py   # OpenWeatherMap integration
│   ├── stock_service.py     # Alpha Vantage integration
│   ├── news_service.py      # NewsAPI integration
│   └── speech_service.py    # Google Cloud Speech APIs
├── chatbot_interface.py     # Core NLP logic
├── web_interface.py         # Simple web interface
├── web_chatbot.py          # Web-based chatbot
├── speech_chatbot_clean.py # Speech-enabled chatbot
├── mcp_server.py           # MCP protocol server
├── config.py               # Configuration management
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with your API keys:

```env
# API Keys (Get free keys from these services)
OPENWEATHER_API_KEY=your_openweather_api_key
ALPHA_VANTAGE_API_KEY=your_alphavantage_api_key
NEWS_API_KEY=your_newsapi_key

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Google Cloud Configuration
GOOGLE_APPLICATION_CREDENTIALS=./google-credentials.json
GOOGLE_CLOUD_PROJECT=your_project_id
```

### Google Cloud Setup

1. Create a Google Cloud project
2. Enable Speech-to-Text and Text-to-Speech APIs
3. Create a service account and download credentials
4. Place credentials in `google-credentials.json`

## 📱 Usage Examples

### Voice Commands

- **Weather**: "What's the weather in San Francisco?"
- **Stocks**: "Show me Apple stock price"
- **News**: "Give me news on technology"

### Text Commands

- **Weather**: Type "weather in Tokyo"
- **Stocks**: Type "stock price of TSLA"
- **News**: Type "news on sports"

## 🧪 Testing

Test your setup with:

```bash
python test_services.py
```

This will validate all API keys and Google Cloud credentials.

## 🔌 MCP Integration

The chatbot implements the Model Context Protocol, making it compatible with AI assistants that support MCP. Run the MCP server with:

```bash
python mcp_server.py
```

## 🚀 Deployment

### Local Development
```bash
python speech_chatbot_clean.py
```

### Docker (Optional)
```bash
docker-compose up
```

### GitHub Pages
The web interface can be deployed to GitHub Pages for easy access.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [OpenWeatherMap](https://openweathermap.org/) for weather data
- [Alpha Vantage](https://www.alphavantage.co/) for stock market data
- [NewsAPI.org](https://newsapi.org/) for news content
- [Google Cloud](https://cloud.google.com/) for speech APIs
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/mcp-chatbot/issues) page
2. Review the configuration and API key setup
3. Ensure all dependencies are properly installed

---

**Happy chatting! 🎉**
