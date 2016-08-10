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
import cgi
import codecs
form="""
<!DOCTYPE html>
<html>
  <head>
    <title>Unit 2 Rot 13</title>
  </head>
  <body>
    <h2>Enter some text to ROT13:</h2>
    <form method="post">
      <textarea name="text"
                style="height: 100px; width: 400px;">%(text)s</textarea>
      <br>
      <input type="submit">
    </form>
  </body>
</html>
"""
def escape_html(s):
    return cgi.escape(s,quote= True)

class MainHandler(webapp2.RequestHandler):
    def write_form(self,text=""):
        self.response.out.write(form %{"text":escape_html(text)})
    def get(self):
        self.write_form()
    def post(self):
        input_text = self.request.get("text")
        output_text = codecs.encode(input_text, 'rot_13')
        if input_text:
            self.write_form(output_text)
app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
