from datetime import datetime, timezone
from sqlalchemy import or_
from app.extensions import db
from app.models.citizen import Citizen
from app.models.complaint import Complaint
from app.constants.complaint_status import ComplaintStatus
from app.services.activity_logger import ActivityLogger

class CitizenService:
    @staticmethod
    def create_citizen(data, current_user_id=None):
        if Citizen.query.filter_by(voter_id=data.get('voter_id')).first():
            return None, "Voter ID already exists"
        if Citizen.query.filter_by(phone_number=data.get('phone_number')).first():
            return None, "Phone number already exists"
            
        citizen = Citizen(
            voter_id=data.get('voter_id'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            phone_number=data.get('phone_number'),
            address=data.get('address'),
            user_id=data.get('user_id') # Can be null
        )
        db.session.add(citizen)
        db.session.commit()
        
        ActivityLogger.log("CITIZEN_CREATED", f"Created citizen {citizen.voter_id}", current_user_id)
        return citizen, None

    @staticmethod
    def get_citizens(voter_id=None, name=None, phone=None):
        query = Citizen.query.filter_by(is_deleted=False)
        if voter_id:
            query = query.filter(Citizen.voter_id.ilike(f"%{voter_id}%"))
        if name:
            query = query.filter(or_(
                Citizen.first_name.ilike(f"%{name}%"),
                Citizen.last_name.ilike(f"%{name}%")
            ))
        if phone:
            query = query.filter(Citizen.phone_number.ilike(f"%{phone}%"))
        return query.all()

    @staticmethod
    def get_citizen_by_id(citizen_id):
        return Citizen.query.filter_by(id=citizen_id, is_deleted=False).first()

    @staticmethod
    def update_citizen(citizen_id, data, current_user_id=None):
        citizen = CitizenService.get_citizen_by_id(citizen_id)
        if not citizen:
            return None, "Citizen not found"
            
        if 'voter_id' in data and data['voter_id'] != citizen.voter_id:
            if Citizen.query.filter_by(voter_id=data['voter_id']).first():
                return None, "Voter ID already exists"
            citizen.voter_id = data['voter_id']
            
        if 'phone_number' in data and data['phone_number'] != citizen.phone_number:
            if Citizen.query.filter_by(phone_number=data['phone_number']).first():
                return None, "Phone number already exists"
            citizen.phone_number = data['phone_number']
            
        if 'first_name' in data: citizen.first_name = data['first_name']
        if 'last_name' in data: citizen.last_name = data['last_name']
        if 'address' in data: citizen.address = data['address']
        if 'user_id' in data: citizen.user_id = data['user_id']

        db.session.commit()
        ActivityLogger.log("CITIZEN_UPDATED", f"Updated citizen {citizen.voter_id}", current_user_id)
        return citizen, None

    @staticmethod
    def delete_citizen(citizen_id, current_user_id=None):
        citizen = CitizenService.get_citizen_by_id(citizen_id)
        if not citizen:
            return False, "Citizen not found"
            
        # Soft delete
        citizen.is_deleted = True
        citizen.deleted_at = datetime.now(timezone.utc)
        db.session.commit()
        ActivityLogger.log("CITIZEN_DELETED", f"Soft deleted citizen {citizen.voter_id}", current_user_id)
        return True, None

    @staticmethod
    def get_citizen_history(voter_id):
        citizen = Citizen.query.filter_by(voter_id=voter_id, is_deleted=False).first()
        if not citizen:
            return None, "Citizen not found"
            
        complaints = Complaint.query.filter_by(citizen_id=citizen.id, is_deleted=False).order_by(Complaint.created_at.desc()).all()
        
        total_complaints = len(complaints)
        open_count = sum(1 for c in complaints if c.status == ComplaintStatus.OPEN.value)
        pending_count = sum(1 for c in complaints if c.status in [ComplaintStatus.ASSIGNED.value, ComplaintStatus.UNDER_REVIEW.value, ComplaintStatus.IN_PROGRESS.value])
        closed_count = sum(1 for c in complaints if c.status in [ComplaintStatus.RESOLVED.value, ComplaintStatus.CLOSED.value])
        
        departments_involved = list(set([c.department.name for c in complaints if c.department]))
        
        # Avg resolution time
        total_time = 0
        resolved_complaints = [c for c in complaints if c.status in [ComplaintStatus.RESOLVED.value, ComplaintStatus.CLOSED.value]]
        for rc in resolved_complaints:
            resolution_time = (rc.updated_at - rc.created_at).total_seconds()
            total_time += resolution_time
            
        avg_resolution_time_hrs = (total_time / len(resolved_complaints)) / 3600 if resolved_complaints else 0

        latest_10 = [{
            "problem_id": c.problem_id,
            "title": c.title,
            "status": c.status,
            "created_at": c.created_at.isoformat()
        } for c in complaints[:10]]

        # Build timeline from latest 10
        timeline = []
        for c in complaints[:10]:
            for h in c.history:
                timeline.append({
                    "problem_id": c.problem_id,
                    "status": h.status_changed_to,
                    "date": h.created_at.isoformat(),
                    "notes": h.notes
                })
        timeline = sorted(timeline, key=lambda x: x['date'], reverse=True)

        return {
            "citizen_details": {
                "voter_id": citizen.voter_id,
                "name": f"{citizen.first_name} {citizen.last_name}",
                "phone": citizen.phone_number,
                "address": citizen.address
            },
            "metrics": {
                "total_complaints": total_complaints,
                "open_count": open_count,
                "pending_count": pending_count,
                "closed_count": closed_count,
                "avg_resolution_time_hrs": round(avg_resolution_time_hrs, 2),
                "departments_involved": departments_involved
            },
            "latest_10_complaints": latest_10,
            "timeline": timeline
        }, None
