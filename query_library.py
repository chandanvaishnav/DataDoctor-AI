# ============================================================
# DATADOCTOR AI
# 100 READY-MADE QUERY LIBRARY
# ============================================================


QUERY_LIBRARY = [

    # ========================================================
    # 1 - SALES & BASIC ANALYSIS
    # ========================================================

    {
        "id": 1,
        "category": "💰 Sales & Basic Analysis",
        "question": "What is the total sales?",
        "sql": """
SELECT ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
"""
    },

    {
        "id": 2,
        "category": "💰 Sales & Basic Analysis",
        "question": "What is the total profit?",
        "sql": """
SELECT ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
"""
    },

    {
        "id": 3,
        "category": "💰 Sales & Basic Analysis",
        "question": "What is the total quantity sold?",
        "sql": """
SELECT SUM(Quantity) AS Total_Quantity
FROM dataset
"""
    },

    {
        "id": 4,
        "category": "💰 Sales & Basic Analysis",
        "question": "What is the average sales?",
        "sql": """
SELECT ROUND(AVG(Sales), 2) AS Average_Sales
FROM dataset
"""
    },

    {
        "id": 5,
        "category": "💰 Sales & Basic Analysis",
        "question": "What is the average profit?",
        "sql": """
SELECT ROUND(AVG(Profit), 2) AS Average_Profit
FROM dataset
"""
    },

    {
        "id": 6,
        "category": "💰 Sales & Basic Analysis",
        "question": "What is the average discount?",
        "sql": """
SELECT ROUND(AVG(Discount), 2) AS Average_Discount
FROM dataset
"""
    },

    {
        "id": 7,
        "category": "💰 Sales & Basic Analysis",
        "question": "What is the highest sales value?",
        "sql": """
SELECT ROUND(MAX(Sales), 2) AS Highest_Sales
FROM dataset
"""
    },

    {
        "id": 8,
        "category": "💰 Sales & Basic Analysis",
        "question": "What is the lowest sales value?",
        "sql": """
SELECT ROUND(MIN(Sales), 2) AS Lowest_Sales
FROM dataset
"""
    },

    {
        "id": 9,
        "category": "💰 Sales & Basic Analysis",
        "question": "What is the highest profit?",
        "sql": """
SELECT ROUND(MAX(Profit), 2) AS Highest_Profit
FROM dataset
"""
    },

    {
        "id": 10,
        "category": "💰 Sales & Basic Analysis",
        "question": "What is the lowest profit?",
        "sql": """
SELECT ROUND(MIN(Profit), 2) AS Lowest_Profit
FROM dataset
"""
    },


    # ========================================================
    # 2 - CATEGORY ANALYSIS
    # ========================================================

    {
        "id": 11,
        "category": "📊 Category Analysis",
        "question": "What are the total sales by category?",
        "sql": """
SELECT Category,
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY Category
ORDER BY Total_Sales DESC
"""
    },

    {
        "id": 12,
        "category": "📊 Category Analysis",
        "question": "What is the total profit by category?",
        "sql": """
SELECT Category,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY Category
ORDER BY Total_Profit DESC
"""
    },

    {
        "id": 13,
        "category": "📊 Category Analysis",
        "question": "What is the average sales by category?",
        "sql": """
SELECT Category,
       ROUND(AVG(Sales), 2) AS Average_Sales
FROM dataset
GROUP BY Category
ORDER BY Average_Sales DESC
"""
    },

    {
        "id": 14,
        "category": "📊 Category Analysis",
        "question": "What is the average profit by category?",
        "sql": """
SELECT Category,
       ROUND(AVG(Profit), 2) AS Average_Profit
FROM dataset
GROUP BY Category
ORDER BY Average_Profit DESC
"""
    },

    {
        "id": 15,
        "category": "📊 Category Analysis",
        "question": "Which category has the highest sales?",
        "sql": """
SELECT Category,
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY Category
ORDER BY Total_Sales DESC
LIMIT 1
"""
    },

    {
        "id": 16,
        "category": "📊 Category Analysis",
        "question": "Which category has the lowest sales?",
        "sql": """
SELECT Category,
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY Category
ORDER BY Total_Sales ASC
LIMIT 1
"""
    },

    {
        "id": 17,
        "category": "📊 Category Analysis",
        "question": "Which category has the highest profit?",
        "sql": """
SELECT Category,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY Category
ORDER BY Total_Profit DESC
LIMIT 1
"""
    },

    {
        "id": 18,
        "category": "📊 Category Analysis",
        "question": "Which category has the lowest profit?",
        "sql": """
SELECT Category,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY Category
ORDER BY Total_Profit ASC
LIMIT 1
"""
    },

    {
        "id": 19,
        "category": "📊 Category Analysis",
        "question": "What is the quantity sold by category?",
        "sql": """
SELECT Category,
       SUM(Quantity) AS Total_Quantity
FROM dataset
GROUP BY Category
ORDER BY Total_Quantity DESC
"""
    },

    {
        "id": 20,
        "category": "📊 Category Analysis",
        "question": "What is the average discount by category?",
        "sql": """
SELECT Category,
       ROUND(AVG(Discount), 2) AS Average_Discount
FROM dataset
GROUP BY Category
ORDER BY Average_Discount DESC
"""
    },


    # ========================================================
    # 3 - SUB-CATEGORY ANALYSIS
    # ========================================================

    {
        "id": 21,
        "category": "📦 Sub-Category Analysis",
        "question": "What are the total sales by sub-category?",
        "sql": """
SELECT "Sub-Category",
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY "Sub-Category"
ORDER BY Total_Sales DESC
"""
    },

    {
        "id": 22,
        "category": "📦 Sub-Category Analysis",
        "question": "What are the total profit by sub-category?",
        "sql": """
SELECT "Sub-Category",
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY "Sub-Category"
ORDER BY Total_Profit DESC
"""
    },

    {
        "id": 23,
        "category": "📦 Sub-Category Analysis",
        "question": "What are the top 5 sub-categories by sales?",
        "sql": """
SELECT "Sub-Category",
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY "Sub-Category"
ORDER BY Total_Sales DESC
LIMIT 5
"""
    },

    {
        "id": 24,
        "category": "📦 Sub-Category Analysis",
        "question": "What are the top 10 sub-categories by sales?",
        "sql": """
SELECT "Sub-Category",
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY "Sub-Category"
ORDER BY Total_Sales DESC
LIMIT 10
"""
    },

    {
        "id": 25,
        "category": "📦 Sub-Category Analysis",
        "question": "What are the top 5 sub-categories by profit?",
        "sql": """
SELECT "Sub-Category",
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY "Sub-Category"
ORDER BY Total_Profit DESC
LIMIT 5
"""
    },

    {
        "id": 26,
        "category": "📦 Sub-Category Analysis",
        "question": "Which sub-category has the highest sales?",
        "sql": """
SELECT "Sub-Category",
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY "Sub-Category"
ORDER BY Total_Sales DESC
LIMIT 1
"""
    },

    {
        "id": 27,
        "category": "📦 Sub-Category Analysis",
        "question": "Which sub-category has the lowest sales?",
        "sql": """
SELECT "Sub-Category",
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY "Sub-Category"
ORDER BY Total_Sales ASC
LIMIT 1
"""
    },

    {
        "id": 28,
        "category": "📦 Sub-Category Analysis",
        "question": "Which sub-category has the highest profit?",
        "sql": """
SELECT "Sub-Category",
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY "Sub-Category"
ORDER BY Total_Profit DESC
LIMIT 1
"""
    },

    {
        "id": 29,
        "category": "📦 Sub-Category Analysis",
        "question": "Which sub-category has the lowest profit?",
        "sql": """
SELECT "Sub-Category",
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY "Sub-Category"
ORDER BY Total_Profit ASC
LIMIT 1
"""
    },

    {
        "id": 30,
        "category": "📦 Sub-Category Analysis",
        "question": "What is the quantity sold by sub-category?",
        "sql": """
SELECT "Sub-Category",
       SUM(Quantity) AS Total_Quantity
FROM dataset
GROUP BY "Sub-Category"
ORDER BY Total_Quantity DESC
"""
    },


    # ========================================================
    # 4 - REGION ANALYSIS
    # ========================================================

    {
        "id": 31,
        "category": "🌎 Region Analysis",
        "question": "What are the total sales by region?",
        "sql": """
SELECT Region,
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY Region
ORDER BY Total_Sales DESC
"""
    },

    {
        "id": 32,
        "category": "🌎 Region Analysis",
        "question": "What are the total profit by region?",
        "sql": """
SELECT Region,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY Region
ORDER BY Total_Profit DESC
"""
    },

    {
        "id": 33,
        "category": "🌎 Region Analysis",
        "question": "What is the average sales by region?",
        "sql": """
SELECT Region,
       ROUND(AVG(Sales), 2) AS Average_Sales
FROM dataset
GROUP BY Region
ORDER BY Average_Sales DESC
"""
    },

    {
        "id": 34,
        "category": "🌎 Region Analysis",
        "question": "What is the average profit by region?",
        "sql": """
SELECT Region,
       ROUND(AVG(Profit), 2) AS Average_Profit
FROM dataset
GROUP BY Region
ORDER BY Average_Profit DESC
"""
    },

    {
        "id": 35,
        "category": "🌎 Region Analysis",
        "question": "Which region has the highest sales?",
        "sql": """
SELECT Region,
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY Region
ORDER BY Total_Sales DESC
LIMIT 1
"""
    },

    {
        "id": 36,
        "category": "🌎 Region Analysis",
        "question": "Which region has the lowest sales?",
        "sql": """
SELECT Region,
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY Region
ORDER BY Total_Sales ASC
LIMIT 1
"""
    },

    {
        "id": 37,
        "category": "🌎 Region Analysis",
        "question": "Which region has the highest profit?",
        "sql": """
SELECT Region,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY Region
ORDER BY Total_Profit DESC
LIMIT 1
"""
    },

    {
        "id": 38,
        "category": "🌎 Region Analysis",
        "question": "Which region has the lowest profit?",
        "sql": """
SELECT Region,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY Region
ORDER BY Total_Profit ASC
LIMIT 1
"""
    },

    {
        "id": 39,
        "category": "🌎 Region Analysis",
        "question": "What is the quantity sold by region?",
        "sql": """
SELECT Region,
       SUM(Quantity) AS Total_Quantity
FROM dataset
GROUP BY Region
ORDER BY Total_Quantity DESC
"""
    },

    {
        "id": 40,
        "category": "🌎 Region Analysis",
        "question": "What is the average discount by region?",
        "sql": """
SELECT Region,
       ROUND(AVG(Discount), 2) AS Average_Discount
FROM dataset
GROUP BY Region
ORDER BY Average_Discount DESC
"""
    },


    # ========================================================
    # 5 - STATE ANALYSIS
    # ========================================================

    {
        "id": 41,
        "category": "📍 State Analysis",
        "question": "What are the top 5 states by sales?",
        "sql": """
SELECT State,
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY State
ORDER BY Total_Sales DESC
LIMIT 5
"""
    },

    {
        "id": 42,
        "category": "📍 State Analysis",
        "question": "What are the top 10 states by sales?",
        "sql": """
SELECT State,
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY State
ORDER BY Total_Sales DESC
LIMIT 10
"""
    },

    {
        "id": 43,
        "category": "📍 State Analysis",
        "question": "What are the top 5 states by profit?",
        "sql": """
SELECT State,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY State
ORDER BY Total_Profit DESC
LIMIT 5
"""
    },

    {
        "id": 44,
        "category": "📍 State Analysis",
        "question": "What are the bottom 5 states by sales?",
        "sql": """
SELECT State,
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY State
ORDER BY Total_Sales ASC
LIMIT 5
"""
    },

    {
        "id": 45,
        "category": "📍 State Analysis",
        "question": "Which state has the highest sales?",
        "sql": """
SELECT State,
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY State
ORDER BY Total_Sales DESC
LIMIT 1
"""
    },

    {
        "id": 46,
        "category": "📍 State Analysis",
        "question": "Which state has the lowest sales?",
        "sql": """
SELECT State,
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY State
ORDER BY Total_Sales ASC
LIMIT 1
"""
    },

    {
        "id": 47,
        "category": "📍 State Analysis",
        "question": "Which state has the highest profit?",
        "sql": """
SELECT State,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY State
ORDER BY Total_Profit DESC
LIMIT 1
"""
    },

    {
        "id": 48,
        "category": "📍 State Analysis",
        "question": "Which state has the lowest profit?",
        "sql": """
SELECT State,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY State
ORDER BY Total_Profit ASC
LIMIT 1
"""
    },

    {
        "id": 49,
        "category": "📍 State Analysis",
        "question": "What are the total sales by state?",
        "sql": """
SELECT State,
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY State
ORDER BY Total_Sales DESC
"""
    },

    {
        "id": 50,
        "category": "📍 State Analysis",
        "question": "What are the total profit by state?",
        "sql": """
SELECT State,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY State
ORDER BY Total_Profit DESC
"""
    },


    # ========================================================
    # 6 - CITY ANALYSIS
    # ========================================================

    {
        "id": 51,
        "category": "🏙 City Analysis",
        "question": "What are the top 5 cities by sales?",
        "sql": """
SELECT City,
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY City
ORDER BY Total_Sales DESC
LIMIT 5
"""
    },

    {
        "id": 52,
        "category": "🏙 City Analysis",
        "question": "What are the top 10 cities by sales?",
        "sql": """
SELECT City,
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY City
ORDER BY Total_Sales DESC
LIMIT 10
"""
    },

    {
        "id": 53,
        "category": "🏙 City Analysis",
        "question": "What are the top 5 cities by profit?",
        "sql": """
SELECT City,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY City
ORDER BY Total_Profit DESC
LIMIT 5
"""
    },

    {
        "id": 54,
        "category": "🏙 City Analysis",
        "question": "What are the bottom 5 cities by sales?",
        "sql": """
SELECT City,
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY City
ORDER BY Total_Sales ASC
LIMIT 5
"""
    },

    {
        "id": 55,
        "category": "🏙 City Analysis",
        "question": "Which city has the highest sales?",
        "sql": """
SELECT City,
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY City
ORDER BY Total_Sales DESC
LIMIT 1
"""
    },

    {
        "id": 56,
        "category": "🏙 City Analysis",
        "question": "Which city has the lowest sales?",
        "sql": """
SELECT City,
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY City
ORDER BY Total_Sales ASC
LIMIT 1
"""
    },

    {
        "id": 57,
        "category": "🏙 City Analysis",
        "question": "Which city has the highest profit?",
        "sql": """
SELECT City,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY City
ORDER BY Total_Profit DESC
LIMIT 1
"""
    },

    {
        "id": 58,
        "category": "🏙 City Analysis",
        "question": "Which city has the lowest profit?",
        "sql": """
SELECT City,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY City
ORDER BY Total_Profit ASC
LIMIT 1
"""
    },

    {
        "id": 59,
        "category": "🏙 City Analysis",
        "question": "What are the total sales by city?",
        "sql": """
SELECT City,
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY City
ORDER BY Total_Sales DESC
"""
    },

    {
        "id": 60,
        "category": "🏙 City Analysis",
        "question": "What are the total profit by city?",
        "sql": """
SELECT City,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY City
ORDER BY Total_Profit DESC
"""
    },


    # ========================================================
    # 7 - SEGMENT ANALYSIS
    # ========================================================

    {
        "id": 61,
        "category": "👥 Segment Analysis",
        "question": "What are the total sales by segment?",
        "sql": """
SELECT Segment,
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY Segment
ORDER BY Total_Sales DESC
"""
    },

    {
        "id": 62,
        "category": "👥 Segment Analysis",
        "question": "What are the total profit by segment?",
        "sql": """
SELECT Segment,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY Segment
ORDER BY Total_Profit DESC
"""
    },

    {
        "id": 63,
        "category": "👥 Segment Analysis",
        "question": "What is the average sales by segment?",
        "sql": """
SELECT Segment,
       ROUND(AVG(Sales), 2) AS Average_Sales
FROM dataset
GROUP BY Segment
ORDER BY Average_Sales DESC
"""
    },

    {
        "id": 64,
        "category": "👥 Segment Analysis",
        "question": "What is the average profit by segment?",
        "sql": """
SELECT Segment,
       ROUND(AVG(Profit), 2) AS Average_Profit
FROM dataset
GROUP BY Segment
ORDER BY Average_Profit DESC
"""
    },

    {
        "id": 65,
        "category": "👥 Segment Analysis",
        "question": "Which segment has the highest sales?",
        "sql": """
SELECT Segment,
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY Segment
ORDER BY Total_Sales DESC
LIMIT 1
"""
    },

    {
        "id": 66,
        "category": "👥 Segment Analysis",
        "question": "Which segment has the highest profit?",
        "sql": """
SELECT Segment,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY Segment
ORDER BY Total_Profit DESC
LIMIT 1
"""
    },

    {
        "id": 67,
        "category": "👥 Segment Analysis",
        "question": "Which segment has the lowest sales?",
        "sql": """
SELECT Segment,
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY Segment
ORDER BY Total_Sales ASC
LIMIT 1
"""
    },

    {
        "id": 68,
        "category": "👥 Segment Analysis",
        "question": "Which segment has the lowest profit?",
        "sql": """
SELECT Segment,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY Segment
ORDER BY Total_Profit ASC
LIMIT 1
"""
    },

    {
        "id": 69,
        "category": "👥 Segment Analysis",
        "question": "What is the quantity sold by segment?",
        "sql": """
SELECT Segment,
       SUM(Quantity) AS Total_Quantity
FROM dataset
GROUP BY Segment
ORDER BY Total_Quantity DESC
"""
    },

    {
        "id": 70,
        "category": "👥 Segment Analysis",
        "question": "What is the average discount by segment?",
        "sql": """
SELECT Segment,
       ROUND(AVG(Discount), 2) AS Average_Discount
FROM dataset
GROUP BY Segment
ORDER BY Average_Discount DESC
"""
    },


    # ========================================================
    # 8 - SHIP MODE ANALYSIS
    # ========================================================

    {
        "id": 71,
        "category": "🚚 Ship Mode Analysis",
        "question": "What are the total sales by ship mode?",
        "sql": """
SELECT "Ship Mode",
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY "Ship Mode"
ORDER BY Total_Sales DESC
"""
    },

    {
        "id": 72,
        "category": "🚚 Ship Mode Analysis",
        "question": "What are the total profit by ship mode?",
        "sql": """
SELECT "Ship Mode",
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY "Ship Mode"
ORDER BY Total_Profit DESC
"""
    },

    {
        "id": 73,
        "category": "🚚 Ship Mode Analysis",
        "question": "What is the average sales by ship mode?",
        "sql": """
SELECT "Ship Mode",
       ROUND(AVG(Sales), 2) AS Average_Sales
FROM dataset
GROUP BY "Ship Mode"
ORDER BY Average_Sales DESC
"""
    },

    {
        "id": 74,
        "category": "🚚 Ship Mode Analysis",
        "question": "What is the average profit by ship mode?",
        "sql": """
SELECT "Ship Mode",
       ROUND(AVG(Profit), 2) AS Average_Profit
FROM dataset
GROUP BY "Ship Mode"
ORDER BY Average_Profit DESC
"""
    },

    {
        "id": 75,
        "category": "🚚 Ship Mode Analysis",
        "question": "Which ship mode has the highest sales?",
        "sql": """
SELECT "Ship Mode",
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY "Ship Mode"
ORDER BY Total_Sales DESC
LIMIT 1
"""
    },

    {
        "id": 76,
        "category": "🚚 Ship Mode Analysis",
        "question": "Which ship mode has the highest profit?",
        "sql": """
SELECT "Ship Mode",
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY "Ship Mode"
ORDER BY Total_Profit DESC
LIMIT 1
"""
    },

    {
        "id": 77,
        "category": "🚚 Ship Mode Analysis",
        "question": "Which ship mode has the lowest sales?",
        "sql": """
SELECT "Ship Mode",
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY "Ship Mode"
ORDER BY Total_Sales ASC
LIMIT 1
"""
    },

    {
        "id": 78,
        "category": "🚚 Ship Mode Analysis",
        "question": "Which ship mode has the lowest profit?",
        "sql": """
SELECT "Ship Mode",
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY "Ship Mode"
ORDER BY Total_Profit ASC
LIMIT 1
"""
    },

    {
        "id": 79,
        "category": "🚚 Ship Mode Analysis",
        "question": "What is the quantity sold by ship mode?",
        "sql": """
SELECT "Ship Mode",
       SUM(Quantity) AS Total_Quantity
FROM dataset
GROUP BY "Ship Mode"
ORDER BY Total_Quantity DESC
"""
    },

    {
        "id": 80,
        "category": "🚚 Ship Mode Analysis",
        "question": "What is the average discount by ship mode?",
        "sql": """
SELECT "Ship Mode",
       ROUND(AVG(Discount), 2) AS Average_Discount
FROM dataset
GROUP BY "Ship Mode"
ORDER BY Average_Discount DESC
"""
    },


    # ========================================================
    # 9 - DISCOUNT & PROFIT
    # ========================================================

    {
        "id": 81,
        "category": "📉 Discount & Profit",
        "question": "What is the average discount by category?",
        "sql": """
SELECT Category,
       ROUND(AVG(Discount), 2) AS Average_Discount
FROM dataset
GROUP BY Category
ORDER BY Average_Discount DESC
"""
    },

    {
        "id": 82,
        "category": "📉 Discount & Profit",
        "question": "What is the average discount by region?",
        "sql": """
SELECT Region,
       ROUND(AVG(Discount), 2) AS Average_Discount
FROM dataset
GROUP BY Region
ORDER BY Average_Discount DESC
"""
    },

    {
        "id": 83,
        "category": "📉 Discount & Profit",
        "question": "What is the average discount by segment?",
        "sql": """
SELECT Segment,
       ROUND(AVG(Discount), 2) AS Average_Discount
FROM dataset
GROUP BY Segment
ORDER BY Average_Discount DESC
"""
    },

    {
        "id": 84,
        "category": "📉 Discount & Profit",
        "question": "What is the average discount by sub-category?",
        "sql": """
SELECT "Sub-Category",
       ROUND(AVG(Discount), 2) AS Average_Discount
FROM dataset
GROUP BY "Sub-Category"
ORDER BY Average_Discount DESC
"""
    },

    {
        "id": 85,
        "category": "📉 Discount & Profit",
        "question": "Which category has the highest average discount?",
        "sql": """
SELECT Category,
       ROUND(AVG(Discount), 2) AS Average_Discount
FROM dataset
GROUP BY Category
ORDER BY Average_Discount DESC
LIMIT 1
"""
    },

    {
        "id": 86,
        "category": "📉 Discount & Profit",
        "question": "Which region has the highest average discount?",
        "sql": """
SELECT Region,
       ROUND(AVG(Discount), 2) AS Average_Discount
FROM dataset
GROUP BY Region
ORDER BY Average_Discount DESC
LIMIT 1
"""
    },

    {
        "id": 87,
        "category": "📉 Discount & Profit",
        "question": "Which segment has the highest average discount?",
        "sql": """
SELECT Segment,
       ROUND(AVG(Discount), 2) AS Average_Discount
FROM dataset
GROUP BY Segment
ORDER BY Average_Discount DESC
LIMIT 1
"""
    },

    {
        "id": 88,
        "category": "📉 Discount & Profit",
        "question": "Which sub-category has the highest average discount?",
        "sql": """
SELECT "Sub-Category",
       ROUND(AVG(Discount), 2) AS Average_Discount
FROM dataset
GROUP BY "Sub-Category"
ORDER BY Average_Discount DESC
LIMIT 1
"""
    },

    {
        "id": 89,
        "category": "📉 Discount & Profit",
        "question": "Which sub-categories have negative profit?",
        "sql": """
SELECT "Sub-Category",
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY "Sub-Category"
HAVING Total_Profit < 0
ORDER BY Total_Profit ASC
"""
    },

    {
        "id": 90,
        "category": "📉 Discount & Profit",
        "question": "Which categories have negative profit?",
        "sql": """
SELECT Category,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY Category
HAVING Total_Profit < 0
ORDER BY Total_Profit ASC
"""
    },


    # ========================================================
    # 10 - ADVANCED ANALYSIS
    # ========================================================

    {
        "id": 91,
        "category": "🔬 Advanced Analysis",
        "question": "What are the top 10 products by sales?",
        "sql": """
SELECT "Product Name",
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY "Product Name"
ORDER BY Total_Sales DESC
LIMIT 10
"""
    },

    {
        "id": 92,
        "category": "🔬 Advanced Analysis",
        "question": "What are the top 10 products by profit?",
        "sql": """
SELECT "Product Name",
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY "Product Name"
ORDER BY Total_Profit DESC
LIMIT 10
"""
    },

    {
        "id": 93,
        "category": "🔬 Advanced Analysis",
        "question": "What are the bottom 10 products by profit?",
        "sql": """
SELECT "Product Name",
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY "Product Name"
ORDER BY Total_Profit ASC
LIMIT 10
"""
    },

    {
        "id": 94,
        "category": "🔬 Advanced Analysis",
        "question": "Which products have negative profit?",
        "sql": """
SELECT "Product Name",
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY "Product Name"
HAVING Total_Profit < 0
ORDER BY Total_Profit ASC
"""
    },

    {
        "id": 95,
        "category": "🔬 Advanced Analysis",
        "question": "Which products have sales greater than 1000?",
        "sql": """
SELECT "Product Name",
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY "Product Name"
HAVING Total_Sales > 1000
ORDER BY Total_Sales DESC
"""
    },

    {
        "id": 96,
        "category": "🔬 Advanced Analysis",
        "question": "Which cities have sales greater than 10000?",
        "sql": """
SELECT City,
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY City
HAVING Total_Sales > 10000
ORDER BY Total_Sales DESC
"""
    },

    {
        "id": 97,
        "category": "🔬 Advanced Analysis",
        "question": "Which states have profit greater than 5000?",
        "sql": """
SELECT State,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY State
HAVING Total_Profit > 5000
ORDER BY Total_Profit DESC
"""
    },

    {
        "id": 98,
        "category": "🔬 Advanced Analysis",
        "question": "What are the top 10 cities by profit?",
        "sql": """
SELECT City,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY City
ORDER BY Total_Profit DESC
LIMIT 10
"""
    },

    {
        "id": 99,
        "category": "🔬 Advanced Analysis",
        "question": "What are the top 10 states by profit?",
        "sql": """
SELECT State,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY State
ORDER BY Total_Profit DESC
LIMIT 10
"""
    },

    {
        "id": 100,
        "category": "🔬 Advanced Analysis",
        "question": "Show the sales, quantity, discount, and profit summary.",
        "sql": """
SELECT
    ROUND(SUM(Sales), 2) AS Total_Sales,
    SUM(Quantity) AS Total_Quantity,
    ROUND(AVG(Discount), 2) AS Average_Discount,
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
"""
    }
]


