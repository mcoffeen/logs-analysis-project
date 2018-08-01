#!/usr/bin/Python3

import psycopg2
import time

DBNAME = "news"

db = psycopg2.connect(database=DBNAME)
c = db.cursor()

# What are the most popular three articles of all time?
c.execute("select articles.title, count(*) as views from articles,log where "
          "concat('/article/',articles.slug) = log.path group by "
          "articles.title order by views desc limit 3;")
results = c.fetchall()
print "\n" + "Three most popular articles of all time:" + "\n"
for result in results:
    print result[0] + ' - ' + str(result[1]) + ' views.'


# Who are the most popular article authors of all time?
c.execute("select authors.name, authorviews.totalviews as views from authors,"
          "authorviews where authors.id = authorviews.author order by "
          "views desc;")
results = c.fetchall()
print "\n" + "The most popular authors of all time:" + "\n"
for result in results:
    print result[0] + ' - ' + str(result[1]) + ' views.'


# Which days did more than 1% of requests lead to errors
c.execute("select totalviews.date, errors.errors*100/totalviews.totalviews::"
          "float as percent from errors,totalviews where errors.date = "
          "totalviews.date and errors.errors*100/totalviews.totalviews::"
          "float > 1 group by totalviews.date,errors.errors,"
          "totalviews.totalviews order by percent desc;")
results = c.fetchall()
print "\n" + "Days with more than 1% of requests leading to errors:" + "\n"
for result in results:
    print str(result[0]) + ' - ' + str(round(result[1], 2)) + "% errors" + "\n"
db.close()
