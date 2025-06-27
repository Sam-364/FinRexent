"""
Logging utilities for FinRexent
"""
import logging
import logging.handlers
import os
from pathlib import Path
from typing import Optional
from datetime import datetime

class FinRexentLogger:
    """Custom logger for FinRexent with file rotation and formatting"""
    
    def __init__(self, name: str = "FinRexent", log_file: Optional[str] = None, level: str = "INFO"):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        
        # Prevent duplicate handlers
        if self.logger.handlers:
            return
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s'
        )
        simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler with rotation
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(detailed_formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log critical message"""
        self.logger.critical(message)
    
    def log_stock_analysis(self, ticker: str, analysis_type: str, result: dict):
        """Log stock analysis results"""
        self.info(f"Stock Analysis - {ticker} - {analysis_type}: {result}")
    
    def log_investment_recommendation(self, ticker: str, recommendation: dict):
        """Log investment recommendations"""
        self.info(f"Investment Recommendation - {ticker}: {recommendation}")
    
    def log_news_crawled(self, source: str, count: int):
        """Log news crawling results"""
        self.info(f"News Crawled - {source}: {count} articles")
    
    def log_llm_request(self, model: str, prompt_length: int, response_time: float):
        """Log LLM request details"""
        self.debug(f"LLM Request - Model: {model}, Prompt Length: {prompt_length}, Response Time: {response_time:.2f}s")
    
    def log_error_with_context(self, error: Exception, context: str):
        """Log error with additional context"""
        self.error(f"Error in {context}: {str(error)}")
        if hasattr(error, '__traceback__'):
            import traceback
            self.error(f"Traceback: {traceback.format_exc()}")

# Global logger instance
logger = FinRexentLogger() 