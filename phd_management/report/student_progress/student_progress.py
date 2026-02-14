import frappe
from frappe import _

def execute(filters=None):
	columns = [
		_("Registration No") + ":Link/Student:120",
		_("Student Name") + ":Data:150",
		_("Department") + ":Link/Department:120",
		_("Supervisor") + ":Link/Supervisor:150",
		_("Status") + ":Data:120",
		_("Last Review Date") + ":Date:120"
	]
	
	# Fetch basic student data
	students = frappe.db.sql("""
		SELECT
			name as student_id,
			first_name,
			last_name,
			department,
			workflow_state
		FROM
			`tabStudent`
	""", as_dict=1)
	
	data = []
	for student in students:
		# Fetch supervisor linked to student
		# Note: Supervisor is not a direct field in Student based on our Sprint 1 design (it's in Progress Review), 
		# but usually it IS in Student. Let's assume we missed it or it's fetched via custom logic.
		# For this report, we'll fetch the supervisor from the LATEST Progress Review if available, 
		# or leave blank if we didn't add a direct link in Student DocType (which we should have!).
		# Let's check our Student DocType... we didn't add 'supervisor' field in Sprint 1. 
		# We only added it to 'Progress Review'. This is a design gap we should fix or workaround.
		# Workaround: Fetch from latest Progress Review.
		
		last_review = frappe.get_all("Progress Review", 
			filters={"student": student.student_id, "docstatus": 1},
			fields=["review_date", "supervisor"],
			order_by="review_date desc",
			limit=1
		)
		
		supervisor_name = last_review[0].supervisor if last_review else ""
		last_review_date = last_review[0].review_date if last_review else None
		
		row = [
			student.student_id,
			f"{student.first_name} {student.last_name or ''}",
			student.department,
			supervisor_name,
			student.workflow_state,
			last_review_date
		]
		data.append(row)
		
	return columns, data
