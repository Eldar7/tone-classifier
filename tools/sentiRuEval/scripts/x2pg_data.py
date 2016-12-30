#!/usr/bin/python

import sys
import libxml2
from psycopg2 import connect

# -----------------------------------------------------------------------------
# PostgreSQL connection settings
# -----------------------------------------------------------------------------
PGSQL_USER = "postgres"
PGSQL_PWD = "postgres"
PGSQL_HOST = "localhost"
# -----------------------------------------------------------------------------

# Getting Row of a table from xmlFile
def getRow(tableNode):
    row = {}
    columnNode = tableNode.children
    while columnNode is not None:
        if columnNode.type == "element":
            colName = columnNode.prop("name")
            colValue = columnNode.getContent().strip()
            # Check that text is not "NULL"
            if (colValue != "NULL"):
                # String data type
                row[colName] = "\'%s\'" % (colValue.replace('\'', '\'\''))
        columnNode = columnNode.next
    return row


# Insert Row into table
def insertRow(cursor, tableName, row):
    args = ""
    argv = ""
    for colName in row.keys():
        if (args != ""):
            args += ","
            argv += ","
        args += str(colName)
        argv += str(row[colName])

    cursor.execute("INSERT INTO %s(%s) VALUES(%s);" % (tableName, args, argv))

if (len(sys.argv) == 1):
    print "usage: {} <xmlFile>".format(sys.argv[0])
    exit(0)

# Parsing Xml File
xmlFile = sys.argv[1]
doc = libxml2.parseFile(xmlFile)
ctx = doc.xpathNewContext()
databaseNode = ctx.xpathEval("/pma_xml_export/database")[0]

# Setting up Connection
dbName = databaseNode.prop("name").lower()
connSettings = """dbname=%s user=%s password=%s host=%s""" % (dbName,
                                                              PGSQL_USER,
                                                              PGSQL_PWD,
                                                              PGSQL_HOST)
conn = connect(connSettings)
cursor = conn.cursor()

# Getting all Data Training Data from XML file
tables = ctx.xpathEval("/pma_xml_export/database/table")

for tableNode in tables:
    row = getRow(tableNode)
    insertRow(cursor, tableNode.prop("name"), row)

cursor.close()
conn.commit()
conn.close()
