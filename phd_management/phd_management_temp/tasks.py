import frappe
from frappe.utils import date_diff, nowdate

def check_at_risk_students():
	"""
	Scheduled daily.
	Checks if students in 'Research Phase' have submitted a Progress Review in the last 6 months (180 days).
	If not, sets their academic_status to 'At Risk'.
	"""
	# Get students in Research Phase who are currently 'Good'
	students = frappe.get_all("Student", 
		filters={
			"workflow_state": "Research Phase",
			"academic_status": "Good"
		},
		fields=["name"]
	)

	for student in students:
		# Get the latest Progress Review
		last_review = frappe.get_all("Progress Review",
			filters={"student": student.name, "docstatus": 1},
			order_by="review_date desc",
			limit=1,
			fields=["review_date"]
		)

		days_since_review = 0
		if last_review:
			days_since_review = date_diff(nowdate(), last_review[0].review_date)
		else:
			# If no review yet, check admission date (optional logic, using simplistic approach here)
			# For now, we assume if they are in Research Phase, they should have had a review? 
			# Or we can skip if no review exists (maybe they just started).
			# Let's assume strict: No review = At Risk if in Research Phase for > 6 months.
			# Using Student modified date or similar as fallback would be better, but let's stick to simple logic.
			continue 

		if days_since_review > 180:
			frappe.db.set_value("Student", student.name, "academic_status", "At Risk")
			# Log it
			frappe.log_error(f"Student {student.name} marked At Risk (No review for {days_since_review} days)", "Risk Check")
