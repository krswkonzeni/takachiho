# -*- coding: utf-8 -*-
from __future__ import print_function
from pyknp import Jumanpp

import sys
import codecs
import pprint
pp = pprint.PrettyPrinter(indent=4)

def read_and_anlyze_text():
    sys.stdin = codecs.getreader('utf_8')(sys.stdin)
    sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
    jumanpp = Jumanpp()
    midasis = []
    repnames = []
    repname_counts = {}
    row_result = []
    while True:
        input_ = sys.stdin.readline()
        if input_ == '' :
            break
        else :
            input_ = input_.strip()
            if input_ == '' :
                continue
            result = jumanpp.analysis(input_)
            for mrph in result.mrph_list():
                if not repname_counts.has_key(mrph.repname):
                    repname_counts[mrph.repname] = 0
                if (not mrph.midasi in midasis) and (mrph.repname != u"") :
                    repname_counts[mrph.repname] += 1
                midasis.append(mrph.midasi)
                repnames.append(mrph.repname)
            midasis.append("\n")
            repnames.append("\n")
            repname_counts["\n"] = 0
            row_result.append(result.spec())

    yure_result = []
    for i, midasi in enumerate(midasis):
        yure = False
        if repname_counts[repnames[i]] > 1:
            yure = True
        yure_result.append({"midasi":midasi, "repname": repnames[i], "repname_count":repname_counts[repnames[i]], "yure": yure})
    return row_result, yure_result

def disp_marked_sentence(yure_result):
    print(u"<h2>表記ゆれ検出結果</h2>")
    print("<div class='sentence'>")
    for obj in yure_result:
        if obj["midasi"] == "\n":
            print("<br>")
        elif obj["yure"]:
            print('<span class="yure">', end="")
            print(obj["midasi"], end="")
            print("</span>", end="")
        else:
            print(obj["midasi"], end="")
    print("</div>")

def disp_yure(yure_result):
    print(u"<h2>表記ゆれ解析結果</h2>")
    print("<div class='yure_list'><table>")
    print(u"<tr><th>見出し</th><th>代表表記</th><th>重複数</th></tr>")
    for obj in yure_result:
        if obj["midasi"] != u"" and obj["midasi"] != u"\n":
            print("<tr><td>%s</td><td>%s</td><td>%d</td></tr>" % (obj["midasi"], obj["repname"], obj["repname_count"]))
    print("</table></div>")

def disp_structure(row_result):
    print(u"<h2>JUMAN++解析結果</h2>")
    print("<div class='structure'><pre>")
    for obj in row_result:
        print(obj)
    print("</pre></div>")

row_result, yure_result = read_and_anlyze_text()
disp_marked_sentence(yure_result)
disp_yure(yure_result)
disp_structure(row_result) #for debug