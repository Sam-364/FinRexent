"""
Ollama LLM Client for FinRexent Agent
"""
import requests
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime

from utils.logger import logger
from utils.config import config

class OllamaClient:
    """Client for Ollama LLM service"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.1:8b"):
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
        
        # Load configuration
        ollama_config = config.get_ollama_config()
        self.timeout = ollama_config.get('timeout', 30)
        self.max_tokens = ollama_config.get('max_tokens', 2048)
        self.temperature = ollama_config.get('temperature', 0.7)
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> Optional[str]:
        """Generate response from Ollama"""
        try:
            payload = {
                'model': self.model,
                'prompt': prompt,
                'stream': False,
                'options': {
                    'temperature': self.temperature,
                    'num_predict': self.max_tokens
                }
            }
            
            if system_prompt:
                payload['system'] = system_prompt
            
            start_time = time.time()
            
            response = self.session.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout
            )
            
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get('response', '')
                
                logger.log_llm_request(
                    model=self.model,
                    prompt_length=len(prompt),
                    response_time=response_time
                )
                
                return generated_text
            else:
                logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating response from Ollama: {str(e)}")
            return None
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text using LLM"""
        prompt = f"""
        Analyze the sentiment of the following financial news text. 
        Provide a sentiment score between -1 (very negative) and 1 (very positive) 
        and explain your reasoning.
        
        Text: {text}
        
        Respond in JSON format:
        {{
            "sentiment": "positive/negative/neutral",
            "score": 0.0,
            "confidence": 0.0,
            "reasoning": "explanation"
        }}
        """
        
        response = self.generate(prompt)
        if response:
            try:
                # Try to extract JSON from response
                import re
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                else:
                    return {
                        'sentiment': 'neutral',
                        'score': 0.0,
                        'confidence': 0.5,
                        'reasoning': response
                    }
            except json.JSONDecodeError:
                return {
                    'sentiment': 'neutral',
                    'score': 0.0,
                    'confidence': 0.5,
                    'reasoning': response
                }
        
        return {
            'sentiment': 'neutral',
            'score': 0.0,
            'confidence': 0.0,
            'reasoning': 'Unable to analyze'
        }
    
    def extract_stock_mentions(self, text: str) -> List[str]:
        """Extract stock tickers mentioned in text"""
        prompt = f"""
        Extract all Indian stock tickers (NSE format with .NS suffix) mentioned in the following text.
        Return only the ticker symbols, one per line.
        
        Text: {text}
        
        Example format:
        RELIANCE.NS
        HDFCBANK.NS
        TCS.NS
        """
        
        response = self.generate(prompt)
        if response:
            # Extract ticker symbols
            import re
            ticker_pattern = r'\b[A-Z]{2,5}\.NS\b'
            tickers = re.findall(ticker_pattern, response.upper())
            return list(set(tickers))
        
        return []
    
    def analyze_stock_fundamentals(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze stock fundamentals using LLM"""
        prompt = f"""
        Analyze the following stock fundamental data and provide investment insights:
        
        Stock: {stock_data.get('symbol', 'Unknown')}
        Company: {stock_data.get('name', 'Unknown')}
        Sector: {stock_data.get('sector', 'Unknown')}
        Market Cap: {stock_data.get('market_cap', 'Unknown')}
        P/E Ratio: {stock_data.get('pe_ratio', 'Unknown')}
        Dividend Yield: {stock_data.get('dividend_yield', 'Unknown')}
        Beta: {stock_data.get('beta', 'Unknown')}
        
        Provide analysis in JSON format:
        {{
            "strengths": ["list of strengths"],
            "weaknesses": ["list of weaknesses"],
            "opportunities": ["list of opportunities"],
            "threats": ["list of threats"],
            "investment_rating": "buy/hold/sell",
            "confidence": 0.0,
            "reasoning": "detailed explanation"
        }}
        """
        
        response = self.generate(prompt)
        if response:
            try:
                import re
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        
        return {
            'strengths': [],
            'weaknesses': [],
            'opportunities': [],
            'threats': [],
            'investment_rating': 'hold',
            'confidence': 0.5,
            'reasoning': response or 'Unable to analyze'
        }
    
    def generate_investment_recommendation(self, 
                                         stock_data: Dict[str, Any],
                                         news_data: List[Dict[str, Any]],
                                         market_conditions: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive investment recommendation"""
        
        # Prepare context
        news_summary = "\n".join([
            f"- {news['title']} (Sentiment: {news.get('sentiment', 'neutral')})"
            for news in news_data[:5]
        ])
        
        prompt = f"""
        As a financial advisor, provide a comprehensive investment recommendation for {stock_data.get('symbol', 'this stock')}.
        
        Stock Information:
        - Symbol: {stock_data.get('symbol', 'Unknown')}
        - Company: {stock_data.get('name', 'Unknown')}
        - Sector: {stock_data.get('sector', 'Unknown')}
        - Market Cap: {stock_data.get('market_cap', 'Unknown')}
        - P/E Ratio: {stock_data.get('pe_ratio', 'Unknown')}
        - Current Price: {stock_data.get('current_price', 'Unknown')}
        
        Recent News:
        {news_summary}
        
        Market Conditions:
        - Market Trend: {market_conditions.get('trend', 'Unknown')}
        - Volatility: {market_conditions.get('volatility', 'Unknown')}
        - Sector Performance: {market_conditions.get('sector_performance', 'Unknown')}
        
        Provide recommendation in JSON format:
        {{
            "recommendation": "buy/hold/sell",
            "confidence": 0.0,
            "target_price": 0.0,
            "stop_loss": 0.0,
            "time_horizon": "short/medium/long",
            "risk_level": "low/medium/high",
            "reasoning": "detailed explanation",
            "key_factors": ["factor1", "factor2", "factor3"],
            "investment_amount_suggestion": "explanation of suggested investment amount"
        }}
        """
        
        response = self.generate(prompt)
        if response:
            try:
                import re
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        
        return {
            'recommendation': 'hold',
            'confidence': 0.5,
            'target_price': 0.0,
            'stop_loss': 0.0,
            'time_horizon': 'medium',
            'risk_level': 'medium',
            'reasoning': response or 'Unable to generate recommendation',
            'key_factors': [],
            'investment_amount_suggestion': 'Consult with financial advisor'
        }
    
    def suggest_portfolio_allocation(self, 
                                   available_capital: float,
                                   risk_profile: str,
                                   preferred_sectors: List[str]) -> Dict[str, Any]:
        """Suggest portfolio allocation strategy"""
        
        prompt = f"""
        As a portfolio manager, suggest an optimal portfolio allocation strategy:
        
        Available Capital: ₹{available_capital:,.2f}
        Risk Profile: {risk_profile}
        Preferred Sectors: {', '.join(preferred_sectors)}
        
        Provide allocation strategy in JSON format:
        {{
            "total_allocation": 0.0,
            "sector_allocation": {{
                "sector_name": {{
                    "percentage": 0.0,
                    "amount": 0.0,
                    "reasoning": "explanation"
                }}
            }},
            "risk_management": {{
                "max_position_size": 0.0,
                "stop_loss_strategy": "explanation",
                "diversification_rules": ["rule1", "rule2"]
            }},
            "recommended_stocks": [
                {{
                    "ticker": "SYMBOL.NS",
                    "allocation_percentage": 0.0,
                    "allocation_amount": 0.0,
                    "reasoning": "explanation"
                }}
            ],
            "overall_strategy": "detailed explanation"
        }}
        """
        
        response = self.generate(prompt)
        if response:
            try:
                import re
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        
        return {
            'total_allocation': 0.0,
            'sector_allocation': {},
            'risk_management': {
                'max_position_size': 0.0,
                'stop_loss_strategy': 'Standard 5% stop loss',
                'diversification_rules': ['Diversify across sectors', 'Limit single stock exposure']
            },
            'recommended_stocks': [],
            'overall_strategy': response or 'Unable to generate allocation strategy'
        }
    
    def is_model_available(self) -> bool:
        """Check if the specified model is available"""
        try:
            response = self.session.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                models = response.json().get('models', [])
                return any(self.model in model.get('name', '') for model in models)
            return False
        except Exception as e:
            logger.error(f"Error checking model availability: {e}")
            return False
    
    def list_available_models(self) -> List[str]:
        """List available models"""
        try:
            response = self.session.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                models = response.json().get('models', [])
                return [model.get('name', '') for model in models]
            return []
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return [] 