import asyncio
import aiohttp
import time
from typing import List, Dict
import statistics
import json

async def run_performance_test(
    endpoint: str,
    num_requests: int,
    concurrent_requests: int
) -> Dict[str, float]:
    """Run performance test on endpoint"""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(num_requests):
            tasks.append(
                measure_request_time(session, endpoint)
            )
            
        response_times = await asyncio.gather(*tasks)
        
        return {
            "avg_response_time": statistics.mean(response_times),
            "p95_response_time": statistics.quantiles(response_times, n=20)[18],
            "max_response_time": max(response_times),
            "min_response_time": min(response_times),
            "total_requests": len(response_times)
        }

async def measure_request_time(session: aiohttp.ClientSession, url: str) -> float:
    start_time = time.time()
    async with session.get(url) as response:
        await response.text()
        return time.time() - start_time 