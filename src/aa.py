#!/usr/bin/python2
#============================================================================
# Filename:      s2s-security.py
# Created at:    Fri May 09 13:06:23 UTC 2014
#
# Author:        Chris Tracy
#
# License
#
# The contents of this file are subject to the Cisco Commercial Software
# License (the "License").  You may not copy or use this file, in either
# source code or executable form, except in compliance with the License.
# You may obtain a copy of the License by contacting Cisco Systems, Inc.
# at http:#www.cisco.com.
#
# Copyrights
#
# Portions created by or assigned to Cisco Systems, Inc. are
# Copyright (c) 2014 Cisco Systems, Inc. All Rights Reserved
#
# Last Modified   : $Date: $
# Last Modified By: $Author: $
# Revision        : $Revision: $
#============================================================================
import sys
import os.path
from optparse import OptionParser
import xml.etree.ElementTree as ET
from subprocess import Popen, PIPE

ver='0.0.1'
version='%prog ' + ver
usage = """Populates the S2S Security information in the Jabber DB

%prog [options] sql_file """

# The SQL Script supplied to this utility should be similar to this:
'''
SET head off
SET pagesize 0
SET verify off
SET feedback off
SET autocommit off

/* If the script fails, leave the table as is... */
WHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK

/* Remove all current entries */
DELETE FROM s2s_security_levels;

/* Populate the full list of domain pairs and security levels */
INSERT INTO s2s_security_levels VALUES('local1', 'remote1', 'strict');
INSERT INTO s2s_security_levels VALUES('local1', 'remote2', 'encrypted');
INSERT INTO s2s_security_levels VALUES('local1', 'remote3', 'plain-only');
INSERT INTO s2s_security_levels VALUES('local1', 'remote4', 'optional');
INSERT INTO s2s_security_levels VALUES('local2', 'remote3', 'encrypted');
INSERT INTO s2s_security_levels VALUES('local2', 'remote5', 'optional');

COMMIT;
'''

NS_JABBER_CONFIG='{http://www.jabber.com/config}'
JABBER_CONFIG_HOME='/opt/jabber/xcp/etc/'

def runSqlScript(sql_script, connect_string):
    if os.path.isfile(sql_script) is False:
        logit("Unable to access specified SQL script %s" % sql_script)
        raise
    else:
        return runSqlQuery('@%s' % sql_script, connect_string)

def runSqlQuery(sql_command, connect_string):
    session = Popen(['sqlplus', '-L', '-S', connect_string],
                    stdin=PIPE, stdout=PIPE, stderr=PIPE)
    session.stdin.write(sql_command)
    return session.communicate()

def grockConfig(config_file):

    if os.path.isfile(config_file) is False:
        logit("Unable to access %s to obtain DB creds" % config_file)
        raise

    tree = ET.parse(config_file)
    doc = tree.getroot()

    ns = NS_JABBER_CONFIG
    username = doc.findtext('%sglobal/%sdatabase/%susername' % (ns, ns, ns))
    password = doc.findtext('%sglobal/%sdatabase/%spassword' % (ns, ns, ns))
    ora_sid  = doc.findtext('%sglobal/%sdatabase/%sdatasource' % (ns, ns, ns))
    return username, password, ora_sid

def display_row_count(connect_string):
    sql_cmd = "set heading off \n SELECT COUNT(*) FROM s2s_security_levels;"
    return runSqlQuery(sql_cmd, connect_string)[0].strip()

def logit(msg):
    if options.quiet is False:
        print msg

# Parse options
parser = OptionParser(usage=usage, version=version)
parser.add_option("-q", "--quiet", help="Turn off logging", default=False,
                  dest='quiet', action="store_true")
parser.add_option("-j", "--jabber", dest='jabber',
                  default=JABBER_CONFIG_HOME, metavar="JABBER_CFG_HOME",
                  help="Jabber config directory for obtaining DB creds")

parser.add_option("-c", "--connect", dest='connect', metavar="DB_CNX_STR",
                  help="Connection parameters for DB. E.G., user/pass@SID")
parser.add_option("-z", "--jabber_zone", dest='jabber_zone',
                  metavar="JABBER_ZONE",
                  help="Jabber Zone name to use to locate config file")

(options, args) = parser.parse_args()

if len(args) != 1:
    parser.print_help()
    sys.exit(64)

sql_script = args[0]

retval = 0
try:
    if (options.connect is not None):
        sql_connect = options.connect
    else:
        config_file = "%s/%s.xml" % (options.jabber, options.jabber_zone)
        sql_connect = "%s/%s@%s" %  grockConfig(config_file)
except:
    logit("Unable to determine DB connection parameters!")
    retval = 1
else:
    try:
        sql_err = runSqlScript(sql_script, sql_connect)[0]
        if len(sql_err) > 0:
            logit("SQL Failure: %s" % sql_err)
            raise
        logit("Successfully updated the s2s_security_levels table (row count="
              "%s)" % display_row_count(sql_connect))

    except:
        logit("Unable to update s2s_security_levels in database!")
        retval = 1

sys.exit(retval)
