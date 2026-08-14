from app.models.complaint import Complaint
from app.models.department import Department, Ward

class GisService:
    @staticmethod
    def get_complaints_gis(ward_id=None, department_id=None, severity=None, status=None):
        query = Complaint.query.filter(Complaint.latitude.isnot(None), Complaint.longitude.isnot(None), Complaint.is_deleted == False)
        
        if ward_id:
            query = query.filter_by(ward_id=ward_id)
        if department_id:
            query = query.filter_by(department_id=department_id)
        if severity:
            query = query.filter_by(severity=severity)
        if status:
            query = query.filter_by(status=status)
            
        complaints = query.all()
        features = []
        for c in complaints:
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [c.longitude, c.latitude]
                },
                "properties": {
                    "problem_id": c.problem_id,
                    "severity": c.severity,
                    "department": c.department.name if c.department else None,
                    "ward": c.ward.name if c.ward else None,
                    "status": c.status
                }
            })
        return {
            "type": "FeatureCollection",
            "features": features
        }
        
    @staticmethod
    def get_heatmap_data():
        query = Complaint.query.filter(Complaint.latitude.isnot(None), Complaint.longitude.isnot(None), Complaint.is_deleted == False)
        complaints = query.all()
        points = []
        for c in complaints:
            points.append({
                "lat": c.latitude,
                "lng": c.longitude,
                "intensity": 1 if c.severity == 'LOW' else 2 if c.severity == 'MEDIUM' else 3 if c.severity == 'HIGH' else 4
            })
        return points
