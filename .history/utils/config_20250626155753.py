"""
Configuration management for FinRexent
"""
import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

class Config:
    """Configuration manager for FinRexent"""
    
    def __init__(self, config_path: Optional[str] = None):
        # Load environment variables
        load_dotenv()
        
        # Default configuration
        self.default_config = {
            'ollama': {
                'base_url': 'http://localhost:11434',
                'model': 'llama3.1:8b',
                'timeout': 30,
                'max_tokens': 2048,
                'temperature': 0.7
            },
            'database': {
                'url': 'sqlite:///data/finrexent.db',
                'echo': False
            },
            'crawling': {
                'interval': 3600,  # seconds
                'max_articles': 100,
                'timeout': 30,
                'user_agent': 'FinRexent/1.0'
            },
            'analysis': {
                'lookback_period': '1y',
                'rsi_period': 14,
                'macd_fast': 12,
                'macd_slow': 26,
                'macd_signal': 9,
                'bollinger_period': 20,
                'bollinger_std': 2
            },
            'logging': {
                'level': 'INFO',
                'file': 'logs/finrexent.log',
                'max_size': 10 * 1024 * 1024,  # 10MB
                'backup_count': 5
            },
            'risk': {
                'max_portfolio_risk': 0.02,  # 2% max risk per position
                'max_correlation': 0.7,
                'min_diversification': 5,  # minimum stocks in portfolio
                'stop_loss_percentage': 0.05  # 5% stop loss
            },
            'indian_markets': {
                'nse_suffix': '.NS',
                'bse_suffix': '.BO',
                'market_hours': {
                    'start': '09:15',
                    'end': '15:30',
                    'timezone': 'Asia/Kolkata'
                }
            }
        }
        
        # Load custom config if provided
        self.config = self.default_config.copy()
        if config_path and os.path.exists(config_path):
            self.load_config(config_path)
        
        # Override with environment variables
        self._load_from_env()
    
    def _load_from_env(self):
        """Load configuration from environment variables"""
        env_mappings = {
            'OLLAMA_BASE_URL': ('ollama', 'base_url'),
            'OLLAMA_MODEL': ('ollama', 'model'),
            'OLLAMA_TIMEOUT': ('ollama', 'timeout'),
            'DATABASE_URL': ('database', 'url'),
            'CRAWL_INTERVAL': ('crawling', 'interval'),
            'MAX_NEWS_ARTICLES': ('crawling', 'max_articles'),
            'LOG_LEVEL': ('logging', 'level'),
            'LOG_FILE': ('logging', 'file'),
        }
        
        for env_var, config_path in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                # Navigate to nested config and set value
                current = self.config
                for key in config_path[:-1]:
                    current = current[key]
                current[config_path[-1]] = value
    
    def load_config(self, config_path: str):
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                custom_config = yaml.safe_load(f)
                self._merge_config(self.config, custom_config)
        except Exception as e:
            print(f"Warning: Could not load config file {config_path}: {e}")
    
    def _merge_config(self, base: Dict, update: Dict):
        """Recursively merge configuration dictionaries"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation"""
        keys = key.split('.')
        current = self.config
        
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return default
        
        return current
    
    def set(self, key: str, value: Any):
        """Set configuration value using dot notation"""
        keys = key.split('.')
        current = self.config
        
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        current[keys[-1]] = value
    
    def save_config(self, config_path: str):
        """Save current configuration to YAML file"""
        try:
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False, indent=2)
        except Exception as e:
            print(f"Error saving config to {config_path}: {e}")
    
    def get_ollama_config(self) -> Dict[str, Any]:
        """Get Ollama-specific configuration"""
        return self.config['ollama']
    
    def get_database_config(self) -> Dict[str, Any]:
        """Get database configuration"""
        return self.config['database']
    
    def get_crawling_config(self) -> Dict[str, Any]:
        """Get crawling configuration"""
        return self.config['crawling']
    
    def get_analysis_config(self) -> Dict[str, Any]:
        """Get analysis configuration"""
        return self.config['analysis']
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration"""
        return self.config['logging']
    
    def get_risk_config(self) -> Dict[str, Any]:
        """Get risk management configuration"""
        return self.config['risk']
    
    def get_indian_markets_config(self) -> Dict[str, Any]:
        """Get Indian markets configuration"""
        return self.config['indian_markets']

# Global configuration instance
config = Config() 