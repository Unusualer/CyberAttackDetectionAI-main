from typing import Dict, Any, List
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from ..schemas.schemas import AnalyticsReport, ThreatMetrics, SystemMetrics
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)

class AnalyticsService:
    def __init__(self):
        self.report_cache = {}
        
    async def generate_threat_report(
        self,
        organization_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> AnalyticsReport:
        """Generate comprehensive threat analysis report"""
        try:
            # Get threat data
            threats = await self._get_threat_data(
                organization_id,
                start_date,
                end_date
            )
            
            # Calculate metrics
            metrics = self._calculate_threat_metrics(threats)
            
            # Generate insights
            insights = self._generate_insights(threats, metrics)
            
            # Create recommendations
            recommendations = self._create_recommendations(insights)
            
            return AnalyticsReport(
                organization_id=organization_id,
                time_period={
                    "start": start_date,
                    "end": end_date
                },
                metrics=metrics,
                insights=insights,
                recommendations=recommendations,
                generated_at=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Error generating threat report: {str(e)}")
            raise
            
    def _calculate_threat_metrics(self, threats: List[Dict]) -> ThreatMetrics:
        """Calculate threat detection metrics"""
        df = pd.DataFrame(threats)
        
        return ThreatMetrics(
            total_threats=len(threats),
            severity_distribution=df['severity'].value_counts().to_dict(),
            threat_types=df['type'].value_counts().to_dict(),
            detection_source=df['detection_source'].value_counts().to_dict(),
            average_response_time=df['response_time'].mean(),
            resolution_rate=len(df[df['resolved']]) / len(df) if len(df) > 0 else 0
        )
        
    def _generate_insights(
        self,
        threats: List[Dict],
        metrics: ThreatMetrics
    ) -> List[Dict[str, Any]]:
        """Generate insights from threat data"""
        insights = []
        
        # Trend analysis
        trend = self._analyze_threat_trends(threats)
        if trend["significant_change"]:
            insights.append({
                "type": "trend",
                "severity": "high" if trend["increase"] else "medium",
                "description": f"Threat incidents have {trend['direction']} by {trend['change_percent']}%",
                "details": trend
            })
            
        # Pattern detection
        patterns = self._detect_attack_patterns(threats)
        for pattern in patterns:
            insights.append({
                "type": "pattern",
                "severity": "high",
                "description": f"Detected {pattern['type']} attack pattern",
                "details": pattern
            })
            
        # Resource targeting
        targeted = self._analyze_targeted_resources(threats)
        if targeted["high_risk_targets"]:
            insights.append({
                "type": "targeting",
                "severity": "critical",
                "description": "Critical resources under targeted attacks",
                "details": targeted
            })
            
        return insights
        
    def _create_recommendations(
        self,
        insights: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Create security recommendations based on insights"""
        recommendations = []
        
        for insight in insights:
            if insight["type"] == "trend" and insight["severity"] == "high":
                recommendations.append({
                    "priority": "high",
                    "category": "defense",
                    "action": "Strengthen security measures",
                    "details": {
                        "steps": [
                            "Update security rules",
                            "Increase monitoring frequency",
                            "Deploy additional controls"
                        ],
                        "resources": insight["details"]["affected_resources"]
                    }
                })
                
            elif insight["type"] == "pattern":
                recommendations.append({
                    "priority": "critical",
                    "category": "mitigation",
                    "action": f"Mitigate {insight['details']['type']} attack pattern",
                    "details": {
                        "mitigation_steps": self._get_mitigation_steps(
                            insight["details"]["type"]
                        ),
                        "affected_systems": insight["details"]["systems"]
                    }
                })
                
        return recommendations
        
    async def _get_threat_data(
        self,
        organization_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict]:
        """Get threat data from database"""
        query = """
            SELECT *
            FROM security_events
            WHERE organization_id = :org_id
            AND timestamp BETWEEN :start_date AND :end_date
        """
        
        async with self.db.acquire() as conn:
            result = await conn.fetch(
                query,
                org_id=organization_id,
                start_date=start_date,
                end_date=end_date
            )
            
        return [dict(row) for row in result]
        
    def _analyze_threat_trends(self, threats: List[Dict]) -> Dict[str, Any]:
        """Analyze trends in threat data"""
        df = pd.DataFrame(threats)
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        
        daily_counts = df.groupby('date').size()
        
        if len(daily_counts) < 2:
            return {
                "significant_change": False,
                "change_percent": 0,
                "direction": "unchanged"
            }
            
        avg_first_half = daily_counts[:len(daily_counts)//2].mean()
        avg_second_half = daily_counts[len(daily_counts)//2:].mean()
        
        change_percent = ((avg_second_half - avg_first_half) / avg_first_half) * 100
        
        return {
            "significant_change": abs(change_percent) > settings.TREND_THRESHOLD,
            "change_percent": abs(change_percent),
            "direction": "increased" if change_percent > 0 else "decreased",
            "daily_counts": daily_counts.to_dict()
        } 