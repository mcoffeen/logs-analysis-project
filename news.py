#!/usr/bin/env python

import psycopg2
import time

DBNAME = "news"

db = psycopg2.connect(database=DBNAME)
c = db.cursor()

def execute_query(query):
    """
    execute_query takes an SQL query as a parameter.
    Executes the query and returns the results as a list of tuples.
    args:
    query - an SQL query statement to be executed.

    returns:
    A list of tuples containing the results of the query.
    """
    c.execute(query)
    return c.fetchall()

def print_top_articles():
    # Prints the most popular three articles of all time.
    query="""
      SELECT articles.title, pageviews.views
      FROM articles,pageviews
      WHERE concat('/article/',articles.slug) = pageviews.path
      ORDER BY views DESC
      LIMIT 3;
      """
    results = execute_query(query)
    print "\n" + "Three most popular articles of all time:" + "\n"
    for result in results:
        print result[0] + ' - ' + str(result[1]) + ' views.'

def print_top_authors():
    # Prints a list of the most popular article authors of all time.
    query="""
      SELECT authors.name, authorviews.totalviews AS views
      FROM authors,authorviews
      WHERE authors.id = authorviews.author
      ORDER BY views DESC;
      """
    results = execute_query(query)
    print "\n" + "The most popular authors of all time:" + "\n"
    for result in results:
        print result[0] + ' - ' + str(result[1]) + ' views.'

def print_errors_over_one():
    # Prints out the days where more than 1% of requests lead to errors
    query="""
      SELECT totalviews.date, errors.errors*100/totalviews.totalviews::float
      AS percent
      FROM errors,totalviews
      WHERE errors.date = totalviews.date and
      errors.errors*100/totalviews.totalviews::float > 1
      GROUP BY totalviews.date,errors.errors,totalviews.totalviews
      ORDER BY percent DESC;
      """
    results = execute_query(query)
    print "\n" + "Days with more than 1% of requests leading to errors:" + "\n"
    for result in results:
        print str(result[0]) + ' - ' + str(round(result[1], 2)) + "% errors" + "\n"

if __name__ == '__main__':
  print_top_articles()
  print_top_authors()
  print_errors_over_one()
  db.close()



