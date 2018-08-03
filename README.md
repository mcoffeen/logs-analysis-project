# Logs Analysis Project

This project creates a reporting tool for a newspaper using the Python DB-API to connect to a PostgreSQL database that contains data from the newspaper's website.  The tables include data about authors, the articles they write and website traffic.

### The reporting tool will answer the following questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

### Requirements
* Python 2.7
* PostgreSQL
* psycopg2 (Python DB-API module)


### Before Running `news.py`
Three steps are required before running the program.
1. A PostgreSQL database `news` needs to be created.
`$ createdb news`
2.  Import the schema and data to the news database.  Download [newsdata.sql](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) zip file.
Extract and run:
`$ psql -d news -f newsdata.sql`
3. Create four views.
`$ psql -d news -f create_views.sql`
The four views that will be created are as follows:
**pageviews** is a view of the log table to count the number of times an article is viewed.
    ```SQL
    CREATE VIEW pageviews AS
    SELECT path, count(*) AS views
    FROM log
    WHERE status = '200 OK'
    GROUP BY path
    ORDER BY views DESC;
    ```
    **authorviews** is a view joining the articles and previously created **pageviews** view to attach author data to the page view data.
    ```SQL
    CREATE VIEW authorviews AS
    SELECT articles.author, sum(pageviews.views) AS totalViews
    FROM articles,pageviews
    WHERE concat('/article/',articles.slug) = pageviews.path
    GROUP BY articles.author
    ORDER BY totalviews DESC;
    ```
    **totalviews** is a view of all of the page views grouped by date.
    ```SQL
    CREATE VIEW totalviews AS
    SELECT time::date AS date, count(*) AS totalviews
    FROM log
    GROUP BY date
    ORDER BY date ASC;
    ```
    **errors** is a view that shows the number of page visits that resulted in an error grouped by date.
    ```SQL
    CREATE VIEW errors AS
    SELECT time::date AS date, count(*) AS errors
    FROM log
    WHERE status = '404 NOT FOUND'
    GROUP BY date
    ORDER BY date ASC;
    ```