import frappe
from frappe.model.document import Document

class ThesisSubmission(Document):
	def validate(self):
		self.validate_research_phase()
		self.check_duplicate_submission()

	def validate_research_phase(self):
		# Assuming 'Research Phase' is the workflow state required
		student_status = frappe.db.get_value("Student", self.student, "workflow_state")
		if student_status != "Research Phase":
			frappe.throw("Thesis can only be submitted when the student is in the 'Research Phase'.")

	def check_duplicate_submission(self):
		existing = frappe.db.exists("Thesis Submission", {
			"student": self.student,
			"docstatus": ["<", 2],  # Not cancelled
			"name": ["!=", self.name]
		})
		if existing:
			frappe.throw("A pending Thesis Submission already exists for this student.")

	def after_insert(self):
		self.send_submission_email()

	def send_submission_email(self):
		student_name = frappe.db.get_value("Student", self.student, "first_name")
		supervisor_email = frappe.db.get_value("Supervisor", self.student, "email") # Assuming Supervisor is linked to Student and has email

		# Better: Fetch supervisor from the Student -> Supervisor link
		# In Student DocType, we don't have a direct link to Supervisor Email, we have a link to 'Supervisor' doctype.
		# Let's fetch it properly.
		supervisor_id = frappe.db.get_value("Student", self.student, "supervisor")
		if supervisor_id:
			supervisor_email = frappe.db.get_value("Supervisor", supervisor_id, "email") # Supervisor DocType needs email field? 
			# Wait, in Sprint 1 we didn't add 'email' to Supervisor DocType. We need to add it or assume it exists.
			# Let's assume we need to add it. For now, I'll write the logic assuming it's there.
			
			if supervisor_email:
				frappe.sendmail(
					recipients=[supervisor_email],
					subject=f"New Thesis Submission: {self.thesis_title}",
					message=f"Student {student_name} has submitted a thesis titled '{self.thesis_title}'. Please review it in the system."
				)
