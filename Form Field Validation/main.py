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
import cgi
form="""
<!DOCTYPE html>
<html>
  <head>
    <title>Homework 2</title>
  </head>
  <body>
    <form method="post">
      <label>User Name&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<input type="text" name="username" value=%(username)s><div style="color:red">%(username_error)s</div></label>
      <br>
      <label>Password&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<input type="password" name="password"><div style="color:red">%(password_error)s</div></label>
      <br>
      <label>Verify Password&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<input type="password" name="verify_password"><div style="color:red">%(password_mismatch_error)s</div></label>
      <br>
      <label>Email ID(optional)&nbsp&nbsp<input type="text" name="email" value=%(email)s><div style="color:red">%(email_error)s</div></label>
      <br>
      <input type="submit">
    </form>
  </body>
</html>
"""
def escape_html(s):
    return cgi.escape(s,quote= True)
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_username(username):
    return USER_RE.match(username)
def valid_password(password):
    return PASSWORD_RE.match(password)
def valid_email(email):
    return EMAIL_RE.match(email)

class MainHandler(webapp2.RequestHandler):
    
    def write_form(self,username="",email="",username_error="",password_error="",password_mismatch_error="",email_error=""):
        self.response.out.write(form %{"username":escape_html(username),"email":email,"username_error":username_error,"password_error":password_error,"password_mismatch_error":password_mismatch_error,"email_error":email_error})
    
    def get(self):
        self.write_form()
    
    def post(self):
        username_input = self.request.get("username")
        password_input = self.request.get("password")
        password_verify_input = self.request.get("verify_password")
        email_input = self.request.get("email")
        
        username_valid = valid_username(username_input)
        password_valid = valid_password(password_input)
        if email_input:
            email_valid = valid_email(email_input)
        else:
            email_valid = True
        
        if (username_valid and password_valid and email_valid and (password_input == password_verify_input)):
            self.redirect("/welcome?username=%s"%username_input)
        
        elif not username_valid and not password_valid:
            self.write_form(username_input,email_input,"The user name entered is invalid","The password entered is invalid")
        elif not password_valid and not(password_input == password_verify_input):
            self.write_form(username_input,email_input,"","The password entered is invalid","The passwords do not match")
        elif not password_valid and not email_valid:
            self.write_form(username_input,email_input,"","The password entered is invalid","","The email ID entered is invalid")
        elif not(password_input == password_verify_input) and not email_valid:
            self.write_form(username_input,email_input,"","","The passwords do not match","The email ID entered is invalid")
        elif not username_valid and not email_valid:
            self.write_form(username_input,email_input,"The user name entered is invalid","","","The email ID entered is invalid")
        elif not(password_input == password_verify_input) and not username_valid:
            self.write_form(username_input,email_input,"The user name entered is invalid","","The passwords do not match","")
        elif not username_valid and password_valid and not email_valid and not (password_input == password_verify_input):
            self.write_form(username_input,email_input,"The user name entered is invalid","The password entered is invalid","The passwords do not match","The email ID entered is invalid")
        elif not username_valid and not password_valid and not email_valid:
            self.write_form(username_input,email_input,"The user name entered is invalid","The password entered is invalid","","The email ID entered is invalid")
        elif not password_valid and not email_valid and not(password_input == password_verify_input):
            self.write_form(username_input,email_input,"","The password entered is invalid","The passwords do not match","The email ID entered is invalid")
        elif not email_valid and not(password_input == password_verify_input) and not username_valid:
            self.write_form(username_input,email_input,"The user name entered is invalid","","The passwords do not match","The email ID entered is invalid")
        elif not password_valid:
            self.write_form(username_input,email_input,"","The password entered is invalid")
        elif not (password_input == password_verify_input):
            self.write_form(username_input,email_input,"","","The passwords do not match")
        elif not email_valid:
            self.write_form(username_input,email_input,"","","","The email ID entered is invalid")
        elif not username_valid:
            self.write_form(username_input,email_input,"The user name entered is invalid")
            
class SuccessHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Welcome, %s!"%self.request.get("username"))
        
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', SuccessHandler)
], debug=True)