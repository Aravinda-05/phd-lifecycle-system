import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate

class Student(Document):
	def validate(self):
		if self.date_of_admission and getdate(self.date_of_admission) > getdate(nowdate()):
			frappe.throw("Date of Admission cannot be in the future.")
