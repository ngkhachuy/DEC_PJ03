WITH
    tbl1 AS (SELECT * FROM category WHERE LVL = 1),
    tbl2 AS (SELECT * FROM category WHERE LVL = 2),
    tbl3 AS (SELECT * FROM category WHERE LVL = 3),
    tbl4 AS (SELECT * FROM category WHERE LVL = 4),
    tbl5 AS (SELECT * FROM category WHERE LVL = 5)

SELECT
    tbl1.CAT_NAME AS name_1,
    tbl2.CAT_NAME AS name_2,
    tbl3.CAT_NAME AS name_3,
    tbl4.CAT_NAME AS name_4,
    tbl5.CAT_NAME AS name_5,
    CASE
        WHEN tbl5.CAT_NAME IS NOT NULL THEN tbl5.CAT_ID
        WHEN tbl4.CAT_NAME IS NOT NULL THEN tbl4.CAT_ID
        WHEN tbl3.CAT_NAME IS NOT NULL THEN tbl3.CAT_ID
        WHEN tbl2.CAT_NAME IS NOT NULL THEN tbl2.CAT_ID
        ELSE tbl1.CAT_ID
    END AS LEAF_CAT_ID,
    CASE
        WHEN tbl5.CAT_NAME IS NOT NULL THEN tbl5.URL
        WHEN tbl4.CAT_NAME IS NOT NULL THEN tbl4.URL
        WHEN tbl3.CAT_NAME IS NOT NULL THEN tbl3.URL
        WHEN tbl2.CAT_NAME IS NOT NULL THEN tbl2.URL
        ELSE tbl1.URL
    END AS LEAF_CAT_URL
FROM
    tbl5
    RIGHT JOIN tbl4 ON tbl5.PARENT_ID = tbl4.CAT_ID
    RIGHT JOIN tbl3 ON tbl4.PARENT_ID = tbl3.CAT_ID
    RIGHT JOIN tbl2 ON tbl3.PARENT_ID = tbl2.CAT_ID
    RIGHT JOIN tbl1 ON tbl2.PARENT_ID = tbl1.CAT_ID
ORDER BY
    tbl1.CAT_ID, tbl2.CAT_ID, tbl3.CAT_ID, tbl4.CAT_ID, tbl5.CAT_ID;