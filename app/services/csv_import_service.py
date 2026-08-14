import csv
import io
from app.services.complaint_service import ComplaintService
from app.models.citizen import Citizen
from app.models.department import Department
from app.services.activity_logger import ActivityLogger

class CsvImportService:
    @staticmethod
    def import_complaints(file, current_user_id=None):
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        reader = csv.DictReader(stream)
        
        success_count = 0
        errors = []
        
        required_columns = {'voter_id', 'title', 'description', 'department'}
        
        if not reader.fieldnames or not required_columns.issubset(set(reader.fieldnames)):
            return None, [f"Missing required columns. Expected at least: {', '.join(required_columns)}"]

        for row_idx, row in enumerate(reader, start=1):
            try:
                voter_id = row.get('voter_id')
                title = row.get('title')
                description = row.get('description')
                department_name = row.get('department')
                address = row.get('address', '')
                severity = row.get('severity', 'MEDIUM')
                
                if not voter_id or not title or not description:
                    errors.append({"row": row_idx, "error": "Missing required fields (voter_id, title, description)"})
                    continue
                    
                citizen = Citizen.query.filter_by(voter_id=voter_id).first()
                if not citizen:
                    errors.append({"row": row_idx, "error": f"Citizen with voter_id {voter_id} not found"})
                    continue
                    
                department_id = None
                if department_name:
                    dept = Department.query.filter_by(name=department_name).first()
                    if dept:
                        department_id = dept.id
                    else:
                        errors.append({"row": row_idx, "error": f"Department {department_name} not found"})
                        continue
                        
                # Check duplicate
                dup_score = ComplaintService.check_duplicate(voter_id, department_id, address, description)
                if dup_score > 60:
                    errors.append({"row": row_idx, "error": f"Duplicate complaint detected (Score: {dup_score})"})
                    continue
                    
                data = {
                    'voter_id': voter_id,
                    'title': title,
                    'description': description,
                    'address': address,
                    'severity': severity,
                    'department_id': department_id
                }
                
                complaint, err = ComplaintService.create_complaint(data, current_user_id=current_user_id)
                if err:
                    errors.append({"row": row_idx, "error": err})
                else:
                    success_count += 1
            except Exception as e:
                errors.append({"row": row_idx, "error": str(e)})
                
        ActivityLogger.log("CSV_IMPORT", f"Imported {success_count} complaints. Errors: {len(errors)}", current_user_id)
        
        return {
            "success_count": success_count,
            "error_count": len(errors),
            "errors": errors
        }, None
