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
import os

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

def make_page(username_error='', pass_error='', verifypass_error='', email_error='', username='', email=''):
    style = """
                <style type="text/css">
                .label {text-align: right}
                .error {color: red}
                </style>
            """
    
    name_input = "<td><input type='text' id='username' value=%s></td>" % (username)
    name_label = "<td class='label'>Username</td>"
    name_error = "<p class='error'>%s</p>" % (username_error)
    username_table = ("<tr>" +
                      name_label +
                      name_input +
                      name_error +
                      "</tr>")
    
    pass_label = "<td class='label'>Password</td>"
    pass_input = "<td><input type='password' id='password' value=''></td>"
    pass_retype = "<td><input type='password' id='verified_pass' value=''></td>"
    pass_error = "<p class='error'>%s</p>" % (pass_error)
    verify_error = "<p class='error'>%s</p>" % (verifypass_error)
    password_table = ("<tr>" +
                      pass_label +
                      pass_input + '<br/>' +
                      pass_retype +
                      pass_error +
                      "</tr>")
    
    email_label = "<td class='email'>Email (optional)</td>"
    email_input = "<td><input type='text' id='email' value=%s></td>" % (email)
    email_error = "<p class='error'>%s</p>" % (email_error)
    email_table = ("<tr>" +
                   email_label +
                   email_input +
                   email_error +
                   "</tr>")

    input_button = "<input type='submit'>"

    head = "<head>" + style + "</head>"
    header = "<h2>Signup</h2>"
    content_table = "<table>" + username_table + password_table + email_table + "</table>"
    form = "<form method='post'>" + content_table + input_button + "</form>"
    body = "<body>" + header + form + "</body>"

    full_page = "<!DOCTYPE html><html>" + head + body + "</html>"

    return full_page 

class Signup(webapp2.RequestHandler):

    def get(self):
        self.response.write(make_page())

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verified_pass')
        email = self.request.get('email')

        params = dict()

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.response.write(make_page(params.get('error_username',''),
                                          params.get('error_password', ''), 
                                          params.get('error_verify', ''), 
                                          params.get('error_email', ''),
                                          username,
                                          email))
        else:
            self.redirect('/welcome?username=' + username)

app = webapp2.WSGIApplication([
    ('/', Signup)
], debug=True)
