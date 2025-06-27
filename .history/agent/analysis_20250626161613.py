"""
Financial Analysis Module for FinRexent Agent
"""
import pandas as pd
import numpy as np
import yfinance as yf
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

from utils.logger import logger
from utils.config import config
from utils.helpers import calculate_risk_metrics, format_currency, format_percentage

class FinancialAnalyzer:
    """Comprehensive financial analysis for stocks"""
    
    def __init__(self):
        self.analysis_config = config.get_analysis_config()
        self.risk_config = config.get_risk_config()
        self.indian_markets_config = config.get_indian_markets_config()
    
    def get_stock_data(self, ticker: str, period: str = "1y") -> Optional[pd.DataFrame]:
        """Get stock data from Yahoo Finance"""
        try:
            # Add NSE suffix if not present
            if not ticker.endswith(('.NS', '.BO')):
                ticker = ticker + self.indian_markets_config['nse_suffix']
            
            stock = yf.Ticker(ticker)
            data = stock.history(period=period)
            
            if data.empty:
                logger.warning(f"No data found for ticker: {ticker}")
                return None
            
            return data
            
        except Exception as e:
            logger.error(f"Error fetching data for {ticker}: {e}")
            return None
    
    def get_stock_info(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Get fundamental stock information"""
        try:
            if not ticker.endswith(('.NS', '.BO')):
                ticker = ticker + self.indian_markets_config['nse_suffix']
            
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
                'forward_pe': info.get('forwardPE', 0),
                'price_to_book': info.get('priceToBook', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'beta': info.get('beta', 1.0),
                'debt_to_equity': info.get('debtToEquity', 0),
                'return_on_equity': info.get('returnOnEquity', 0),
                'return_on_assets': info.get('returnOnAssets', 0),
                'current_ratio': info.get('currentRatio', 0),
                'quick_ratio': info.get('quickRatio', 0),
                'profit_margins': info.get('profitMargins', 0),
                'revenue_growth': info.get('revenueGrowth', 0),
                'earnings_growth': info.get('earningsGrowth', 0),
                'fifty_two_week_high': info.get('fiftyTwoWeekHigh', 0),
                'fifty_two_week_low': info.get('fiftyTwoWeekLow', 0),
                'fifty_day_average': info.get('fiftyDayAverage', 0),
                'two_hundred_day_average': info.get('twoHundredDayAverage', 0)
            }
            
        except Exception as e:
            logger.error(f"Error fetching stock info for {ticker}: {e}")
            return None
    
    def calculate_technical_indicators(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate technical indicators"""
        if data.empty:
            return {}
        
        try:
            indicators = {}
            
            # Moving Averages
            indicators['sma_20'] = data['Close'].rolling(window=20).mean().iloc[-1]
            indicators['sma_50'] = data['Close'].rolling(window=50).mean().iloc[-1]
            indicators['sma_200'] = data['Close'].rolling(window=200).mean().iloc[-1]
            
            # Exponential Moving Averages
            indicators['ema_12'] = data['Close'].ewm(span=12).mean().iloc[-1]
            indicators['ema_26'] = data['Close'].ewm(span=26).mean().iloc[-1]
            
            # RSI
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            indicators['rsi'] = 100 - (100 / (1 + rs.iloc[-1]))
            
            # MACD
            ema_12 = data['Close'].ewm(span=12).mean()
            ema_26 = data['Close'].ewm(span=26).mean()
            macd_line = ema_12 - ema_26
            signal_line = macd_line.ewm(span=9).mean()
            indicators['macd'] = macd_line.iloc[-1]
            indicators['macd_signal'] = signal_line.iloc[-1]
            indicators['macd_histogram'] = indicators['macd'] - indicators['macd_signal']
            
            # Bollinger Bands
            sma_20 = data['Close'].rolling(window=20).mean()
            std_20 = data['Close'].rolling(window=20).std()
            indicators['bb_upper'] = sma_20.iloc[-1] + (std_20.iloc[-1] * 2)
            indicators['bb_middle'] = sma_20.iloc[-1]
            indicators['bb_lower'] = sma_20.iloc[-1] - (std_20.iloc[-1] * 2)
            indicators['bb_position'] = (data['Close'].iloc[-1] - indicators['bb_lower']) / (indicators['bb_upper'] - indicators['bb_lower'])
            
            # Volume indicators
            indicators['volume_sma'] = data['Volume'].rolling(window=20).mean().iloc[-1]
            indicators['volume_ratio'] = data['Volume'].iloc[-1] / indicators['volume_sma']
            
            # Price momentum
            indicators['momentum_5'] = (data['Close'].iloc[-1] / data['Close'].iloc[-6]) - 1
            indicators['momentum_10'] = (data['Close'].iloc[-1] / data['Close'].iloc[-11]) - 1
            indicators['momentum_20'] = (data['Close'].iloc[-1] / data['Close'].iloc[-21]) - 1
            
            # Support and Resistance levels
            indicators['support_level'] = data['Low'].rolling(window=20).min().iloc[-1]
            indicators['resistance_level'] = data['High'].rolling(window=20).max().iloc[-1]
            
            return indicators
            
        except Exception as e:
            logger.error(f"Error calculating technical indicators: {e}")
            return {}
    
    def analyze_trend(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze price trend"""
        if data.empty:
            return {}
        
        try:
            current_price = data['Close'].iloc[-1]
            sma_20 = data['Close'].rolling(window=20).mean().iloc[-1]
            sma_50 = data['Close'].rolling(window=50).mean().iloc[-1]
            sma_200 = data['Close'].rolling(window=200).mean().iloc[-1]
            
            # Trend analysis
            trend_analysis = {
                'current_price': current_price,
                'sma_20': sma_20,
                'sma_50': sma_50,
                'sma_200': sma_200,
                'above_sma_20': current_price > sma_20,
                'above_sma_50': current_price > sma_50,
                'above_sma_200': current_price > sma_200,
                'trend_strength': 0,
                'trend_direction': 'neutral'
            }
            
            # Calculate trend strength
            trend_strength = 0
            if current_price > sma_20:
                trend_strength += 1
            if current_price > sma_50:
                trend_strength += 1
            if current_price > sma_200:
                trend_strength += 1
            if sma_20 > sma_50:
                trend_strength += 1
            if sma_50 > sma_200:
                trend_strength += 1
            
            trend_analysis['trend_strength'] = trend_strength
            
            # Determine trend direction
            if trend_strength >= 4:
                trend_analysis['trend_direction'] = 'strong_uptrend'
            elif trend_strength >= 2:
                trend_analysis['trend_direction'] = 'uptrend'
            elif trend_strength <= 1:
                trend_analysis['trend_direction'] = 'downtrend'
            else:
                trend_analysis['trend_direction'] = 'sideways'
            
            return trend_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing trend: {e}")
            return {}
    
    def calculate_risk_metrics(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate comprehensive risk metrics"""
        if data.empty:
            return {}
        
        try:
            # Use helper function
            basic_risk = calculate_risk_metrics(data)
            
            # Additional risk metrics
            current_price = data['Close'].iloc[-1]
            
            # Value at Risk (VaR)
            returns = data['Close'].pct_change().dropna()
            var_95 = np.percentile(returns, 5)
            var_99 = np.percentile(returns, 1)
            
            # Maximum drawdown
            cumulative_returns = (1 + returns).cumprod()
            rolling_max = cumulative_returns.expanding().max()
            drawdown = (cumulative_returns - rolling_max) / rolling_max
            max_drawdown = drawdown.min()
            
            # Volatility
            daily_volatility = returns.std()
            annualized_volatility = daily_volatility * np.sqrt(252)
            
            # Beta calculation (simplified - using market proxy)
            # In a real implementation, you'd compare against a market index
            beta = 1.0  # Placeholder
            
            risk_metrics = {
                **basic_risk,
                'var_95': var_95,
                'var_99': var_99,
                'max_drawdown': max_drawdown,
                'daily_volatility': daily_volatility,
                'annualized_volatility': annualized_volatility,
                'beta': beta,
                'current_price': current_price
            }
            
            return risk_metrics
            
        except Exception as e:
            logger.error(f"Error calculating risk metrics: {e}")
            return {}
    
    def analyze_fundamentals(self, stock_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze fundamental metrics"""
        if not stock_info:
            return {}
        
        try:
            analysis = {
                'valuation_metrics': {},
                'financial_health': {},
                'growth_metrics': {},
                'overall_score': 0
            }
            
            # Valuation analysis
            pe_ratio = stock_info.get('pe_ratio', 0)
            pb_ratio = stock_info.get('price_to_book', 0)
            dividend_yield = stock_info.get('dividend_yield', 0)
            
            analysis['valuation_metrics'] = {
                'pe_ratio': pe_ratio,
                'pb_ratio': pb_ratio,
                'dividend_yield': dividend_yield,
                'pe_assessment': 'expensive' if pe_ratio > 25 else 'reasonable' if pe_ratio > 15 else 'cheap',
                'pb_assessment': 'expensive' if pb_ratio > 3 else 'reasonable' if pb_ratio > 1 else 'cheap'
            }
            
            # Financial health analysis
            debt_to_equity = stock_info.get('debt_to_equity', 0)
            current_ratio = stock_info.get('current_ratio', 0)
            roe = stock_info.get('return_on_equity', 0)
            roa = stock_info.get('return_on_assets', 0)
            
            analysis['financial_health'] = {
                'debt_to_equity': debt_to_equity,
                'current_ratio': current_ratio,
                'roe': roe,
                'roa': roa,
                'debt_assessment': 'high' if debt_to_equity > 1 else 'moderate' if debt_to_equity > 0.5 else 'low',
                'liquidity_assessment': 'good' if current_ratio > 1.5 else 'adequate' if current_ratio > 1 else 'poor',
                'profitability_assessment': 'excellent' if roe > 20 else 'good' if roe > 15 else 'poor'
            }
            
            # Growth analysis
            revenue_growth = stock_info.get('revenue_growth', 0)
            earnings_growth = stock_info.get('earnings_growth', 0)
            
            analysis['growth_metrics'] = {
                'revenue_growth': revenue_growth,
                'earnings_growth': earnings_growth,
                'growth_assessment': 'strong' if revenue_growth > 0.15 else 'moderate' if revenue_growth > 0.05 else 'weak'
            }
            
            # Calculate overall fundamental score
            score = 0
            
            # Valuation score (30%)
            if pe_ratio > 0 and pe_ratio < 20:
                score += 30
            elif pe_ratio >= 20 and pe_ratio < 30:
                score += 15
            
            # Financial health score (40%)
            if debt_to_equity < 0.5:
                score += 20
            elif debt_to_equity < 1:
                score += 10
            
            if current_ratio > 1.5:
                score += 20
            elif current_ratio > 1:
                score += 10
            
            # Growth score (30%)
            if revenue_growth > 0.1:
                score += 30
            elif revenue_growth > 0.05:
                score += 15
            
            analysis['overall_score'] = score
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing fundamentals: {e}")
            return {}
    
    def generate_trading_signals(self, 
                               technical_indicators: Dict[str, Any],
                               trend_analysis: Dict[str, Any],
                               risk_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Generate trading signals based on analysis"""
        try:
            signals = {
                'buy_signals': [],
                'sell_signals': [],
                'hold_signals': [],
                'overall_signal': 'hold',
                'confidence': 0.5,
                'reasoning': []
            }
            
            current_price = trend_analysis.get('current_price', 0)
            
            # Technical signals
            if technical_indicators:
                # RSI signals
                rsi = technical_indicators.get('rsi', 50)
                if rsi < 30:
                    signals['buy_signals'].append(f"RSI oversold ({rsi:.1f})")
                elif rsi > 70:
                    signals['sell_signals'].append(f"RSI overbought ({rsi:.1f})")
                
                # MACD signals
                macd = technical_indicators.get('macd', 0)
                macd_signal = technical_indicators.get('macd_signal', 0)
                if macd > macd_signal and macd > 0:
                    signals['buy_signals'].append("MACD bullish crossover")
                elif macd < macd_signal and macd < 0:
                    signals['sell_signals'].append("MACD bearish crossover")
                
                # Bollinger Bands signals
                bb_position = technical_indicators.get('bb_position', 0.5)
                if bb_position < 0.2:
                    signals['buy_signals'].append("Price near lower Bollinger Band")
                elif bb_position > 0.8:
                    signals['sell_signals'].append("Price near upper Bollinger Band")
            
            # Trend signals
            if trend_analysis:
                trend_direction = trend_analysis.get('trend_direction', 'neutral')
                if trend_direction in ['strong_uptrend', 'uptrend']:
                    signals['buy_signals'].append(f"Strong {trend_direction}")
                elif trend_direction == 'downtrend':
                    signals['sell_signals'].append("Downtrend detected")
            
            # Risk-based signals
            if risk_metrics:
                volatility = risk_metrics.get('annualized_volatility', 0)
                if volatility > 0.4:
                    signals['hold_signals'].append("High volatility - exercise caution")
                
                max_drawdown = risk_metrics.get('max_drawdown', 0)
                if abs(max_drawdown) > 0.3:
                    signals['hold_signals'].append("Significant drawdown history")
            
            # Determine overall signal
            buy_count = len(signals['buy_signals'])
            sell_count = len(signals['sell_signals'])
            hold_count = len(signals['hold_signals'])
            
            if buy_count > sell_count and buy_count > 0:
                signals['overall_signal'] = 'buy'
                signals['confidence'] = min(0.9, 0.5 + (buy_count * 0.1))
            elif sell_count > buy_count and sell_count > 0:
                signals['overall_signal'] = 'sell'
                signals['confidence'] = min(0.9, 0.5 + (sell_count * 0.1))
            else:
                signals['overall_signal'] = 'hold'
                signals['confidence'] = 0.5
            
            # Generate reasoning
            if signals['buy_signals']:
                signals['reasoning'].append(f"Buy signals: {', '.join(signals['buy_signals'])}")
            if signals['sell_signals']:
                signals['reasoning'].append(f"Sell signals: {', '.join(signals['sell_signals'])}")
            if signals['hold_signals']:
                signals['reasoning'].append(f"Caution: {', '.join(signals['hold_signals'])}")
            
            return signals
            
        except Exception as e:
            logger.error(f"Error generating trading signals: {e}")
            return {
                'buy_signals': [],
                'sell_signals': [],
                'hold_signals': [],
                'overall_signal': 'hold',
                'confidence': 0.5,
                'reasoning': ['Error in signal generation']
            }
    
    def comprehensive_analysis(self, ticker: str) -> Dict[str, Any]:
        """Perform comprehensive analysis of a stock"""
        try:
            logger.info(f"Starting comprehensive analysis for {ticker}")
            
            # Get data
            data = self.get_stock_data(ticker)
            if data is None:
                return {'error': f'Unable to fetch data for {ticker}'}
            
            stock_info = self.get_stock_info(ticker)
            
            # Perform analysis
            technical_indicators = self.calculate_technical_indicators(data)
            trend_analysis = self.analyze_trend(data)
            risk_metrics = self.calculate_risk_metrics(data)
            fundamental_analysis = self.analyze_fundamentals(stock_info)
            trading_signals = self.generate_trading_signals(
                technical_indicators, trend_analysis, risk_metrics
            )
            
            # Compile results
            analysis_result = {
                'ticker': ticker,
                'timestamp': datetime.now().isoformat(),
                'stock_info': stock_info,
                'technical_indicators': technical_indicators,
                'trend_analysis': trend_analysis,
                'risk_metrics': risk_metrics,
                'fundamental_analysis': fundamental_analysis,
                'trading_signals': trading_signals,
                'summary': {
                    'current_price': trend_analysis.get('current_price', 0),
                    'trend_direction': trend_analysis.get('trend_direction', 'neutral'),
                    'overall_signal': trading_signals.get('overall_signal', 'hold'),
                    'confidence': trading_signals.get('confidence', 0.5),
                    'risk_level': 'high' if risk_metrics.get('annualized_volatility', 0) > 0.4 else 'medium' if risk_metrics.get('annualized_volatility', 0) > 0.2 else 'low'
                }
            }
            
            logger.info(f"Analysis completed for {ticker}")
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error in comprehensive analysis for {ticker}: {e}")
            return {'error': f'Analysis failed for {ticker}: {str(e)}'} 