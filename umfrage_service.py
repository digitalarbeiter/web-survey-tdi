#!/usr/bin/env python
# -*- coding: utf8 -*-
# 
# Umfrage Kiga
#
# TDI Version
# 


import os
import sys
import random
from cPickle import load, dump

import tdi

import uServer
from uServer import static_file, not_found
from kiga2013 import survey_factory


VOTE_CODE_PATH = "data/vote-codes.dump"

SUBMITTED_SURVEY_DIR = "data/submitted_surveys"


def element_name(question):
    title = question["toc"] or question["title"]
    elt = title.strip().lower().encode("utf8")
    elt = elt.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
    elt = elt.replace("ß", "ss")
    elt = elt.replace(" ", "-")
    elt = "".join([
        i for i in elt if i in "-0123456789abcdefghijklmnopqrstuvwxyz"
    ])
    return elt


def session_filename(request):
    session = request.session["sid"]
    print "/tmp/survey-%r.dump" % session
    return "/tmp/survey-%r.dump" % session


def get_survey(request):
    try:
        survey = load(file(session_filename(request), "rb"))
    except:
        survey = survey_factory()
    return survey


QuestionTemplate = tdi.html.from_string("""
<div id="" name="" tdi="anchor_div">

  <a name="anchor_tag"> </a>
  <h1 tdi="title"> Titel der Frage </h1>

  <div tdi="question">
    Die Frage selbst.
  </div>

  <div tdi="subquestions">
    <table border="1" width="98%">
      <thead>
        <tr>
          <th tdi="subquestion_header"> </th>
        </tr>
      </thead>
      <tbody>
        <tr tdi="subquestion">
          <td tdi="cell"> </td>
        </tr>
      </tbody>
    </table>
    <br />
  </div>

  <div tdi="comment">
    <span tdi="comment_desc"> </span>
    <br />
    <textarea tdi="comment_text" cols="85" rows="6"> </textarea>
    <br />
  </div>

  <button type="button" tdi="next_anchor">Weiter</button>
  <input type="submit" value="Zwischenspeichern" tdi="save" />

</div>
""")


class QuestionModel(object):

    def __init__(self, prefix, question, next_anchor):
        self.prefix = prefix
        self.question = question
        self.next_anchor = next_anchor
        self.subquestions = question.get("subquestions", []) or []
        self.choices = question.get("choices", []) or []
        self.answer = question.get("answer", {}) or {}
        if len(self.choices) > 4:
            choice_width = int(60.0 / len(self.choices))
        else:
            choice_width = 15;
        subquestion_width = 100 - choice_width * len(self.choices)
        self.width = [ subquestion_width ]
        self.width.extend([ choice_width ] * len(self.choices))

    def render_anchor_div(self, node):
        anchor = element_name(self.question)
        node["id"] = anchor
        node["name"] = anchor

    def render_anchor_tag(self, node):
        anchor = element_name(self.question)
        node["id"] = anchor
        node["name"] = anchor

    def render_title(self, node):
        node.content = self.question["title"]

    def render_question(self, node):
        node.raw.content = self.question["question"].encode("utf8")

    def render_subquestions(self, node):
        if self.subquestions:
            node["style"] = "display: block"
        else:
            node["style"] = "display: none"

    def render_subquestion_header(self, node):
        columns = [ "Frage" ]
        columns.extend(self.choices)
        for colnode, (width, text) in node.iterate(zip(self.width, columns)):
            colnode["width"] = "%i%%" % width
            colnode.content = text

    def render_subquestion(self, node):
        def answer_attr(answer_dict):
            if answer_dict \
            and "answers" in answer_dict \
            and answer_dict["answers"][i][j]:
                return " checked=\"checked\" " + \
                       " defaultChecked=\"defaultChecked\" "
            else:
                return ""
        for i, (rownode, subq) in enumerate(node.iterate(self.subquestions)):
            input_type = self.question["answer_type"]
            columns = [ subq ]
            columns.extend([
                ( "<input name=\"%s_answer_%i\" value=\"%i\" " \
                + "type=\"%s\" %s />") % (
                    self.prefix, i, j, input_type, answer_attr(self.answer)
                )
                for j, choice in enumerate(self.choices)
            ])
            for colnode, col in rownode.cell.iterate(columns):
                colnode.raw.content = col.encode("utf8")

    def render_comment(self, node):
        if self.question["comment"] is None:
            node["style"] = "display: none"
        else:
            node["style"] = "display: block"

    def render_comment_desc(self, node):
        if self.subquestions and self.question["comment"]:
            node.content = self.question["comment"] + ":"
        else:
            node.content = "" # question already displayed

    def render_comment_text(self, node):
        if self.question["type"] == "votecode":
            node["name"] = "votecode"
            node["rows"] = 1
            node["cols"] = 15
        else:
            node["name"] = node["id"] = self.prefix + "_comment"
            if not self.subquestions:
                node["rows"] = 12
        node.content = self.answer.get("comment", "")

    def render_next_anchor(self, node):
        if self.next_anchor:
            node["onclick"] = "open_question(\"%s\");" % self.next_anchor
        else:
            node.content = ""

    def render_save(self, node):
        if self.question["type"] == "votecode":
            node["value"] = "Abschicken!"
        else:
            node["value"] = "Zwischenspeichern"


