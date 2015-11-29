#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from psycopg2 import connect
from pymystem3 import Mystem
from inspect import getsourcefile
from os.path import abspath, dirname
import model_core

sys.path.insert(0, dirname(abspath(getsourcefile(lambda:0))) + '/../aux')
from tvoc import TermVocabulary
from msg import Message
import pconf
import twits
import prob
import test

argc = len(sys.argv)
if (argc == 1):
    print """%s\n%s\n%s\n%s\n%s"""%(
        "Usage: baseline_bank_test <database> <train_table> <output> <pconf_output>",
        "<task_type> -- type of task",
        "<database> -- database to connect for training data",
        "<test_table> -- table with testing data for bank",
        "<output> -- file to save tonality vectors",
        "<pconf_output> -- file to save configuration for predict.py")
    exit(0)

config = {
    'task_type' : sys.argv[1],
    'database' : sys.argv[2],
    'test_table' : sys.argv[3],
    'output' : sys.argv[4],
    'pconf_output' : sys.argv[5]
}

etalon_table = config['test_table']

# Connect to a database
connSettings = """dbname=%s user=%s password=%s host=%s"""%(
    config['database'], "postgres", "postgres", "localhost")
conn = connect(connSettings)
cursor = conn.cursor()

# create new etalon table
new_etalon_table = 'tf_idf_' + config['task_type'] + '_new_etalon'
out_table = 'tf_idf_' + config['task_type'] + '_results'
print "create_table:", new_etalon_table
test.create_table_as(conn, new_etalon_table, etalon_table)
columns = twits.get_score_columns(config['task_type'])

# make problem
m = Mystem(entire_input=False)
tvoc = TermVocabulary()
problem = []
limit = sys.maxint
vectors = []
for score in [-1, 0, 1]:
    # getting twits with the same score
    twits.get(config['task_type'], cursor, etalon_table, score, limit)
    # processing twits
    row = twits.next_row(cursor, score)
    count = 0
    while row is not None:
        text = row[0]
        index = row[1]
        terms = model_core.process_text(m, text, tvoc)
        test.add_row(conn, new_etalon_table, columns, row[2:])
        vectors.append({'id': index, 'terms' : terms})
        # next row
        row = twits.next_row(cursor, score)
        count += 1
    print "class:\t%s; %s"%(score, count)

# make problem
for vector in vectors:
    problem.append(model_core.train_vector(
        vector['id'], tvoc, vector['terms']))

#save problem
prob.save(problem, config['output'])

#save .pconf
pconf.save(config['task_type'], new_etalon_table,
    out_table, config['pconf_output'])
