import os
import datetime
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models.complaint import Complaint, ComplaintHistory, Attachment
from app.models.citizen import Citizen
from app.constants.complaint_status import ComplaintStatus
from app.services.activity_logger import ActivityLogger

class ComplaintService:
    @staticmethod
    def generate_problem_id():
        year = datetime.datetime.now().year
        last_complaint = Complaint.query.filter(Complaint.problem_id.like(f"MHN-{year}-%")).order_by(Complaint.problem_id.desc()).first()
        if not last_complaint:
            sequence = 1
        else:
            last_seq = int(last_complaint.problem_id.split("-")[-1])
            sequence = last_seq + 1
        return f"MHN-{year}-{sequence:06d}"

    @staticmethod
    def check_duplicate(voter_id, department_id, address, description):
        score = 0
        citizen = Citizen.query.filter_by(voter_id=voter_id).first()
        if not citizen:
            return 0
            
        # Get all active complaints for this citizen
        recent_complaints = Complaint.query.filter_by(citizen_id=citizen.id, is_deleted=False).all()
        
        max_score = 0
        for comp in recent_complaints:
            current_score = 0
            # Same Citizen (already filtered) = 40%
            current_score += 40
            
            # Same Department = 20%
            if comp.department_id and str(comp.department_id) == str(department_id):
                current_score += 20
                
            # Same Address = 20%
            if comp.address and address and comp.address.lower().strip() == address.lower().strip():
                current_score += 20
                
            # Similar Description (Basic rule-based substring matching for simplicity) = 20%
            if description and comp.description:
                words1 = set(description.lower().split())
                words2 = set(comp.description.lower().split())
                if words1 and words2:
                    overlap = len(words1.intersection(words2)) / float(min(len(words1), len(words2)))
                    if overlap > 0.5:
                        current_score += 20
                        
            if current_score > max_score:
                max_score = current_score
                
        return max_score

    @staticmethod
    def handle_attachments(files, problem_id):
        attachments = []
        upload_folder = os.path.join(os.getenv("UPLOAD_FOLDER", "./uploads"), "complaints", problem_id)
        os.makedirs(upload_folder, exist_ok=True)
        
        allowed_extensions = {'.png', '.jpg', '.jpeg', '.pdf', '.doc', '.docx'}
        
        for file in files:
            if file.filename:
                ext = os.path.splitext(file.filename)[1].lower()
                if ext in allowed_extensions:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(upload_folder, filename)
                    file.save(file_path)
                    
                    # Store relative path in DB
                    db_path = f"complaints/{problem_id}/{filename}"
                    attachments.append({
                        "file_path": db_path,
                        "file_type": file.content_type,
                        "original_filename": filename
                    })
        return attachments

    @staticmethod
    def create_complaint(data, files=None, current_user_id=None):
        citizen = Citizen.query.filter_by(voter_id=data.get('voter_id')).first()
        if not citizen:
            return None, "Citizen not found. Please register citizen first."
            
        problem_id = ComplaintService.generate_problem_id()
        
        complaint = Complaint(
            problem_id=problem_id,
            title=data.get('title'),
            description=data.get('description'),
            address=data.get('address'),
            severity=data.get('severity', 'MEDIUM'),
            citizen_id=citizen.id,
            department_id=data.get('department_id'),
            ward_id=data.get('ward_id')
        )
        db.session.add(complaint)
        db.session.flush() # To get the complaint ID
        
        # Add initial history
        history = ComplaintHistory(
            complaint_id=complaint.id,
            status_changed_to=ComplaintStatus.OPEN.value,
            notes="Complaint registered.",
            changed_by=current_user_id
        )
        db.session.add(history)
        
        # Handle attachments
        if files:
            atts_data = ComplaintService.handle_attachments(files, problem_id)
            for att in atts_data:
                db.session.add(Attachment(
                    complaint_id=complaint.id,
                    file_path=att['file_path'],
                    file_type=att['file_type'],
                    original_filename=att['original_filename']
                ))
        
        db.session.commit()
        ActivityLogger.log("COMPLAINT_CREATED", f"Created complaint {problem_id}", current_user_id)
        
        return complaint, None

    @staticmethod
    def get_complaints():
        return Complaint.query.filter_by(is_deleted=False).all()

    @staticmethod
    def get_complaint_by_id(complaint_id):
        # We can search by UUID or problem_id
        c = Complaint.query.filter_by(id=complaint_id, is_deleted=False).first()
        if not c:
            c = Complaint.query.filter_by(problem_id=complaint_id, is_deleted=False).first()
        return c

    @staticmethod
    def update_complaint(complaint_id, data, current_user_id=None):
        complaint = ComplaintService.get_complaint_by_id(complaint_id)
        if not complaint:
            return None, "Complaint not found"
            
        status_changed = False
        old_status = complaint.status
        
        if 'status' in data and data['status'] != complaint.status:
            complaint.status = data['status']
            status_changed = True
            
        if 'title' in data: complaint.title = data['title']
        if 'description' in data: complaint.description = data['description']
        if 'address' in data: complaint.address = data['address']
        if 'severity' in data: complaint.severity = data['severity']
        if 'department_id' in data: complaint.department_id = data['department_id']
        if 'ward_id' in data: complaint.ward_id = data['ward_id']
        if 'assigned_to' in data: complaint.assigned_to = data['assigned_to']
        
        if status_changed:
            history = ComplaintHistory(
                complaint_id=complaint.id,
                status_changed_to=complaint.status,
                notes=data.get('notes', f"Status updated from {old_status} to {complaint.status}"),
                changed_by=current_user_id
            )
            db.session.add(history)
            ActivityLogger.log("COMPLAINT_STATUS_CHANGED", f"Complaint {complaint.problem_id} status changed to {complaint.status}", current_user_id)
        
        db.session.commit()
        ActivityLogger.log("COMPLAINT_UPDATED", f"Updated complaint {complaint.problem_id}", current_user_id)
        return complaint, None

    @staticmethod
    def delete_complaint(complaint_id, current_user_id=None):
        complaint = ComplaintService.get_complaint_by_id(complaint_id)
        if not complaint:
            return False, "Complaint not found"
            
        complaint.is_deleted = True
        complaint.deleted_at = datetime.datetime.now(datetime.timezone.utc)
        db.session.commit()
        
        ActivityLogger.log("COMPLAINT_DELETED", f"Soft deleted complaint {complaint.problem_id}", current_user_id)
        return True, None
