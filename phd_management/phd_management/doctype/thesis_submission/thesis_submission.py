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
