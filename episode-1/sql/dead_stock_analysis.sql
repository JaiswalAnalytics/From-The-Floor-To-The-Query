-- =====================================================================
-- From the Floor to the Query | Episode 1: Dead Stock Detector
-- Dialect: PostgreSQL / DuckDB. For Snowflake or SQL Server, swap the
-- date subtraction for DATEDIFF('day', start, end).
-- Tables: products(sku, product_name, category, cost_price, stock_qty)
--         sales(sku, sale_date, qty)
-- =====================================================================
WITH params AS (
    SELECT DATE '2026-09-30' AS as_of          -- one place to change the "today" date
),
sales_summary AS (                              -- one row per SKU that has ever sold
    SELECT
        s.sku,
        MAX(s.sale_date) AS last_sale_date,
        SUM(CASE WHEN s.sale_date > p.as_of - 90 THEN s.qty ELSE 0 END) AS qty_90d
    FROM sales s
    CROSS JOIN params p
    WHERE s.sale_date <= p.as_of
    GROUP BY s.sku
),
stock_status AS (                               -- every SKU, sold or not
    SELECT
        pr.sku, pr.product_name, pr.category, pr.stock_qty,
        pr.stock_qty * pr.cost_price                          AS stock_value,
        p.as_of - ss.last_sale_date                           AS days_since_sale,
        ROUND(pr.stock_qty / NULLIF(ss.qty_90d / 90.0, 0), 0) AS days_of_cover
    FROM products pr
    CROSS JOIN params p
    LEFT JOIN sales_summary ss ON ss.sku = pr.sku
),
classified AS (
    SELECT *,
        CASE
            WHEN days_since_sale IS NULL OR days_since_sale > 90 THEN 'Dead'
            WHEN days_since_sale > 60 OR days_of_cover > 180     THEN 'Slow'
            ELSE 'Moving'
        END AS status
    FROM stock_status
)

-- QUERY A: the dead stock list with a running share of trapped rupees
SELECT
    sku, product_name, stock_qty, stock_value, days_since_sale,
    ROUND(100.0 * SUM(stock_value) OVER (ORDER BY stock_value DESC, sku)
                / SUM(stock_value) OVER (), 1) AS cum_pct_of_dead_value
FROM classified
WHERE status = 'Dead'
ORDER BY stock_value DESC;

-- QUERY B (swap in for A): rupees by status
-- SELECT status, COUNT(*) AS skus, SUM(stock_value) AS stock_value,
--        ROUND(100.0 * SUM(stock_value) / SUM(SUM(stock_value)) OVER (), 1) AS pct_of_stock
-- FROM classified GROUP BY status ORDER BY stock_value DESC;
