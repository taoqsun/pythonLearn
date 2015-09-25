# -*- coding: utf-8 -*-
'''
Created on Sep 25, 2015

@author: taoqsun
'''
d = { 'Adam': 95, 'Lisa': 85, 'Bart': 59 }
def generate_tr(name, score):
    if score < 60:
        return '<tr><td>%s</td><td style="color:red">%s</td></tr>' % (name, score)
    return '<tr><td>%s</td><td>%s</td></tr>' % (name, score)
tds = [generate_tr(name, score) for name, score in d.iteritems()]
test1= '<table border="1">'
test2= '<tr><th>Name</th><th>Score</th><tr>'
test3= '\n'.join(tds)
test4= '</table>'


print test3
print tds