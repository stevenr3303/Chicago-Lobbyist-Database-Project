#
# datatier.py
#
# Executes SQL queries against the given database.
#
import sqlite3
import logging

logger = logging.getLogger(__name__)


##################################################################
#
# select_one_row:
#
# Given a database connection and a SQL Select query,
# executes this query against the database and returns
# the first row retrieved by the query (or the empty
# tuple () if no data was retrieved). The query can
# be parameterized, in which case pass the values as
# a list via parameters; this parameter is optional.
#
# Returns: first row retrieved by the given query, or
#          () if no data was retrieved. If an error
#          occurs, a msg is output and None is returned.
#
def select_one_row(dbConn, sql, parameters=None):
  if parameters is None:
      parameters = []

  dbCursor = dbConn.cursor()

  try:
      dbCursor.execute(sql, parameters)
      row = dbCursor.fetchone()
      if row is None:
          return ()
      return row
  except Exception as err:
    logger.error("select_one_row failed: %s", err)
    return ()
  finally:
      dbCursor.close()



##################################################################
#
# select_n_rows:
#
# Given a database connection and a SQL Select query,
# executes this query against the database and returns
# a list of rows retrieved by the query. If the query
# retrieves no data, the empty list [] is returned.
# The query can be parameterized, in which case pass 
# the values as a list via parameters; this parameter 
# is optional.
#
# Returns: a list of 0 or more rows retrieved by the 
#          given query; if an error occurs a msg is 
#          output and None is returned.
#
def select_n_rows(dbConn, sql, parameters = None):
  if (parameters == None):
     parameters = []

  dbCursor = dbConn.cursor()

  try:
     dbCursor.execute(sql, parameters)
     rows = dbCursor.fetchall()
     if rows is None:
      return []
     return rows
  except Exception as err:
    logger.error("select_n_rows failed: %s", err)
    return None
  finally:
     dbCursor.close()


##################################################################
#
# perform_action: 
# 
# Given a database connection and a SQL action query,
# executes this query and returns the # of rows
# modified; a return value of 0 means no rows were
# updated. Action queries are typically "insert", 
# "update", "delete". The query can be parameterized,
# in which case pass the values as a list via 
# parameters; this parameter is optional.
#
# Returns: the # of rows modified by the query; if an 
#          error occurs a msg is output and -1 is 
#          returned. Note that a return value of 0 is
#          not considered an error --- it means the
#          query did not change the database (e.g. 
#          because the where condition was false?).
#
def perform_action(dbConn, sql, parameters=None):
  if parameters is None:
    parameters = []

  dbCursor = dbConn.cursor()
  try:
    dbCursor.execute(sql, parameters)
    num_rows = dbCursor.rowcount
    return num_rows
  except Exception as err:
    logger.error("perform_action failed: %s", err)
    return -1
  finally:
    dbCursor.close()


  
