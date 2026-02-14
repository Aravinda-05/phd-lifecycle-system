import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate

class ProgressReview(Document):
	def validate(self):
		self.validate_student_status()
		self.validate_review_date()

	def validate_student_status(self):
		student_status = frappe.db.get_value("Student", self.student, "workflow_state")
		if student_status in ["Suspended", "Graduated"]:
			frappe.throw(f"Cannot create Progress Review for a student who is {student_status}.")

	def validate_review_date(self):
		if self.review_date and getdate(self.review_date) > getdate(nowdate()):
			frappe.throw("Review Date cannot be in the future.")
