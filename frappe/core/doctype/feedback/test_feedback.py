# Copyright (c) 2021, Frappe Technologies and Contributors
# License: MIT. See LICENSE

import frappe
import unittest

class TestFeedback(unittest.TestCase):
	def tearDown(self):
		frappe.form_dict.reference_doctype = None
		frappe.form_dict.reference_name = None
		frappe.form_dict.rating = None
		frappe.form_dict.feedback = None
		frappe.local.request_ip = None

	def test_feedback_creation_updation(self):
		from frappe.website.doctype.blog_post.test_blog_post import make_test_blog
		test_blog = make_test_blog()

		frappe.db.delete("Feedback", {"reference_doctype": "Blog Post"})

		from frappe.templates.includes.feedback.feedback import add_feedback, update_feedback

		frappe.form_dict.reference_doctype = 'Blog Post'
		frappe.form_dict.reference_name = test_blog.name
		frappe.form_dict.rating = 5
		frappe.form_dict.feedback = 'New feedback'
		frappe.local.request_ip = '127.0.0.1'

		feedback = add_feedback()

		self.assertEqual(feedback.feedback, 'New feedback')
		self.assertEqual(feedback.rating, 5)

		updated_feedback = update_feedback('Blog Post', test_blog.name, 6, 'Updated feedback')

		self.assertEqual(updated_feedback.feedback, 'Updated feedback')
		self.assertEqual(updated_feedback.rating, 6)

		frappe.db.delete("Feedback", {"reference_doctype": "Blog Post"})

		test_blog.delete()