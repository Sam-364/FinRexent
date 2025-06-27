"""
Memory Management System for FinRexent Agent
"""
import sqlite3
import json
import pickle
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import hashlib

from utils.logger import logger
from utils.config import config

class MemoryManager:
    """Memory management system for storing and retrieving agent data"""
    
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            db_path = config.get_database_config().get('url', 'sqlite:///data/memory/agent_memory.db')
            # Convert SQLAlchemy URL to file path
            if db_path.startswith('sqlite:///'):
                db_path = db_path.replace('sqlite:///', '')
        
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Initialize the memory database with required tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # User interactions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    user_query TEXT,
                    agent_response TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    interaction_type TEXT,
                    metadata TEXT
                )
            ''')
            
            # Investment recommendations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS investment_recommendations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticker TEXT,
                    recommendation TEXT,
                    confidence REAL,
                    target_price REAL,
                    stop_loss REAL,
                    reasoning TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    market_conditions TEXT,
                    news_context TEXT,
                    user_feedback TEXT
                )
            ''')
            
            # Market analysis table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS market_analysis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    analysis_type TEXT,
                    data TEXT,
                    insights TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    validity_period INTEGER
                )
            ''')
            
            # Portfolio tracking table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS portfolio_tracking (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticker TEXT,
                    entry_price REAL,
                    entry_date TIMESTAMP,
                    current_price REAL,
                    quantity INTEGER,
                    total_investment REAL,
                    current_value REAL,
                    pnl REAL,
                    pnl_percentage REAL,
                    recommendation_id INTEGER,
                    status TEXT,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (recommendation_id) REFERENCES investment_recommendations (id)
                )
            ''')
            
            # Learning data table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS learning_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data_type TEXT,
                    data_hash TEXT UNIQUE,
                    data_content TEXT,
                    importance_score REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    access_count INTEGER DEFAULT 0
                )
            ''')
            
            # Performance metrics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_type TEXT,
                    metric_value REAL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    context TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Memory database initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing memory database: {e}")
    
    def store_interaction(self, 
                         session_id: str,
                         user_query: str,
                         agent_response: str,
                         interaction_type: str = "general",
                         metadata: Optional[Dict[str, Any]] = None):
        """Store a user interaction"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO user_interactions 
                (session_id, user_query, agent_response, interaction_type, metadata)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                session_id,
                user_query,
                agent_response,
                interaction_type,
                json.dumps(metadata) if metadata else None
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error storing interaction: {e}")
    
    def store_recommendation(self,
                           ticker: str,
                           recommendation: str,
                           confidence: float,
                           target_price: float,
                           stop_loss: float,
                           reasoning: str,
                           market_conditions: Optional[Dict[str, Any]] = None,
                           news_context: Optional[List[Dict[str, Any]]] = None):
        """Store an investment recommendation"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO investment_recommendations 
                (ticker, recommendation, confidence, target_price, stop_loss, reasoning, 
                 market_conditions, news_context)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                ticker,
                recommendation,
                confidence,
                target_price,
                stop_loss,
                reasoning,
                json.dumps(market_conditions) if market_conditions else None,
                json.dumps(news_context) if news_context else None
            ))
            
            recommendation_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            logger.info(f"Stored recommendation for {ticker} with ID {recommendation_id}")
            return recommendation_id
            
        except Exception as e:
            logger.error(f"Error storing recommendation: {e}")
            return None
    
    def get_recent_recommendations(self, 
                                 ticker: Optional[str] = None,
                                 days: int = 30) -> List[Dict[str, Any]]:
        """Get recent investment recommendations"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cutoff_date = datetime.now() - timedelta(days=days)
            
            if ticker:
                cursor.execute('''
                    SELECT * FROM investment_recommendations 
                    WHERE ticker = ? AND timestamp > ?
                    ORDER BY timestamp DESC
                ''', (ticker, cutoff_date.isoformat()))
            else:
                cursor.execute('''
                    SELECT * FROM investment_recommendations 
                    WHERE timestamp > ?
                    ORDER BY timestamp DESC
                ''', (cutoff_date.isoformat(),))
            
            rows = cursor.fetchall()
            conn.close()
            
            recommendations = []
            for row in rows:
                recommendations.append({
                    'id': row[0],
                    'ticker': row[1],
                    'recommendation': row[2],
                    'confidence': row[3],
                    'target_price': row[4],
                    'stop_loss': row[5],
                    'reasoning': row[6],
                    'timestamp': row[7],
                    'market_conditions': json.loads(row[8]) if row[8] else None,
                    'news_context': json.loads(row[9]) if row[9] else None,
                    'user_feedback': row[10]
                })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error retrieving recommendations: {e}")
            return []
    
    def store_market_analysis(self,
                            analysis_type: str,
                            data: Dict[str, Any],
                            insights: str,
                            validity_period: int = 24):  # hours
        """Store market analysis data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO market_analysis 
                (analysis_type, data, insights, validity_period)
                VALUES (?, ?, ?, ?)
            ''', (
                analysis_type,
                json.dumps(data),
                insights,
                validity_period
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error storing market analysis: {e}")
    
    def get_valid_market_analysis(self, analysis_type: str) -> List[Dict[str, Any]]:
        """Get valid market analysis data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM market_analysis 
                WHERE analysis_type = ? AND 
                      timestamp > datetime('now', '-' || validity_period || ' hours')
                ORDER BY timestamp DESC
            ''', (analysis_type,))
            
            rows = cursor.fetchall()
            conn.close()
            
            analyses = []
            for row in rows:
                analyses.append({
                    'id': row[0],
                    'analysis_type': row[1],
                    'data': json.loads(row[2]),
                    'insights': row[3],
                    'timestamp': row[4],
                    'validity_period': row[5]
                })
            
            return analyses
            
        except Exception as e:
            logger.error(f"Error retrieving market analysis: {e}")
            return []
    
    def track_portfolio_position(self,
                               ticker: str,
                               entry_price: float,
                               quantity: int,
                               recommendation_id: Optional[int] = None):
        """Track a portfolio position"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            total_investment = entry_price * quantity
            
            cursor.execute('''
                INSERT INTO portfolio_tracking 
                (ticker, entry_price, entry_date, quantity, total_investment, 
                 current_price, current_value, pnl, pnl_percentage, recommendation_id, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                ticker,
                entry_price,
                datetime.now().isoformat(),
                quantity,
                total_investment,
                entry_price,  # Initially same as entry price
                total_investment,  # Initially same as total investment
                0.0,  # Initial PnL
                0.0,  # Initial PnL percentage
                recommendation_id,
                'active'
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error tracking portfolio position: {e}")
    
    def update_portfolio_position(self,
                                ticker: str,
                                current_price: float):
        """Update portfolio position with current price"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get current position
            cursor.execute('''
                SELECT entry_price, quantity, total_investment 
                FROM portfolio_tracking 
                WHERE ticker = ? AND status = 'active'
                ORDER BY entry_date DESC LIMIT 1
            ''', (ticker,))
            
            row = cursor.fetchone()
            if row:
                entry_price, quantity, total_investment = row
                current_value = current_price * quantity
                pnl = current_value - total_investment
                pnl_percentage = (pnl / total_investment) * 100 if total_investment > 0 else 0
                
                cursor.execute('''
                    UPDATE portfolio_tracking 
                    SET current_price = ?, current_value = ?, pnl = ?, 
                        pnl_percentage = ?, last_updated = ?
                    WHERE ticker = ? AND status = 'active'
                ''', (
                    current_price,
                    current_value,
                    pnl,
                    pnl_percentage,
                    datetime.now().isoformat(),
                    ticker
                ))
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error updating portfolio position: {e}")
        finally:
            conn.close()
    
    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Get portfolio summary"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_positions,
                    SUM(total_investment) as total_invested,
                    SUM(current_value) as total_current_value,
                    SUM(pnl) as total_pnl,
                    AVG(pnl_percentage) as avg_pnl_percentage
                FROM portfolio_tracking 
                WHERE status = 'active'
            ''')
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {
                    'total_positions': row[0],
                    'total_invested': row[1] or 0,
                    'total_current_value': row[2] or 0,
                    'total_pnl': row[3] or 0,
                    'avg_pnl_percentage': row[4] or 0
                }
            
            return {}
            
        except Exception as e:
            logger.error(f"Error getting portfolio summary: {e}")
            return {}
    
    def store_learning_data(self,
                           data_type: str,
                           data_content: Any,
                           importance_score: float = 1.0):
        """Store learning data with deduplication"""
        try:
            # Create hash of data content for deduplication
            data_str = json.dumps(data_content, sort_keys=True)
            data_hash = hashlib.md5(data_str.encode()).hexdigest()
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if data already exists
            cursor.execute('''
                SELECT id, access_count FROM learning_data 
                WHERE data_hash = ?
            ''', (data_hash,))
            
            existing = cursor.fetchone()
            
            if existing:
                # Update access count and last accessed time
                cursor.execute('''
                    UPDATE learning_data 
                    SET access_count = access_count + 1, last_accessed = ?
                    WHERE id = ?
                ''', (datetime.now().isoformat(), existing[0]))
            else:
                # Insert new data
                cursor.execute('''
                    INSERT INTO learning_data 
                    (data_type, data_hash, data_content, importance_score)
                    VALUES (?, ?, ?, ?)
                ''', (data_type, data_hash, data_str, importance_score))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error storing learning data: {e}")
    
    def get_learning_data(self,
                         data_type: str,
                         limit: int = 10) -> List[Dict[str, Any]]:
        """Get learning data by type"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT data_content, importance_score, access_count, created_at
                FROM learning_data 
                WHERE data_type = ?
                ORDER BY importance_score DESC, access_count DESC
                LIMIT ?
            ''', (data_type, limit))
            
            rows = cursor.fetchall()
            conn.close()
            
            data = []
            for row in rows:
                data.append({
                    'content': json.loads(row[0]),
                    'importance_score': row[1],
                    'access_count': row[2],
                    'created_at': row[3]
                })
            
            return data
            
        except Exception as e:
            logger.error(f"Error retrieving learning data: {e}")
            return []
    
    def store_performance_metric(self,
                               metric_type: str,
                               metric_value: float,
                               context: Optional[Dict[str, Any]] = None):
        """Store performance metric"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO performance_metrics 
                (metric_type, metric_value, context)
                VALUES (?, ?, ?)
            ''', (
                metric_type,
                metric_value,
                json.dumps(context) if context else None
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error storing performance metric: {e}")
    
    def get_performance_metrics(self,
                              metric_type: str,
                              days: int = 30) -> List[Dict[str, Any]]:
        """Get performance metrics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cutoff_date = datetime.now() - timedelta(days=days)
            
            cursor.execute('''
                SELECT metric_value, timestamp, context
                FROM performance_metrics 
                WHERE metric_type = ? AND timestamp > ?
                ORDER BY timestamp DESC
            ''', (metric_type, cutoff_date.isoformat()))
            
            rows = cursor.fetchall()
            conn.close()
            
            metrics = []
            for row in rows:
                metrics.append({
                    'value': row[0],
                    'timestamp': row[1],
                    'context': json.loads(row[2]) if row[2] else None
                })
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error retrieving performance metrics: {e}")
            return []
    
    def cleanup_old_data(self, days: int = 90):
        """Clean up old data to prevent database bloat"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Clean up old interactions
            cursor.execute('''
                DELETE FROM user_interactions 
                WHERE timestamp < ?
            ''', (cutoff_date.isoformat(),))
            
            # Clean up old market analysis
            cursor.execute('''
                DELETE FROM market_analysis 
                WHERE timestamp < ?
            ''', (cutoff_date.isoformat(),))
            
            # Clean up old performance metrics
            cursor.execute('''
                DELETE FROM performance_metrics 
                WHERE timestamp < ?
            ''', (cutoff_date.isoformat(),))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Cleaned up data older than {days} days")
            
        except Exception as e:
            logger.error(f"Error cleaning up old data: {e}")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory usage statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            stats = {}
            
            # Count records in each table
            tables = ['user_interactions', 'investment_recommendations', 
                     'market_analysis', 'portfolio_tracking', 
                     'learning_data', 'performance_metrics']
            
            for table in tables:
                cursor.execute(f'SELECT COUNT(*) FROM {table}')
                stats[f'{table}_count'] = cursor.fetchone()[0]
            
            # Get database size
            cursor.execute('PRAGMA page_count')
            page_count = cursor.fetchone()[0]
            cursor.execute('PRAGMA page_size')
            page_size = cursor.fetchone()[0]
            stats['database_size_mb'] = (page_count * page_size) / (1024 * 1024)
            
            conn.close()
            return stats
            
        except Exception as e:
            logger.error(f"Error getting memory stats: {e}")
            return {} 