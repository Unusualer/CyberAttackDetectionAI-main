from typing import List, Dict, Any, Optional
from datetime import datetime
import pandas as pd
from .threat_analysis import ThreatAnalysisService
from .ml.training_pipeline import ModelTrainingPipeline
from ..schemas.reports import Report, ReportType
from ..core.config import settings
import logging
from sqlalchemy.future import select

logger = logging.getLogger(__name__)

class ReportingService:
    def __init__(self):
        self.threat_analyzer = ThreatAnalysisService()
        self.model_pipeline = ModelTrainingPipeline()
        
    async def generate_report(
        self,
        organization_id: str,
        report_type: ReportType,
        start_date: datetime,
        end_date: datetime
    ) -> Report:
        """Generate a new security report"""
        try:
            # Get data for report
            data = await self._get_report_data(
                organization_id,
                report_type,
                start_date,
                end_date
            )
            
            # Generate insights
            insights = self._generate_insights(data)
            
            # Create visualizations
            visualizations = self._create_visualizations(data)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(insights)
            
            report = Report(
                organization_id=organization_id,
                report_type=report_type,
                start_date=start_date,
                end_date=end_date,
                data=data,
                insights=insights,
                visualizations=visualizations,
                recommendations=recommendations,
                generated_at=datetime.utcnow()
            )
            
            # Save report
            await self._save_report(report)
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            raise 

    async def _get_report_data(
        self,
        organization_id: str,
        report_type: ReportType,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Get data for report"""
        if report_type == ReportType.THREAT_SUMMARY:
            return await self.threat_analyzer.get_threat_summary(
                organization_id, start_date, end_date
            )
        elif report_type == ReportType.ML_PERFORMANCE:
            return await self.model_pipeline.get_performance_metrics(
                start_date, end_date
            )
        # Add other report types...

    def _generate_insights(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate insights from report data"""
        insights = []
        df = pd.DataFrame(data["events"])
        
        # Trend analysis
        if not df.empty:
            trends = df.groupby('type').size().to_dict()
            insights.append({
                "type": "trend",
                "title": "Threat Trends",
                "data": trends
            })
            
        # Add more insights...
        return insights

    def _create_visualizations(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create visualizations for report"""
        return [
            {
                "type": "line_chart",
                "title": "Threats Over Time",
                "data": self._prepare_time_series_data(data)
            },
            {
                "type": "pie_chart",
                "title": "Threat Distribution",
                "data": self._prepare_distribution_data(data)
            }
        ]
        
    def _prepare_time_series_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare time series data for visualization"""
        df = pd.DataFrame(data["events"])
        if df.empty:
            return {"timestamps": [], "values": []}
            
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.set_index('timestamp')
        
        # Resample to hourly counts
        hourly_counts = df.resample('H').size()
        
        return {
            "timestamps": hourly_counts.index.strftime('%Y-%m-%d %H:%M:%S').tolist(),
            "values": hourly_counts.values.tolist()
        }
        
    def _prepare_distribution_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare distribution data for visualization"""
        df = pd.DataFrame(data["events"])
        if df.empty:
            return {"labels": [], "values": []}
            
        distribution = df['type'].value_counts()
        
        return {
            "labels": distribution.index.tolist(),
            "values": distribution.values.tolist()
        }
        
    def _generate_recommendations(self, insights: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate recommendations based on insights"""
        recommendations = []
        
        for insight in insights:
            if insight["type"] == "trend":
                recommendations.extend(
                    self._get_trend_recommendations(insight["data"])
                )
            elif insight["type"] == "anomaly":
                recommendations.extend(
                    self._get_anomaly_recommendations(insight["data"])
                )
                
        return recommendations
        
    def _get_trend_recommendations(self, trend_data: Dict[str, int]) -> List[Dict[str, Any]]:
        """Generate recommendations based on threat trends"""
        recommendations = []
        
        # Check for high-frequency threats
        for threat_type, count in trend_data.items():
            if count > settings.HIGH_FREQUENCY_THRESHOLD:
                recommendations.append({
                    "priority": "high",
                    "category": "threat_prevention",
                    "title": f"High frequency of {threat_type} threats detected",
                    "description": f"Consider implementing additional controls for {threat_type}",
                    "actions": [
                        f"Review {threat_type} detection rules",
                        "Update security policies",
                        "Deploy additional monitoring"
                    ]
                })
                
        return recommendations
        
    async def _save_report(self, report: Report):
        """Save report to database"""
        try:
            async with self.db.session() as session:
                session.add(report)
                await session.commit()
                
            # Cache report for faster retrieval
            await self._cache_report(report)
            
        except Exception as e:
            logger.error(f"Error saving report: {str(e)}")
            raise
            
    async def _cache_report(self, report: Report):
        """Cache report in Redis"""
        try:
            cache_key = f"report:{report.id}"
            await self.redis.setex(
                cache_key,
                settings.REPORT_CACHE_TTL,
                report.json()
            )
        except Exception as e:
            logger.warning(f"Error caching report: {str(e)}")
            
    async def get_reports(
        self,
        organization_id: str,
        report_type: Optional[ReportType] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 50
    ) -> List[Report]:
        """Get list of reports"""
        try:
            query = select(Report).where(
                Report.organization_id == organization_id
            )
            
            if report_type:
                query = query.where(Report.report_type == report_type)
            if start_date:
                query = query.where(Report.generated_at >= start_date)
            if end_date:
                query = query.where(Report.generated_at <= end_date)
                
            query = query.order_by(Report.generated_at.desc()).limit(limit)
            
            async with self.db.session() as session:
                result = await session.execute(query)
                return result.scalars().all()
                
        except Exception as e:
            logger.error(f"Error getting reports: {str(e)}")
            raise
            
    async def get_report(self, report_id: str, organization_id: str) -> Optional[Report]:
        """Get specific report"""
        try:
            # Try to get from cache first
            cached_report = await self._get_cached_report(report_id)
            if cached_report:
                return cached_report
                
            # Get from database
            async with self.db.session() as session:
                query = select(Report).where(
                    Report.id == report_id,
                    Report.organization_id == organization_id
                )
                result = await session.execute(query)
                return result.scalar_one_or_none()
                
        except Exception as e:
            logger.error(f"Error getting report: {str(e)}")
            raise

    async def _get_cached_report(self, report_id: str) -> Optional[Report]:
        """Get report from cache"""
        try:
            cache_key = f"report:{report_id}"
            cached_data = await self.redis.get(cache_key)
            if cached_data:
                return Report.parse_raw(cached_data)
            return None
        except Exception as e:
            logger.warning(f"Error getting cached report: {str(e)}")
            return None

    def _get_anomaly_recommendations(self, anomaly_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate recommendations for anomalies"""
        recommendations = []
        
        if anomaly_data.get("severity") == "high":
            recommendations.append({
                "priority": "critical",
                "category": "anomaly_investigation",
                "title": "Critical anomaly detected",
                "description": "Immediate investigation required for high-severity anomaly",
                "actions": [
                    "Isolate affected systems",
                    "Collect forensic data",
                    "Initiate incident response"
                ]
            })
            
        return recommendations

    async def _analyze_trends(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze security trends"""
        df = pd.DataFrame(data["events"])
        analysis = {
            "total_events": len(df),
            "severity_distribution": df["severity"].value_counts().to_dict(),
            "top_threats": df["threat_type"].value_counts().head(5).to_dict(),
            "time_based_analysis": self._get_time_based_analysis(df)
        }
        
        if not df.empty:
            analysis["peak_hours"] = self._identify_peak_hours(df)
            analysis["threat_patterns"] = self._identify_threat_patterns(df)
            
        return analysis

    def _identify_peak_hours(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Identify peak hours for security events"""
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        hourly_counts = df.groupby('hour').size()
        peak_hours = hourly_counts[hourly_counts > hourly_counts.mean() + hourly_counts.std()]
        
        return [
            {
                "hour": hour,
                "event_count": count,
                "percentage_above_average": float(
                    ((count - hourly_counts.mean()) / hourly_counts.mean()) * 100
                )
            }
            for hour, count in peak_hours.items()
        ]

    def _identify_threat_patterns(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Identify patterns in threat data"""
        patterns = []
        
        # Time-based patterns
        time_patterns = self._analyze_time_patterns(df)
        if time_patterns:
            patterns.extend(time_patterns)
            
        # Source-based patterns
        source_patterns = self._analyze_source_patterns(df)
        if source_patterns:
            patterns.extend(source_patterns)
            
        return patterns

    def _analyze_time_patterns(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Analyze time-based patterns in threat data"""
        patterns = []
        
        # Daily patterns
        daily_counts = df.groupby(pd.Grouper(key='timestamp', freq='D')).size()
        significant_days = daily_counts[daily_counts > daily_counts.mean() + daily_counts.std()]
        
        if not significant_days.empty:
            patterns.append({
                "type": "daily_pattern",
                "description": "Significant increase in threats detected",
                "dates": significant_days.index.strftime('%Y-%m-%d').tolist(),
                "counts": significant_days.values.tolist()
            })
            
        return patterns

    def _analyze_source_patterns(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Analyze source-based patterns in threat data"""
        patterns = []
        
        # Source IP patterns
        source_counts = df['source_ip'].value_counts()
        frequent_sources = source_counts[source_counts > source_counts.mean() + source_counts.std()]
        
        if not frequent_sources.empty:
            patterns.append({
                "type": "source_pattern",
                "description": "Frequent threat sources identified",
                "sources": frequent_sources.index.tolist(),
                "counts": frequent_sources.values.tolist()
            })
            
        return patterns

    def _get_time_based_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get time-based analysis of threats"""
        return {
            "hourly_distribution": df.groupby(df['timestamp'].dt.hour).size().to_dict(),
            "daily_distribution": df.groupby(df['timestamp'].dt.day_name()).size().to_dict(),
            "monthly_trend": df.groupby(pd.Grouper(key='timestamp', freq='M')).size().to_dict()
        }