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
import string
import cgi
form = """
<form method = "post">
 What is your birthday?
 <br>
<label>Month
<input type="text" name="month" value = %(month)s>
</label>
<label>Day
<input type="text" name="day" value = %(day)s>
</label>
<label>Year
<input type="text" name="year" value = %(year)s>
</label>
<div style="color:red">%(error)s</div>
<br>
<br>
<input type="submit">
</form>
"""
months = ["January",
			  "February",
			  "March",
			  "April",
			  "May",
			  "June",
			  "July",
			  "August",
			  "September",
			  "October",
			  "November",
			  "December"]
def valid_month(month):
		if month:
			actual_month = string.capitalize(month)
			if actual_month in months:
				return actual_month
				
def valid_date(date):
		if date and date.isdigit():
			date = int(date)
			if date >0 and date <=31:
				return date
	
def valid_year(year):
		if year and year.isdigit():
			year = int(year)
			if year > 1900 and year <= 2016:
				return year

def escape_html(s):
		return cgi.escape(s,quote= True)				
class MainHandler(webapp2.RequestHandler):
	def write_form(self,error="",month="",day="",year=""):
		self.response.out.write(form %{"error":error,
										"month":escape_html(month),
										"day":escape_html(day),
										"year":escape_html(year)})
	def get(self):
		self.write_form()
		
										
	def post(self):
		user_month = self.request.get('month')
		user_date = self.request.get('day')
		user_year = self.request.get('year')
		
		month = valid_month(self.request.get('month'))
		date = valid_date(self.request.get('day'))
		year = valid_year(self.request.get('year'))
		if not (month and date and year):
			self.write_form("Oops! Something went wrong!! Please re-try",user_month,user_date,user_year)
		else:
			self.redirect("/thanks")
			
			
class ThanksHandler(webapp2.RequestHandler):
    def get(self):
		self.response.out.write("Thanks! That's a totally valid day!")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
	('/thanks', ThanksHandler)],
	debug=True)
