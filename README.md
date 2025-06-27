# FinRexent - Intelligent Financial Investment Agent

A sophisticated AI-powered financial investment agent designed to help Indian investors make informed stock investment decisions. The agent combines advanced LLM capabilities with real-time market data analysis and comprehensive news crawling to provide accurate investment recommendations.

## 🚀 Features

- **Intelligent Stock Analysis**: Advanced technical and fundamental analysis using multiple indicators
- **Real-time News Crawling**: Automated collection of financial news from multiple sources
- **LLM-Powered Recommendations**: Uses Ollama with Llama models for intelligent reasoning
- **Memory System**: Persistent memory to track investment decisions and market trends
- **Risk Assessment**: Comprehensive risk analysis and investment amount suggestions
- **Indian Market Focus**: Optimized for Indian stock markets (NSE/BSE)
- **Multi-source Data**: Integrates data from multiple financial sources

## 📁 Project Structure

```
FinRexent/
├── agent/                 # Core agent implementation
│   ├── __init__.py
│   ├── agent.py          # Main agent class
│   ├── memory.py         # Memory management system
│   ├── analysis.py       # Financial analysis tools
│   └── llm_client.py     # Ollama LLM integration
├── crawler/              # News and data crawling
│   ├── __init__.py
│   ├── crawler.py        # Main crawler class
│   ├── firecrawl_client.py # Firecrawl integration
│   └── sources.py        # Data source configurations
├── data/                 # Data storage
│   ├── news/            # Crawled news data
│   ├── stocks/          # Stock market data
│   └── memory/          # Agent memory storage
├── utils/               # Utility functions
│   ├── __init__.py
│   ├── config.py        # Configuration management
│   ├── logger.py        # Logging utilities
│   └── helpers.py       # Helper functions
├── tests/               # Test suite
│   ├── __init__.py
│   ├── test_agent.py
│   └── test_crawler.py
├── main.py              # Main application entry point
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## 🛠️ Installation

### Prerequisites

1. **Python 3.8+**
2. **Ollama** - Install from [ollama.ai](https://ollama.ai)
3. **Llama Model** - Download the model: `ollama pull llama3.1:8b`

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/FinRexent.git
   cd FinRexent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configurations
   ```

5. **Install TA-Lib** (Technical Analysis Library)
   ```bash
   # Ubuntu/Debian
   sudo apt-get install ta-lib
   
   # macOS
   brew install ta-lib
   
   # Windows - Download from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
   ```

## 🚀 Usage

### Basic Usage

```python
from agent.agent import FinRexentAgent
from crawler.crawler import StockNewsCrawler

# Initialize the agent
agent = FinRexentAgent()

# Get investment recommendations
recommendations = agent.get_investment_recommendations()

# Analyze specific stock
analysis = agent.analyze_stock("RELIANCE")

# Get investment amount suggestion
suggestion = agent.suggest_investment_amount("RELIANCE", 50000)
```

### Command Line Interface

```bash
# Run the main application
python main.py

# Get recommendations for specific stock
python main.py --stock RELIANCE

# Analyze market trends
python main.py --trends

# Crawl latest news
python main.py --crawl
```

## 🔧 Configuration

### Environment Variables (.env)

```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# API Keys (if needed)
ALPHA_VANTAGE_API_KEY=your_key_here
NEWS_API_KEY=your_key_here

# Database Configuration
DATABASE_URL=sqlite:///data/finrexent.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/finrexent.log

# Crawling Configuration
CRAWL_INTERVAL=3600  # seconds
MAX_NEWS_ARTICLES=100
```

## 📊 Features in Detail

### 1. Intelligent Stock Analysis

- **Technical Indicators**: RSI, MACD, Bollinger Bands, Moving Averages
- **Fundamental Analysis**: P/E ratios, market cap, dividend yields
- **Risk Metrics**: Beta, Sharpe ratio, maximum drawdown
- **Trend Analysis**: Support/resistance levels, breakout detection

### 2. News Crawling System

- **Multiple Sources**: Moneycontrol, Economic Times, Business Standard
- **Sentiment Analysis**: AI-powered news sentiment analysis
- **Entity Recognition**: Automatic company name extraction
- **Real-time Updates**: Scheduled crawling with configurable intervals

### 3. LLM Integration

- **Ollama Integration**: Local LLM deployment for privacy
- **Context-Aware Responses**: Memory-based reasoning
- **Investment Reasoning**: Detailed explanations for recommendations
- **Risk Assessment**: AI-powered risk evaluation

### 4. Memory System

- **Persistent Storage**: SQLite database for long-term memory
- **Context Tracking**: Investment history and market trends
- **Learning Capability**: Improves recommendations over time
- **Performance Tracking**: Historical recommendation accuracy

## 🤖 Agent Capabilities

### Investment Recommendations

The agent provides:
- **Stock Selection**: Best stocks based on current market conditions
- **Investment Amount**: Suggested investment amounts based on risk profile
- **Timing**: Optimal entry and exit points
- **Reasoning**: Detailed explanations for each recommendation

### Risk Management

- **Portfolio Diversification**: Suggests balanced portfolio allocation
- **Risk Assessment**: Individual stock and portfolio risk analysis
- **Stop Loss**: Automated stop-loss recommendations
- **Position Sizing**: Risk-adjusted position sizing

## 📈 Data Sources

### Market Data
- **Yahoo Finance**: Real-time stock prices and historical data
- **NSE/BSE**: Indian market data
- **Alpha Vantage**: Additional market data (optional)

### News Sources
- **Moneycontrol**: Indian financial news
- **Economic Times**: Business and market news
- **Business Standard**: Financial analysis and reports
- **Livemint**: Market insights and analysis

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_agent.py

# Run with coverage
pytest --cov=agent --cov=crawler
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

