#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
	<title>User Signup</title>
	<style type="text/css">
		.error {
			color: red;
		}
	</style>
</head>
<body>
	<h1>
		Signup
	</h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

class MainHandler(webapp2.RequestHandler):
	def get(self):

		#add in the form fields
		add_form = """
		
		<form action="/" method="post">
			<label>Username: </label> 
			<input type="text" name="username" />
			<br>
			<label>Password: </label>
			<input type="password" name="password" />
			<br>
			<label>Verify Password: </label>
			<input type="password" name="verify" />
			<br>
			<label>Email: </label>
			<input type="text" name="email" />
			<br><br>
			<input type="submit" name"submit" value="Submit" />
		</form>
		
		"""
		content = page_header + add_form + page_footer

		self.response.write(content)

	def post(self):

		USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
		PASSWORD_RE = re.compile(r"^.{3,20}$")
		EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
		user = self.request.get("username")
		password = self.request.get("password")
		verify = self.request.get("verify")
		email = self.request.get("email")
		user_error = ""
		pass_error = ""
		verify_error = ""
		email_error = ""

		#validate username exists
		
		if len(user) < 1:
			user_error = "Username is required."
		elif USER_RE.match(user) == None:
			user_error = "That is not a valid username."

		#validate password is correct and match

		if len(password) < 1:
			pass_error = "Password is required."
		elif PASSWORD_RE.match(password) == None:
			pass_error = "Password is not valid."
		elif password != verify:
			verify_error = "Passwords must match."

		
		#if email exists, is it valid

		if len(email) > 0 and EMAIL_RE.match(email) == None:
			email_error = "Email is not valid."	

		#redirect if no errors are thrown

		if user_error == "" and pass_error == "" and verify_error == "" and email_error == "":
			self.redirect("/welcome" + "?username=" + user)
		else:
			#add in the form fields
			add_form = """
			
			<form action="/" method="post">
				<label>Username: </label> 
				<input type="text" name="username" value="{0}"/>
				<span class="error">{1}</span>
				<br>
				<label>Password: </label>
				<input type="password" name="password" />
				<span class="error">{2}</span>
				<br>
				<label>Verify Password: </label>
				<input type="password" name="verify" />
				<span class="error">{3}</span>
				<br>
				<label>Email (optional): </label>
				<input type="text" name="email" />
				<span class="error">{4}</span>
				<br><br>
				<input type="submit" name"submit" value="Submit" />
			</form>
			
			""".format(user,user_error, pass_error, verify_error, email_error)
			content = page_header + add_form + page_footer

			self.response.write(content)

class Welcome(webapp2.RequestHandler):

	def get(self):
		user = self.request.get("username")
		self.response.write("<h1>Welcome, " + user + "!</h1>")      

app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/welcome', Welcome)
], debug=True)