# ============================================================
# FUNCTIONS
# ============================================================

def get_all_questions():
    return QUERY_LIBRARY


def get_categories():

    categories = []

    for item in QUERY_LIBRARY:

        if item["category"] not in categories:

            categories.append(
                item["category"]
            )

    return categories


def get_questions_by_category(category):

    return [
        item
        for item in QUERY_LIBRARY
        if item["category"] == category
    ]


def get_query_by_question(question):

    question = question.strip().lower()

    for item in QUERY_LIBRARY:

        if item["question"].lower() == question:

            return item

    return None


def search_questions(text):

    text = text.strip().lower()

    if not text:
        return []

    words = text.split()

    matches = []

    for item in QUERY_LIBRARY:

        question = item["question"].lower()

        score = 0

        if text in question:
            score += 100

        for word in words:

            if word in question:
                score += 10

        if score > 0:

            matches.append(
                (score, item)
            )

    matches.sort(
        key=lambda x: (
            -x[0],
            x[1]["id"]
        )
    )

    return [
        item
        for _, item in matches
    ]


# Make sure exactly 100 queries exist
if len(QUERY_LIBRARY) != 100:

    raise ValueError(
        f"Query library must contain exactly 100 queries. "
        f"Found {len(QUERY_LIBRARY)}."
    )