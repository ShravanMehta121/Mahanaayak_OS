import json
from app.models.complaint import Complaint
from app.models.department import Department, Ward
from app.constants.complaint_status import ComplaintStatus

class MockAIService:
    @staticmethod
    def _get_dynamic_metrics():
        total = Complaint.query.count()
        open_c = Complaint.query.filter_by(status=ComplaintStatus.OPEN.value).count()
        return total, open_c

    @staticmethod
    def generate_executive_summary(prompt: str) -> dict:
        total, open_c = MockAIService._get_dynamic_metrics()
        return {
            "summary": "The administration has been performing moderately well.",
            "metrics": {
                "total_complaints_handled": total,
                "currently_open": open_c
            },
            "highlights": ["Water supply restored in Ward 3", "Road repair completed in Ward 1"]
        }

    @staticmethod
    def generate_complaint_summary(prompt: str) -> dict:
        return {
            "summary": "Citizen reported severe water logging issues.",
            "suggested_department": "Water Works",
            "suggested_severity": "HIGH",
            "suggested_resolution_steps": ["Dispatch inspection team", "Clear drainage", "Provide temporary water tanker"]
        }

    @staticmethod
    def generate_campaign_planner(prompt: str) -> dict:
        return {
            "meetings": ["Townhall at Ward 1", "Union discussion"],
            "road_shows": ["Main Street Rally"],
            "medical_camps": ["Free Eye Checkup at Community Center"],
            "public_visits": ["Visit Ward 3 slums"],
            "water_surveys": ["Survey Pipeline A"]
        }

    @staticmethod
    def generate_manifesto(prompt: str) -> dict:
        return {
            "roads": "Pledge to repair 100km of roads.",
            "water": "24/7 water supply in all wards.",
            "electricity": "Free electricity up to 200 units.",
            "education": "Build 5 new public schools.",
            "women_safety": "Install 1000 new CCTVs.",
            "healthcare": "Setup mohalla clinics in every ward."
        }

    @staticmethod
    def generate_speech(prompt: str) -> dict:
        return {
            "title": "A New Dawn for Mahanaayak",
            "content": "My dear citizens, today we stand on the precipice of change...",
            "tone": "Inspiring"
        }

    @staticmethod
    def generate_resource_allocation(prompt: str) -> dict:
        return {
            "engineers": 15,
            "cleaning_teams": 30,
            "water_tankers": 10,
            "budget": "50,00,000 INR"
        }

    @staticmethod
    def generate_ward_health(prompt: str) -> dict:
        # Dynamic grade
        total, open_c = MockAIService._get_dynamic_metrics()
        score = max(0, 100 - (open_c * 2))
        grade = "A" if score > 80 else "B" if score > 60 else "C" if score > 40 else "D"
        return {
            "score": score,
            "grade": grade,
            "explanation": f"The ward has {open_c} open issues resulting in a score of {score}."
        }

    @staticmethod
    def generate_constituency_health(prompt: str) -> dict:
        return {
            "sector_scores": {
                "Water": 75,
                "Roads": 60,
                "Health": 85
            },
            "overall_score": 73,
            "weak_areas": ["Roads", "Sanitation"]
        }

    @staticmethod
    def generate_priority_engine(prompt: str) -> dict:
        wards = Ward.query.limit(10).all()
        return {
            "top_10_wards": [
                {"ward": w.name, "reason": "High number of critical complaints."} for w in wards
            ]
        }

    @staticmethod
    def generate_sentiment(prompt: str) -> dict:
        return {
            "classification": "Negative",
            "explanation": "The text contains strong words indicating dissatisfaction with civic services."
        }
