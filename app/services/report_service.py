import io
import csv
from reportlab.pdfgen import canvas
from openpyxl import Workbook
from app.services.activity_logger import ActivityLogger

class ReportService:
    @staticmethod
    def generate_csv(data, headers, user_id=None):
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(headers)
        for row in data:
            writer.writerow(row)
        ActivityLogger.log("REPORT_GENERATED", "Generated CSV report", user_id)
        return output.getvalue().encode('utf-8')

    @staticmethod
    def generate_excel(data, headers, user_id=None):
        wb = Workbook()
        ws = wb.active
        ws.append(headers)
        for row in data:
            ws.append(row)
        output = io.BytesIO()
        wb.save(output)
        ActivityLogger.log("REPORT_GENERATED", "Generated Excel report", user_id)
        return output.getvalue()

    @staticmethod
    def generate_pdf(data, headers, title="Report", user_id=None):
        output = io.BytesIO()
        p = canvas.Canvas(output)
        p.drawString(100, 800, title)
        
        y = 750
        p.drawString(100, y, " | ".join(headers))
        y -= 20
        for row in data:
            p.drawString(100, y, " | ".join([str(x) for x in row]))
            y -= 20
            if y < 50:
                p.showPage()
                y = 800
                
        p.save()
        ActivityLogger.log("REPORT_GENERATED", f"Generated PDF report: {title}", user_id)
        return output.getvalue()
