import datetime
from sqlalchemy import func, desc
from app.extensions import db
from app.models.complaint import Complaint
from app.models.department import Department
from app.models.department import Ward
from app.models.user import User
from app.constants.complaint_status import ComplaintStatus

class AnalyticsService:

    @staticmethod
    def get_admin_dashboard():
        today = datetime.datetime.now(datetime.timezone.utc).date()
        week_ago = today - datetime.timedelta(days=7)
        month_ago = today - datetime.timedelta(days=30)
        
        base_query = Complaint.query.filter_by(is_deleted=False)
        
        total = base_query.count()
        open_c = base_query.filter_by(status=ComplaintStatus.OPEN.value).count()
        pending_c = base_query.filter(Complaint.status.in_([ComplaintStatus.ASSIGNED.value, ComplaintStatus.UNDER_REVIEW.value, ComplaintStatus.IN_PROGRESS.value])).count()
        resolved_c = base_query.filter_by(status=ComplaintStatus.RESOLVED.value).count()
        closed_c = base_query.filter_by(status=ComplaintStatus.CLOSED.value).count()
        
        critical_c = base_query.filter_by(severity="CRITICAL").count()
        high_c = base_query.filter_by(severity="HIGH").count()
        medium_c = base_query.filter_by(severity="MEDIUM").count()
        low_c = base_query.filter_by(severity="LOW").count()
        
        today_c = base_query.filter(func.date(Complaint.created_at) == today).count()
        weekly_c = base_query.filter(func.date(Complaint.created_at) >= week_ago).count()
        monthly_c = base_query.filter(func.date(Complaint.created_at) >= month_ago).count()
        
        # AI-ready additions
        # Top 5 Critical Wards
        top_wards = db.session.query(Ward.name, func.count(Complaint.id).label('count'))\
            .join(Complaint).filter(Complaint.is_deleted == False, Complaint.severity == 'CRITICAL')\
            .group_by(Ward.name).order_by(desc('count')).limit(5).all()
            
        # Top 5 Departments
        top_depts = db.session.query(Department.name, func.count(Complaint.id).label('count'))\
            .join(Complaint).filter(Complaint.is_deleted == False)\
            .group_by(Department.name).order_by(desc('count')).limit(5).all()
            
        # Top 5 Members (by resolved)
        top_members = db.session.query(User.name, func.count(Complaint.id).label('count'))\
            .join(Complaint, Complaint.assigned_to == User.id)\
            .filter(Complaint.status == ComplaintStatus.RESOLVED.value, Complaint.is_deleted == False)\
            .group_by(User.name).order_by(desc('count')).limit(5).all()
            
        # Recent 10 Complaints
        recent_10 = base_query.order_by(Complaint.created_at.desc()).limit(10).all()
        recent_10_data = [{"problem_id": c.problem_id, "title": c.title, "status": c.status, "severity": c.severity} for c in recent_10]
        
        return {
            "total_complaints": total,
            "status_counts": {"open": open_c, "pending": pending_c, "resolved": resolved_c, "closed": closed_c},
            "severity_counts": {"critical": critical_c, "high": high_c, "medium": medium_c, "low": low_c},
            "time_trends": {"today": today_c, "weekly": weekly_c, "monthly": monthly_c},
            "ai_insights": {
                "top_5_critical_wards": [{"ward": w[0], "count": w[1]} for w in top_wards],
                "top_5_departments": [{"department": d[0], "count": d[1]} for d in top_depts],
                "top_5_members": [{"member": m[0], "resolved": m[1]} for m in top_members],
                "recent_10_complaints": recent_10_data
            }
        }

    @staticmethod
    def get_team_dashboard(user_id):
        base_query = Complaint.query.filter_by(assigned_to=user_id, is_deleted=False)
        today = datetime.datetime.now(datetime.timezone.utc).date()
        
        my_complaints = base_query.count()
        my_open = base_query.filter_by(status=ComplaintStatus.OPEN.value).count()
        my_closed = base_query.filter_by(status=ComplaintStatus.CLOSED.value).count()
        my_pending = base_query.filter(Complaint.status.in_([ComplaintStatus.ASSIGNED.value, ComplaintStatus.UNDER_REVIEW.value, ComplaintStatus.IN_PROGRESS.value])).count()
        todays_work = base_query.filter(func.date(Complaint.updated_at) == today).count()
        
        performance = 0
        if my_complaints > 0:
            performance = round((my_closed / my_complaints) * 100, 2)
            
        return {
            "my_complaints": my_complaints,
            "my_open": my_open,
            "my_closed": my_closed,
            "my_pending": my_pending,
            "todays_work": todays_work,
            "performance_score": performance
        }

    @staticmethod
    def get_charts():
        # Dist aggregations
        dept_dist = db.session.query(Department.name, func.count(Complaint.id)).join(Complaint).group_by(Department.name).all()
        sev_dist = db.session.query(Complaint.severity, func.count(Complaint.id)).group_by(Complaint.severity).all()
        status_dist = db.session.query(Complaint.status, func.count(Complaint.id)).group_by(Complaint.status).all()
        ward_dist = db.session.query(Ward.name, func.count(Complaint.id)).join(Complaint).group_by(Ward.name).all()
        
        return {
            "department_distribution": [{"department": d[0], "count": d[1]} for d in dept_dist],
            "severity_distribution": [{"severity": s[0], "count": s[1]} for s in sev_dist],
            "status_distribution": [{"status": s[0], "count": s[1]} for s in status_dist],
            "ward_distribution": [{"ward": w[0], "count": w[1]} for w in ward_dist]
        }
        
    @staticmethod
    def get_department_analytics():
        depts = Department.query.all()
        analytics = []
        for d in depts:
            total = d.complaints.count()
            resolved = d.complaints.filter_by(status=ComplaintStatus.RESOLVED.value).count()
            res_rate = (resolved/total * 100) if total > 0 else 0
            backlog = d.complaints.filter(Complaint.status.notin_([ComplaintStatus.RESOLVED.value, ComplaintStatus.CLOSED.value])).count()
            crit = d.complaints.filter_by(severity="CRITICAL").count()
            
            analytics.append({
                "department": d.name,
                "total": total,
                "resolution_rate": round(res_rate, 2),
                "backlog": backlog,
                "critical_cases": crit
            })
        return analytics
        
    @staticmethod
    def get_ward_analytics():
        wards = Ward.query.all()
        analytics = []
        for w in wards:
            total = w.complaints.count()
            resolved = w.complaints.filter_by(status=ComplaintStatus.RESOLVED.value).count()
            res_rate = (resolved/total * 100) if total > 0 else 0
            
            analytics.append({
                "ward": w.name,
                "total": total,
                "resolution_rate": round(res_rate, 2)
            })
        return analytics

    @staticmethod
    def get_member_performance():
        members = User.query.filter_by(is_active=True).all()
        analytics = []
        for m in members:
            raised = Complaint.query.filter_by(assigned_to=m.id).count()
            closed = Complaint.query.filter_by(assigned_to=m.id, status=ComplaintStatus.CLOSED.value).count()
            analytics.append({
                "member_name": m.name,
                "complaints_assigned": raised,
                "complaints_closed": closed,
                "performance": round((closed/raised*100) if raised > 0 else 0, 2)
            })
        return sorted(analytics, key=lambda x: x['performance'], reverse=True)
