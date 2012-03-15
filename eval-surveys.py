#!/usr/bin/env python
#
# Evaluate Surveys.
#

import os
import sys
from cPickle import load
import cjson


def all_datasets(path, predicate=None):
    if predicate is None:
        predicate = lambda x: True
    for fn in os.listdir(path):
        fn = os.path.join(path, fn)
        try:
            survey = load(file(fn, "rb"))
        except IOError, ex:
            print ex
            continue
        if not predicate(survey):
            continue
        yield survey["questions"]


def collect_questions(path, predicate=None):
    questions, answers = [], []
    for survey in all_datasets(path, predicate):
        while len(questions) < len(survey):
            questions.append(None)
            answers.append([])
        for idx, q in enumerate(survey):
            answers[idx].append(cjson.decode(q["answer"]))
            if not questions[idx]:
                q.pop("answer")
                questions[idx] = q
    return questions, answers


def evaluate_question(question, answers):
    question_type = question["type"]
    if question_type == "yes-no":
        choices = question["choices"]
        subquestions = question["subquestions"]
    else:
        choices = []
        subquestions = []
    comments = []
    sub_totals = [ [0.0 for j in choices] for i in subquestions ]
    for answer in answers:
        if answer.get("comment"):
            comments.append(answer["comment"])
        if question_type == "yes-no":
            for i_sub_q, sub_a in enumerate(answer["answers"]):
                norm = 1.0 / (sum(sub_a) or 1.0)
                norm_sub_a = [ a * norm for a in sub_a ] 
                sub_totals[i_sub_q] = map(sum, zip(
                    sub_totals[i_sub_q], norm_sub_a
                ))
    #for i, sub_total in enumerate(sub_totals):
    #    print subquestions[i]
    #    print zip(choices, sub_total)
    #print comments
    return [ zip(choices, sub_total) for sub_total in sub_totals ], comments


def plot_question(fname, question_text, data):
    import pylab
    import numpy as np
    from matplotlib.font_manager import FontProperties
    from matplotlib.text import Text
    pylab.figure().clear()
    pylab.title(question_text)
    #pylab.xlabel("Verteilung")
    #pylab.subplot(101)
    if True or len(data) < 3:
        width = 0.95
        pylab.bar(range(len(data)), [max(y, 0.01) for x, y in data], 0.95, color="g")
        pylab.xticks([i+0.5*width for i in range(len(data))], [x for x, y in data])
        pylab.yticks([0, 10, 20, 30, 40, 50])
        #ind = np.arange(len(data))
        #pylab.bar(ind, [y for x, y in data], 0.95, color="g")
        #pylab.ylabel("#")
        #pylab.ylim(ymax=45)
        #pylab.ylabel("Antworten")
        #pylab.xticks(ind+0.5, histo.get_ticks())
        #pylab.legend(loc=3, prop=FontProperties(size="smaller"))
        ##pylab.grid(True)
    else:
        pylab.pie([max(y, 0.1) for x, y in data], labels=[x for x, y in data], autopct="%.0f%%")
    pylab.savefig(fname, format="png", dpi=75)


if __name__ == "__main__":
    questions, answers = collect_questions(sys.argv[1])
    outdir = sys.argv[2]
    try:
        os.mkdir(outdir)
    except OSError, ex:
        pass # might already exist
    try:
        os.listdir(outdir)
    except OSError, ex:
        print "cannot create target directory:", outdir
        sys.exit(1)
    with file(os.path.join(outdir, "report.txt"), "wb") as report:
        report.write("# Umfrage 2011\n")
        report.write("\n\n")
        for idx, (q, a) in enumerate(zip(questions, answers)):

            print "question:", q["question"]

            report.write("## \"%s\"\n\n" % q["question"].encode("utf8"))
            answers, comments = evaluate_question(q, a)

            if answers:
                rows = [u"Frage",] + q["subquestions"]
                cols = [u"Frage",] + [choice for choice, count in answers[0]]
                cell_len = map(len, cols)
                cell_len[0] = max(map(len, rows))
                fmt = "%%-%is" % cell_len[0]
                cols[0] = fmt % cols[0]
                hr = "+-" + "-+-".join(n * "-" for n in cell_len) + "-+"
                report.write(hr.encode("utf8") + "\n")
                line = "| " + " | ".join(cols) + " |"
                report.write(line.encode("utf8") + "\n")
                report.write(hr.encode("utf8") + "\n")
                for i, subanswer in enumerate(answers):
                    cells = [ ]
                    fmt = "%%-%is" % cell_len[0]
                    cells.append(fmt % rows[i+1])
                    for choice, count in subanswer:
                        fmt = "%%%ii" % len(choice)
                        cells.append(fmt % int(count))
                    line = "| " + " | ".join(cells) + " |"
                    report.write(line.encode("utf8") + "\n")
                    report.write(hr.encode("utf8") + "\n")
            report.write("\n\n")

            # some nice pics
            report.write("### Abbildungen\n\n")
            for i, subanswer in enumerate(answers):
                fname = os.path.join(outdir, "fig_%02i_%02i.png" % (idx, i))
                title = q["subquestions"][i]
                plot_question(fname, title, subanswer)
                report.write("![image](%s)\n" % fname)
                #report.write("![%s](%s)\n" % (title.encode("utf8"), fname))
            report.write("\n\n")

            # comments section, if any
            if comments:
                report.write("### Anmerkungen\n")
                for comment in comments:
                    report.write(" * %s\n" % comment.strip().replace("\r", "").replace("\n", ". ").encode("utf8"))
                report.write("\n\n")


