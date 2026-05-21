class AnalyticsService:
    async def summary(self) -> dict:
        # TODO: compute real metrics
        return {
            "totalSkills": 0,
            "completedSteps": 0,
            "totalSteps": 0,
            "trend": [],
        }


analytics_service = AnalyticsService()
