import re
import pandas as pd


# ============================================================
# SQL SAFETY
# ============================================================

def validate_sql(sql):

    if not sql:
        return False, "SQL query is empty."

    cleaned = sql.strip().upper()

    # Only SELECT queries
    if not cleaned.startswith("SELECT"):

        return (
            False,
            "Only SELECT queries are allowed."
        )

    dangerous_commands = [
        "DROP ",
        "DELETE ",
        "UPDATE ",
        "INSERT ",
        "ALTER ",
        "CREATE ",
        "REPLACE ",
        "ATTACH ",
        "DETACH ",
        "PRAGMA ",
        "VACUUM ",
        "TRUNCATE "
    ]

    for command in dangerous_commands:

        if command in cleaned:

            return (
                False,
                f"Unsafe SQL command detected: {command.strip()}"
            )

    return True, "SQL query passed the safety check."


# ============================================================
# CUSTOM QUESTION → SQL
# ============================================================

def generate_sql_from_question(question):

    q = question.lower().strip()

    # --------------------------------------------------------
    # TOTAL SALES
    # --------------------------------------------------------

    if (
        "total sales" in q
        and "category" not in q
        and "region" not in q
        and "city" not in q
        and "state" not in q
        and "segment" not in q
        and "sub-category" not in q
        and "sub category" not in q
    ):

        return """
SELECT ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
"""

    # --------------------------------------------------------
    # TOTAL PROFIT
    # --------------------------------------------------------

    if (
        "total profit" in q
        and "category" not in q
        and "region" not in q
        and "city" not in q
        and "state" not in q
        and "segment" not in q
    ):

        return """
SELECT ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
"""

    # --------------------------------------------------------
    # TOTAL QUANTITY
    # --------------------------------------------------------

    if (
        "total quantity" in q
        or "total units" in q
        or "quantity sold" in q
    ):

        return """
SELECT SUM(Quantity) AS Total_Quantity
FROM dataset
"""

    # --------------------------------------------------------
    # AVERAGE SALES
    # --------------------------------------------------------

    if (
        "average sales" in q
        and "category" not in q
        and "region" not in q
        and "city" not in q
        and "state" not in q
    ):

        return """
SELECT ROUND(AVG(Sales), 2) AS Average_Sales
FROM dataset
"""

    # --------------------------------------------------------
    # AVERAGE PROFIT
    # --------------------------------------------------------

    if (
        "average profit" in q
        and "category" not in q
        and "region" not in q
        and "city" not in q
        and "state" not in q
    ):

        return """
SELECT ROUND(AVG(Profit), 2) AS Average_Profit
FROM dataset
"""

    # --------------------------------------------------------
    # AVERAGE DISCOUNT
    # --------------------------------------------------------

    if (
        "average discount" in q
        and "category" not in q
        and "region" not in q
        and "segment" not in q
        and "ship mode" not in q
        and "sub-category" not in q
    ):

        return """
SELECT ROUND(AVG(Discount), 2) AS Average_Discount
FROM dataset
"""

    # --------------------------------------------------------
    # SALES BY CATEGORY
    # --------------------------------------------------------

    if (
        "sales by category" in q
        or "category sales" in q
    ):

        return """
SELECT Category,
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY Category
ORDER BY Total_Sales DESC
"""

    # --------------------------------------------------------
    # PROFIT BY CATEGORY
    # --------------------------------------------------------

    if (
        "profit by category" in q
        or "category profit" in q
    ):

        return """
SELECT Category,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY Category
ORDER BY Total_Profit DESC
"""

    # --------------------------------------------------------
    # SALES BY REGION
    # --------------------------------------------------------

    if (
        "sales by region" in q
        or "region sales" in q
    ):

        return """
SELECT Region,
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY Region
ORDER BY Total_Sales DESC
"""

    # --------------------------------------------------------
    # PROFIT BY REGION
    # --------------------------------------------------------

    if (
        "profit by region" in q
        or "region profit" in q
    ):

        return """
SELECT Region,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY Region
ORDER BY Total_Profit DESC
"""

    # --------------------------------------------------------
    # SALES BY CITY
    # --------------------------------------------------------

    if (
        "sales by city" in q
        or "city sales" in q
    ):

        return """
SELECT City,
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY City
ORDER BY Total_Sales DESC
"""

    # --------------------------------------------------------
    # PROFIT BY CITY
    # --------------------------------------------------------

    if (
        "profit by city" in q
        or "city profit" in q
    ):

        return """
SELECT City,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY City
ORDER BY Total_Profit DESC
"""

    # --------------------------------------------------------
    # SALES BY STATE
    # --------------------------------------------------------

    if (
        "sales by state" in q
        or "state sales" in q
    ):

        return """
SELECT State,
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY State
ORDER BY Total_Sales DESC
"""

    # --------------------------------------------------------
    # PROFIT BY STATE
    # --------------------------------------------------------

    if (
        "profit by state" in q
        or "state profit" in q
    ):

        return """
SELECT State,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY State
ORDER BY Total_Profit DESC
"""

    # --------------------------------------------------------
    # TOP 5 CITIES BY PROFIT
    # --------------------------------------------------------

    if (
        "top 5 cities" in q
        and "profit" in q
    ):

        return """
SELECT City,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY City
ORDER BY Total_Profit DESC
LIMIT 5
"""

    # --------------------------------------------------------
    # TOP 5 CITIES BY SALES
    # --------------------------------------------------------

    if "top 5 cities" in q:

        return """
SELECT City,
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY City
ORDER BY Total_Sales DESC
LIMIT 5
"""

    # --------------------------------------------------------
    # TOP 10 CITIES
    # --------------------------------------------------------

    if "top 10 cities" in q:

        return """
SELECT City,
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY City
ORDER BY Total_Sales DESC
LIMIT 10
"""

    # --------------------------------------------------------
    # TOP 5 STATES
    # --------------------------------------------------------

    if (
        "top 5 states" in q
        and "profit" in q
    ):

        return """
SELECT State,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY State
ORDER BY Total_Profit DESC
LIMIT 5
"""

    if "top 5 states" in q:

        return """
SELECT State,
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY State
ORDER BY Total_Sales DESC
LIMIT 5
"""

    # --------------------------------------------------------
    # TOP 10 STATES
    # --------------------------------------------------------

    if "top 10 states" in q:

        return """
SELECT State,
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY State
ORDER BY Total_Sales DESC
LIMIT 10
"""

    # --------------------------------------------------------
    # TOP 5 SUB-CATEGORIES
    # --------------------------------------------------------

    if (
        "top 5 sub-categories" in q
        and "profit" in q
    ):

        return """
SELECT "Sub-Category",
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY "Sub-Category"
ORDER BY Total_Profit DESC
LIMIT 5
"""

    if (
        "top 5 sub-categories" in q
        or "top 5 sub categories" in q
    ):

        return """
SELECT "Sub-Category",
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY "Sub-Category"
ORDER BY Total_Sales DESC
LIMIT 5
"""

    # --------------------------------------------------------
    # TOP 10 SUB-CATEGORIES
    # --------------------------------------------------------

    if (
        "top 10 sub-categories" in q
        or "top 10 sub categories" in q
    ):

        return """
SELECT "Sub-Category",
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY "Sub-Category"
ORDER BY Total_Sales DESC
LIMIT 10
"""

    # --------------------------------------------------------
    # TOP 10 PRODUCTS
    # --------------------------------------------------------

    if "top 10 products" in q:

        if "profit" in q:

            return """
SELECT "Product Name",
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY "Product Name"
ORDER BY Total_Profit DESC
LIMIT 10
"""

        return """
SELECT "Product Name",
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY "Product Name"
ORDER BY Total_Sales DESC
LIMIT 10
"""

    # --------------------------------------------------------
    # HIGHEST CATEGORY
    # --------------------------------------------------------

    if (
        "category" in q
        and "highest" in q
        and "sales" in q
    ):

        return """
SELECT Category,
       ROUND(SUM(Sales), 2) AS Total_Sales
FROM dataset
GROUP BY Category
ORDER BY Total_Sales DESC
LIMIT 1
"""

    # --------------------------------------------------------
    # HIGHEST PROFIT CATEGORY
    # --------------------------------------------------------

    if (
        "category" in q
        and "highest" in q
        and "profit" in q
    ):

        return """
SELECT Category,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM dataset
GROUP BY Category
ORDER BY Total_Profit DESC
LIMIT 1
"""

    return None


