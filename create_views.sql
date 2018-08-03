--
-- Name: pageviews; Type: VIEW;
--

CREATE VIEW pageviews AS
    SELECT path, count(*) AS views
    FROM log
    WHERE status = '200 OK'
    GROUP BY path
    ORDER BY views DESC;

--
-- Name: authorviews; Type: VIEW;
--

CREATE VIEW authorviews AS
    SELECT articles.author, sum(pageviews.views) AS totalViews
    FROM articles,pageviews
    WHERE concat('/article/',articles.slug) = pageviews.path
    GROUP BY articles.author
    ORDER BY totalviews DESC;

--
-- Name: totalviews; Type: VIEW;
--

CREATE VIEW totalviews AS
    SELECT time::date AS date, count(*) AS totalviews
    FROM log
    GROUP BY date
    ORDER BY date ASC;

--
-- Name: errors; Type: VIEW;
--

CREATE VIEW errors AS
    SELECT time::date AS date, count(*) AS errors
    FROM log
    WHERE status = '404 NOT FOUND'
    GROUP BY date
    ORDER BY date ASC;