QuestionnaireTemplate = tdi.html.from_string("""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
  <head>

    <link rel="stylesheet" type="text/css" href="/umfrage.css" />

    <script language="javascript" tdi="all_questions">
      var ALL_QUESTIONS = []; // gets filled by render_all_questions()
    </script>

    <script language="javascript"> 
      function open_question(element) {
        for (i=0; i<ALL_QUESTIONS.length; i++) {
          var elem = document.getElementById(ALL_QUESTIONS[i]);
          if (ALL_QUESTIONS[i] == element) {
            elem.style.display = "block";
          } else {
            elem.style.display = "none";
          }
        }
      } 
      function open_all_questions() {
        for (i=0; i<ALL_QUESTIONS.length; i++) {
          var elem = document.getElementById(ALL_QUESTIONS[i]);
          elem.style.display = "block";
        }
      } 
    </script>

  </head>
  <body>

    <div class="title">
      <h1 tdi="survey_title"> Umfrage </h1>
      <span class="clickable" onclick="open_question(ALL_QUESTIONS[0]);">
        Fragen einzeln anzeigen
      </span> /
      <span class="clickable" onclick="open_all_questions();">
        Alle auf einmal anzeigen
      </span>
    </div>

    <div class="toc">
      <ul>
        <li tdi="toc"><span tdi="jump" class="clickable"></span></li>
      </ul>
    </div>

    <div class="questions">
      <form tdi="form" action="#" method="post">
        <input tdi="session_id" name="session_id" type="hidden">
        </input>
        <div id="questions" tdi="question">
          <div tdi="question"></div>
        </div>
      </form>
    </div>

    <script language="javascript">
      open_question(ALL_QUESTIONS[0]);
    </script>

  </body>
</html>
""")