# ============================================================
# ANSWER GENERATION
# ============================================================

def generate_answer(result):

    if result is None or result.empty:

        return (
            "No matching records were found."
        )

    if (
        len(result) == 1
        and len(result.columns) == 1
    ):

        value = result.iloc[0, 0]

        column = result.columns[0]

        return (
            f"**{column}:** {value}"
        )

    if len(result) == 1:

        parts = []

        for column in result.columns:

            value = result.iloc[0][column]

            parts.append(
                f"**{column}:** {value}"
            )

        return " | ".join(parts)

    return (
        f"The query returned **{len(result)} records**. "
        "See the table and visualization below."
    )


# ============================================================
# INSIGHT GENERATION
# ============================================================

def generate_insight(result):

    if result is None or result.empty:

        return "There is no data available to generate an insight."

    numeric_columns = (
        result.select_dtypes(
            include="number"
        ).columns.tolist()
    )

    if not numeric_columns:

        return (
            "The result contains categorical data "
            "that can be explored in the table."
        )

    if len(result) == 1:

        return (
            "This query returned a summarized result "
            "from the dataset."
        )

    value_column = numeric_columns[-1]

    try:

        highest_index = result[
            value_column
        ].idxmax()

        lowest_index = result[
            value_column
        ].idxmin()

        highest_value = result.loc[
            highest_index,
            value_column
        ]

        lowest_value = result.loc[
            lowest_index,
            value_column
        ]

        categorical_columns = [
            col
            for col in result.columns
            if col not in numeric_columns
        ]

        if categorical_columns:

            category = categorical_columns[0]

            highest_name = result.loc[
                highest_index,
                category
            ]

            lowest_name = result.loc[
                lowest_index,
                category
            ]

            return (
                f"**{highest_name}** has the highest "
                f"{value_column} at **{highest_value}**, "
                f"while **{lowest_name}** has the lowest "
                f"at **{lowest_value}**."
            )

    except Exception:
        pass

    return (
        "The result provides a comparison across "
        "the selected records."
    )


# ============================================================
# FORMAT RESULT
# ============================================================

def format_result_for_history(result):

    if result is None:

        return ""

    if result.empty:

        return "No results"

    return result.to_csv(
        index=False
    )