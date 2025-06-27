import pytest
from agent.analysis import FinancialAnalyzer
from agent.memory import MemoryManager
import pandas as pd
import numpy as np

@pytest.fixture
def analyzer():
    return FinancialAnalyzer()

@pytest.fixture
def dummy_stock_data():
    # Simulate 1 year of daily data
    dates = pd.date_range(end=pd.Timestamp.today(), periods=252)
    close = np.linspace(2000, 2500, 252) + np.random.normal(0, 20, 252)
    high = close + np.random.uniform(5, 20, 252)
    low = close - np.random.uniform(5, 20, 252)
    volume = np.random.randint(100000, 500000, 252)
    return pd.DataFrame({'Close': close, 'High': high, 'Low': low, 'Volume': volume}, index=dates)

def test_technical_indicators(analyzer, dummy_stock_data):
    indicators = analyzer.calculate_technical_indicators(dummy_stock_data)
    assert 'sma_20' in indicators
    assert 'rsi' in indicators
    assert 0 <= indicators['rsi'] <= 100

def test_trend_analysis(analyzer, dummy_stock_data):
    trend = analyzer.analyze_trend(dummy_stock_data)
    assert 'trend_direction' in trend
    assert trend['trend_direction'] in ['strong_uptrend', 'uptrend', 'downtrend', 'sideways', 'neutral']

def test_risk_metrics(analyzer, dummy_stock_data):
    risk = analyzer.calculate_risk_metrics(dummy_stock_data)
    assert 'volatility' in risk
    assert 'max_drawdown' in risk
    assert risk['volatility'] >= 0

def test_fundamental_analysis(analyzer):
    # Use a real stock for fundamental analysis
    info = analyzer.get_stock_info('RELIANCE')
    if info:
        result = analyzer.analyze_fundamentals(info)
        assert 'valuation_metrics' in result
        assert 'financial_health' in result
        assert 'growth_metrics' in result

def test_comprehensive_analysis(analyzer):
    # Test with a real stock
    result = analyzer.comprehensive_analysis('TCS')
    assert 'ticker' in result
    assert 'technical_indicators' in result
    assert 'trading_signals' in result
    assert 'summary' in result

def test_memory_manager():
    mem = MemoryManager(db_path='data/memory/test_agent_memory.db')
    mem.store_interaction('testsession', 'What is the best stock?', 'RELIANCE', 'query', {'test': True})
    mem.store_recommendation('RELIANCE', 'buy', 0.9, 3000, 2800, 'Strong uptrend', {'trend': 'up'}, [{'title': 'Reliance surges'}])
    recs = mem.get_recent_recommendations('RELIANCE', days=1)
    assert recs
    mem.cleanup_old_data(days=0)  # Clean up test data 