# Logs Analysis Project

This project creates a reporting tool for a newspaper using the Python DB-API to connect to a PostgreSQL database that contains data from the newspaper's website.  The tables include data about authors, the articles they write and website traffic.

### The reporting tool will answer the following questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

### Before Running `news.py`
Four views need to be created in the database before running the Python code.
1. **pageviews** is a view of the log table to count the number of times an article is viewed.

    `create view pageviews as select path, count(*) as views from log where status = '200 OK' group by path order by views desc;`
2. **authorviews** is a view joining the articles and previously created **pageviews** view to attach author data to the page view data.

    `create view authorviews as select articles.author, sum(pageviews.views) as totalViews from articles,pageviews where concat('/article/',articles.slug) = pageviews.path group by articles.author order by totalviews desc;`
3. **totalviews** is a view of all of the page views grouped by date.

    `create view totalviews as select time::date as date, COUNT(*) as totalviews from log GROUP BY date order by date asc;`
4. **errors** is a view that shows the number of page visits that resulted in an error grouped by date.

    `create view errors as select time::date as date, COUNT(*) as errors from log where status = '404 NOT FOUND' GROUP BY date order by date asc;`