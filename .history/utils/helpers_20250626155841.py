"""
Helper utilities for FinRexent
"""
import re
import json
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import yfinance as yf

def clean_company_name(name: str) -> str:
    """Clean and standardize company names"""
    if not name:
        return ""
    
    # Remove common suffixes and prefixes
    suffixes = [' Ltd', ' Limited', ' Inc', ' Corporation', ' Corp', ' Company', ' Co']
    prefixes = ['The ']
    
    cleaned = name.strip()
    
    for suffix in suffixes:
        if cleaned.endswith(suffix):
            cleaned = cleaned[:-len(suffix)]
    
    for prefix in prefixes:
        if cleaned.startswith(prefix):
            cleaned = cleaned[len(prefix):]
    
    return cleaned.strip()

def extract_ticker_from_text(text: str) -> List[str]:
    """Extract potential stock tickers from text"""
    # Pattern for common ticker formats
    patterns = [
        r'\b[A-Z]{2,5}\.NS\b',  # NSE tickers
        r'\b[A-Z]{2,5}\.BO\b',  # BSE tickers
        r'\b[A-Z]{2,5}\b'       # General ticker pattern
    ]
    
    tickers = []
    for pattern in patterns:
        matches = re.findall(pattern, text.upper())
        tickers.extend(matches)
    
    return list(set(tickers))

def calculate_risk_metrics(stock_data: pd.DataFrame) -> Dict[str, float]:
    """Calculate various risk metrics for a stock"""
    if stock_data.empty:
        return {}
    
    # Calculate daily returns
    stock_data['Daily_Return'] = stock_data['Close'].pct_change()
    
    # Volatility (annualized)
    volatility = stock_data['Daily_Return'].std() * (252 ** 0.5)
    
    # Maximum drawdown
    cumulative_returns = (1 + stock_data['Daily_Return']).cumprod()
    rolling_max = cumulative_returns.expanding().max()
    drawdown = (cumulative_returns - rolling_max) / rolling_max
    max_drawdown = drawdown.min()
    
    # Sharpe ratio (assuming risk-free rate of 6%)
    risk_free_rate = 0.06
    excess_returns = stock_data['Daily_Return'] - risk_free_rate/252
    sharpe_ratio = excess_returns.mean() / stock_data['Daily_Return'].std() * (252 ** 0.5)
    
    # Beta (if market data available)
    beta = 1.0  # Default value
    
    return {
        'volatility': volatility,
        'max_drawdown': max_drawdown,
        'sharpe_ratio': sharpe_ratio,
        'beta': beta
    }

def calculate_position_size(capital: float, risk_per_trade: float, stop_loss_pct: float) -> float:
    """Calculate position size based on risk management rules"""
    if stop_loss_pct <= 0:
        return 0
    
    risk_amount = capital * risk_per_trade
    position_size = risk_amount / stop_loss_pct
    
    return min(position_size, capital)  # Don't exceed total capital

def format_currency(amount: float, currency: str = "INR") -> str:
    """Format currency amounts"""
    if currency == "INR":
        return f"₹{amount:,.2f}"
    else:
        return f"{currency} {amount:,.2f}"

def format_percentage(value: float) -> str:
    """Format percentage values"""
    return f"{value:.2f}%"

def get_market_status() -> Dict[str, Any]:
    """Get current market status for Indian markets"""
    now = datetime.now()
    
    # Indian market hours (IST)
    market_start = now.replace(hour=9, minute=15, second=0, microsecond=0)
    market_end = now.replace(hour=15, minute=30, second=0, microsecond=0)
    
    is_market_open = market_start <= now <= market_end
    is_weekend = now.weekday() >= 5
    
    return {
        'is_open': is_market_open and not is_weekend,
        'current_time': now.strftime('%Y-%m-%d %H:%M:%S'),
        'market_start': market_start.strftime('%H:%M'),
        'market_end': market_end.strftime('%H:%M'),
        'is_weekend': is_weekend
    }

def validate_ticker(ticker: str) -> bool:
    """Validate if a ticker symbol is valid"""
    if not ticker:
        return False
    
    # Basic validation patterns
    valid_patterns = [
        r'^[A-Z]{2,5}$',  # Basic ticker
        r'^[A-Z]{2,5}\.NS$',  # NSE ticker
        r'^[A-Z]{2,5}\.BO$',  # BSE ticker
    ]
    
    for pattern in valid_patterns:
        if re.match(pattern, ticker.upper()):
            return True
    
    return False

def get_stock_info(ticker: str) -> Optional[Dict[str, Any]]:
    """Get basic stock information"""
    try:
        # Add .NS suffix if not present
        if not ticker.endswith(('.NS', '.BO')):
            ticker = ticker + '.NS'
        
        stock = yf.Ticker(ticker)
        info = stock.info
        
        if not info or 'symbol' not in info:
            return None
        
        return {
            'symbol': info.get('symbol', ''),
            'name': info.get('longName', ''),
            'sector': info.get('sector', ''),
            'industry': info.get('industry', ''),
            'market_cap': info.get('marketCap', 0),
            'pe_ratio': info.get('trailingPE', 0),
            'dividend_yield': info.get('dividendYield', 0),
            'beta': info.get('beta', 1.0)
        }
    except Exception:
        return None

def create_portfolio_summary(positions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a summary of portfolio positions"""
    if not positions:
        return {}
    
    total_value = sum(pos.get('value', 0) for pos in positions)
    total_cost = sum(pos.get('cost', 0) for pos in positions)
    total_pnl = total_value - total_cost
    total_pnl_pct = (total_pnl / total_cost * 100) if total_cost > 0 else 0
    
    # Calculate sector allocation
    sector_allocation = {}
    for pos in positions:
        sector = pos.get('sector', 'Unknown')
        value = pos.get('value', 0)
        sector_allocation[sector] = sector_allocation.get(sector, 0) + value
    
    return {
        'total_value': total_value,
        'total_cost': total_cost,
        'total_pnl': total_pnl,
        'total_pnl_pct': total_pnl_pct,
        'sector_allocation': sector_allocation,
        'position_count': len(positions)
    }

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations"""
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    
    # Limit length
    if len(filename) > 255:
        filename = filename[:255]
    
    return filename

def parse_date_range(date_range: str) -> Tuple[datetime, datetime]:
    """Parse date range string and return start and end dates"""
    now = datetime.now()
    
    range_mappings = {
        '1d': (now - timedelta(days=1), now),
        '5d': (now - timedelta(days=5), now),
        '1w': (now - timedelta(weeks=1), now),
        '1m': (now - timedelta(days=30), now),
        '3m': (now - timedelta(days=90), now),
        '6m': (now - timedelta(days=180), now),
        '1y': (now - timedelta(days=365), now),
        '2y': (now - timedelta(days=730), now),
        '5y': (now - timedelta(days=1825), now),
        'max': (now - timedelta(days=3650), now),  # 10 years max
    }
    
    return range_mappings.get(date_range.lower(), (now - timedelta(days=365), now)) 