class QuestionnaireModel(object):

    def __init__(self, survey):
        self.survey = survey
        self.questions = self.survey["questions"]

    def get_answers(self, submitted):
        vote_submitted = False
        for key, values in sorted(submitted.iteritems()):
            if key == "votecode":
                print "vote code: %r" % values
                vote_code = None
                try:
                    vote_code = int(values[0].strip())
                    valid_codes = load(file(VOTE_CODE_PATH, "rb"))
                    valid_codes.remove(vote_code)
                    dump(valid_codes, file(VOTE_CODE_PATH, "wb"))
                except ValueError, ex:
                    print "bad vote code: %r" % values[0]
                    for question in self.questions:
                        if question["type"] == "votecode":
                            if question.get("answer") is None:
                                question["answer"] = { }
                            print question
                            question["answer"]["comment"] = \
                                u"Ungültiger Vote-Code"
                    return vote_submitted
                submitted_file = os.path.join(
                    SUBMITTED_SURVEY_DIR,
                    "%i.dump" % vote_code,
                )
                print submitted_file
                dump(self.survey, file(submitted_file, "wb"))
                vote_submitted = True
            elif key.startswith("q_"):
                q_no = int(key.split("_")[1])
                question = self.questions[q_no]
                n_choices = len(question.get("choices", []))
                if question.get("answer") is None:
                    question["answer"] = {
                        "comment": u"",
                        "answers": [],
                    }
                    for qs in question.get("subquestions", []):
                        n_false = n_choices * [ False ]
                        question["answer"]["answers"].append(n_false)
                if key.endswith("comment"):
                    question["answer"]["comment"] = values[0]
                else:
                    subq_no = int(key.split("_")[-1])
                    sub_answer = n_choices * [False]
                    for choice in values:
                        choice = int(choice)
                        sub_answer[choice] = True
                    question["answer"]["answers"][subq_no] = sub_answer
            else:
                print "unknown key: %r (value: %r)" % (key, values)
        return vote_submitted

    def render_survey_title(self, node):
        node.content = self.survey["title"]

    def render_toc(self, node):
        for i, (subnode, question) in enumerate(node.iterate(self.questions)):
            anchor = element_name(question)
            answered = question["answer"] is not None
            subnode.jump.content = question["toc"] or question["title"]
            subnode.jump["onclick"] = "open_question(\"%s\");" % anchor

    def render_question(self, node):
        for i, (subnode, question) in enumerate(node.iterate(self.questions)):
            prefix = "q_%i" % i
            question_text = question["question"]
            if i < len(self.questions) - 1:
                next_anchor = element_name(self.questions[i+1])
            else:
                next_anchor = None
            q_model = QuestionModel(prefix, question, next_anchor)
            q = QuestionTemplate.render_string(q_model)
            subnode.raw.content = q

    def render_all_questions(self, node):
        all_questions = "var ALL_QUESTIONS = [ "
        for question in self.questions:
            all_questions += "\"%s\", " % element_name(question)
        all_questions += " \"\" ];"
        node.raw.content = all_questions


def run(request, response):
    survey = get_survey(request)
    model = QuestionnaireModel(survey)
    vote_submitted = False
    if request.postvars:
        vote_submitted = model.get_answers(request.postvars)
        dump(survey, file(session_filename(request), "wb"))
    if vote_submitted:
        html = u"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
  <head>
    <link rel="stylesheet" type="text/css" href="/umfrage.css" />
  </head>
  <body>
    <div class="title">
      <h1> Umfrage </h1>
    </div>
    <div class="toc">
      <ul>
        <li><a href="/" class="clickable">Neue Umfrage</a></li>
      </ul>
    </div>
    <div class="questions">
        <h1> Fertig </h1>
        Deine Umfrage wurde gespeichert. Vielen Dank für die Teilnahme.
        <p>/p<>
        <a href="/" class="clickable">Neue Umfrage starten</a>.
    </div>
  </body>
</html>
        """.encode("utf8")
        response["no_session"] = True
    else:
        html = QuestionnaireTemplate.render_string(model)
    response["response"] = 200
    response["header"] = [ ("Content-type", "text/html; charset=utf-8"), ]
    response["data"] = html


def generate_votecodes(n):
    print "generating %i vote codes in: %s" % (n, VOTE_CODE_PATH)
    generated = set()
    while len(generated) < n:
        generated.add(10000000 + random.randint(0, 89999999))
    dump(list(generated), file(VOTE_CODE_PATH, "wb"))
    print "generated %i vote codes in: %s" % (n, VOTE_CODE_PATH)


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--generate-vote-codes":
        generate_votecodes(int(sys.argv[2]))
        sys.exit(0)
    url_map = [
        ("/w00tw00t.*", not_found),
        ("/umfrage.css", static_file("umfrage.css", "text/css", False)),
        ("/favicon", static_file("files/favicon.gif", "image/gif")),
        ("/robots.txt", static_file("files/robots.txt", "text/plain")),
        ("/neu", run),
        ("/[A-z0-9].*", not_found),
        ("/", run),
    ]
    uServer.run(url_map, "127.0.0.1", 8000)
    #uServer.run(url_map, "88.198.106.203", 8080)

