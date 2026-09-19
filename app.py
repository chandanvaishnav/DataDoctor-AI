import io
import os
import re
import sqlite3
from datetime import datetime

import pandas as pd
import streamlit as st

# ============================================================
# OPTIONAL VOICE PACKAGES
# ============================================================

try:
    from streamlit_mic_recorder import mic_recorder
    VOICE_AVAILABLE = True
except Exception:
    VOICE_AVAILABLE = False

try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except Exception:
    SPEECH_AVAILABLE = False


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="DataDoctor AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 0px;
}

.subtitle {
    font-size: 18px;
    color: #777;
    margin-bottom: 25px;
}

.card {
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #ddd;
    margin-bottom: 15px;
}

.question-card {
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #ddd;
    margin-bottom: 5px;
}

.history-card {
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #ddd;
    margin-bottom: 12px;
}

.small-text {
    font-size: 13px;
    color: #777;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "df" not in st.session_state:
    st.session_state.df = None

if "dataset_name" not in st.session_state:
    st.session_state.dataset_name = ""

if "db_ready" not in st.session_state:
    st.session_state.db_ready = False

if "question_input" not in st.session_state:
    st.session_state.question_input = ""

if "history" not in st.session_state:
    st.session_state.history = []

if "conversation_active" not in st.session_state:
    st.session_state.conversation_active = True

if "cleaned_df" not in st.session_state:
    st.session_state.cleaned_df = None


# ============================================================
# CONSTANTS
# ============================================================

DB_FILE = "datadoctor.db"

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DEFAULT_CSV = os.path.join(DATA_DIR, "SampleSuperstore.csv")


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_column_name(name):
    """Convert dataframe column names into safe SQLite column names."""
    name = str(name).strip()
    name = name.replace("\n", " ")
    name = re.sub(r"\s+", " ", name)
    return name


def load_file(uploaded_file):
    """Load CSV or Excel file."""
    try:
        filename = uploaded_file.name.lower()

        if filename.endswith(".csv"):
            return pd.read_csv(uploaded_file)

        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            return pd.read_excel(uploaded_file)

        st.error("Please upload a CSV or Excel file.")
        return None

    except Exception as e:
        st.error(f"Could not read file: {e}")
        return None


def load_default_dataset():
    """Load SampleSuperstore.csv if available."""
    if os.path.exists(DEFAULT_CSV):
        try:
            return pd.read_csv(DEFAULT_CSV)
        except Exception as e:
            st.error(f"Could not load default dataset: {e}")

    return None


def clean_dataframe(df):
    """Basic automatic cleaning."""
    cleaned = df.copy()

    # Clean column names
    cleaned.columns = [clean_column_name(c) for c in cleaned.columns]

    # Remove completely empty rows
    cleaned = cleaned.dropna(how="all")

    # Remove duplicate rows
    cleaned = cleaned.drop_duplicates()

    # Strip strings
    for col in cleaned.select_dtypes(include="object").columns:
        cleaned[col] = cleaned[col].apply(
            lambda x: x.strip() if isinstance(x, str) else x
        )

    # Try numeric conversion for numeric-looking columns
    for col in cleaned.columns:
        if cleaned[col].dtype == "object":
            converted = pd.to_numeric(cleaned[col], errors="coerce")

            if converted.notna().mean() > 0.90:
                cleaned[col] = converted

    return cleaned


def quality_report(df):
    """Return data quality information."""
    total_cells = df.shape[0] * df.shape[1]

    missing_cells = int(df.isna().sum().sum())

    duplicate_rows = int(df.duplicated().sum())

    missing_percent = (
        (missing_cells / total_cells) * 100
        if total_cells > 0
        else 0
    )

    quality_score = 100

    if total_cells > 0:
        quality_score -= min(40, missing_percent)

    if len(df) > 0:
        duplicate_percent = (duplicate_rows / len(df)) * 100
        quality_score -= min(30, duplicate_percent)

    quality_score = max(0, round(quality_score, 2))

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "missing": missing_cells,
        "duplicates": duplicate_rows,
        "missing_percent": round(missing_percent, 2),
        "quality_score": quality_score
    }


def create_database(df):
    """Create SQLite database."""
    try:
        conn = sqlite3.connect(DB_FILE)

        db_df = df.copy()

        # SQLite-friendly column names
        db_df.columns = [clean_column_name(c) for c in db_df.columns]

        db_df.to_sql(
            "data",
            conn,
            if_exists="replace",
            index=False
        )

        conn.commit()
        conn.close()

        return True

    except Exception as e:
        st.error(f"Database error: {e}")
        return False


def execute_sql(sql):
    """Execute SELECT query safely."""
    try:
        conn = sqlite3.connect(DB_FILE)

        result = pd.read_sql_query(sql, conn)

        conn.close()

        return result, None

    except Exception as e:
        return None, str(e)


def validate_sql(sql):
    """Basic SQL safety validation."""
    if not sql:
        return False, "Empty SQL query."

    sql_clean = sql.strip().lower()

    if not sql_clean.startswith("select"):
        return False, "Only SELECT queries are allowed."

    forbidden = [
        "insert ",
        "update ",
        "delete ",
        "drop ",
        "alter ",
        "create ",
        "replace ",
        "truncate ",
        "attach ",
        "detach ",
        "pragma ",
        "vacuum "
    ]

    for word in forbidden:
        if word in sql_clean:
            return False, f"Unsafe SQL operation detected: {word.strip()}"

    return True, "SQL is safe."


def format_money(value):
    try:
        return f"₹{float(value):,.2f}"
    except Exception:
        return str(value)


def detect_numeric_columns(df):
    return list(df.select_dtypes(include="number").columns)


def make_insight(question, result):
    """Generate a simple automatic insight."""
    if result is None or result.empty:
        return "No matching data was found."

    numeric_cols = detect_numeric_columns(result)

    if not numeric_cols:
        return f"The query returned {len(result)} result(s)."

    if len(result) == 1:
        parts = []

        for col in result.columns:
            value = result.iloc[0][col]

            if pd.isna(value):
                continue

            if isinstance(value, (int, float)) and (
                "sales" in col.lower()
                or "profit" in col.lower()
            ):
                value = format_money(value)

            parts.append(f"{col}: {value}")

        return " | ".join(parts)

    first_numeric = numeric_cols[0]

    try:
        max_index = result[first_numeric].idxmax()
        max_row = result.loc[max_index]

        label_cols = [
            c for c in result.columns
            if c != first_numeric
        ]

        if label_cols:
            label = max_row[label_cols[0]]
            value = max_row[first_numeric]

            if (
                "sales" in first_numeric.lower()
                or "profit" in first_numeric.lower()
            ):
                value = format_money(value)

            return (
                f"Highest {first_numeric}: "
                f"{label} with {value}."
            )

    except Exception:
        pass

    return f"The query returned {len(result)} rows."


def generate_answer(question, result):
    """Generate human-readable answer."""
    if result is None:
        return "Unable to generate an answer."

    if result.empty:
        return "I could not find any matching records."

    if len(result) == 1:
        row = result.iloc[0]

        if len(result.columns) == 1:
            value = row.iloc[0]

            if isinstance(value, (int, float)):
                col = result.columns[0]

                if (
                    "sales" in col.lower()
                    or "profit" in col.lower()
                ):
                    return format_money(value)

                return f"{value:,.2f}"

            return str(value)

        parts = []

        for col in result.columns:
            value = row[col]

            if pd.isna(value):
                continue

            if (
                isinstance(value, (int, float))
                and (
                    "sales" in col.lower()
                    or "profit" in col.lower()
                )
            ):
                value = format_money(value)

            parts.append(f"{col}: {value}")

        return " | ".join(parts)

    return f"I found {len(result)} records."


def choose_chart(result):
    """Display an automatic chart when appropriate."""
    if result is None or result.empty:
        return

    if len(result) < 2:
        return

    numeric_cols = list(
        result.select_dtypes(include="number").columns
    )

    if not numeric_cols:
        return

    label_cols = [
        c for c in result.columns
        if c not in numeric_cols
    ]

    value_col = numeric_cols[0]

    if label_cols:
        label_col = label_cols[0]

        chart_df = result[[label_col, value_col]].copy()

        chart_df = chart_df.head(15)

        try:
            chart_df = chart_df.set_index(label_col)

            st.bar_chart(chart_df)

        except Exception:
            pass

    else:
        st.line_chart(result[[value_col]].head(20))


# ============================================================
# READY-MADE QUESTIONS
# ============================================================

QUESTIONS = {

"Basic Sales": [
"What is total sales?",
"What is total profit?",
"What is total quantity sold?",
"What is the average sales?",
"What is the average profit?",
"What is the average discount?",
"What is the maximum sales?",
"What is the minimum sales?",
"What is the maximum profit?",
"What is the minimum profit?"
],

"Category Analysis": [
"Show sales by category",
"Show profit by category",
"Show quantity by category",
"Which category has the highest sales?",
"Which category has the highest profit?",
"Which category has the lowest sales?",
"Which category has the lowest profit?",
"Show average discount by category",
"Show average sales by category",
"Show average profit by category"
],

"Sub-Category Analysis": [
"Show sales by sub-category",
"Show profit by sub-category",
"Show quantity by sub-category",
"Show average sales by sub-category",
"Show average profit by sub-category",
"Which sub-category has the highest sales?",
"Which sub-category has the highest profit?",
"Which sub-category has the lowest sales?",
"Which sub-category has the lowest profit?",
"Show discount by sub-category"
],

"Region Analysis": [
"Show sales by region",
"Show profit by region",
"Show quantity by region",
"Show average sales by region",
"Show average profit by region",
"Which region has the highest sales?",
"Which region has the highest profit?",
"Which region has the lowest sales?",
"Which region has the lowest profit?",
"Show discount by region"
],

"State Analysis": [
"Show sales by state",
"Show profit by state",
"Show quantity by state",
"Show average sales by state",
"Show average profit by state",
"Show top 5 states by sales",
"Show top 5 states by profit",
"Show bottom 5 states by sales",
"Show bottom 5 states by profit",
"Show top 10 states by sales"
],

"City Analysis": [
"Show sales by city",
"Show profit by city",
"Show quantity by city",
"Show top 5 cities by sales",
"Show top 5 cities by profit",
"Show bottom 5 cities by sales",
"Show bottom 5 cities by profit",
"Show top 10 cities by sales",
"Show top 10 cities by profit",
"Show average sales by city"
],

"Segment Analysis": [
"Show sales by segment",
"Show profit by segment",
"Show quantity by segment",
"Show average sales by segment",
"Show average profit by segment",
"Which segment has the highest sales?",
"Which segment has the highest profit?",
"Which segment has the lowest sales?",
"Which segment has the lowest profit?",
"Show discount by segment"
],

"Ship Mode": [
"Show sales by ship mode",
"Show profit by ship mode",
"Show quantity by ship mode",
"Show average sales by ship mode",
"Show average profit by ship mode",
"Which ship mode has the highest sales?",
"Which ship mode has the highest profit?",
"Which ship mode has the lowest sales?",
"Which ship mode has the lowest profit?",
"Show discount by ship mode"
],

"Advanced Analysis": [
"Show top 5 categories by sales",
"Show top 5 categories by profit",
"Show top 5 sub-categories by sales",
"Show top 5 sub-categories by profit",
"Show top 5 regions by sales",
"Show top 5 regions by profit",
"Show top 5 category and region combinations by sales",
"Show top 5 category and region combinations by profit",
"Show top 10 state and category combinations by sales",
"Show top 10 state and category combinations by profit"
]

}


# ============================================================
# FLATTEN QUESTIONS
# ============================================================

ALL_QUESTIONS = []

for category, questions in QUESTIONS.items():
    for question in questions:
        ALL_QUESTIONS.append(
            {
                "category": category,
                "question": question
            }
        )


# ============================================================
# SQL GENERATOR FOR READY QUESTIONS
# ============================================================

def ready_question_sql(question):
    q = question.lower()

    # ---------------- BASIC ----------------

    if q == "what is total sales?":
        return 'SELECT SUM("Sales") AS "Total Sales" FROM data'

    if q == "what is total profit?":
        return 'SELECT SUM("Profit") AS "Total Profit" FROM data'

    if q == "what is total quantity sold?":
        return 'SELECT SUM("Quantity") AS "Total Quantity" FROM data'

    if q == "what is the average sales?":
        return 'SELECT AVG("Sales") AS "Average Sales" FROM data'

    if q == "what is the average profit?":
        return 'SELECT AVG("Profit") AS "Average Profit" FROM data'

    if q == "what is the average discount?":
        return 'SELECT AVG("Discount") AS "Average Discount" FROM data'

    if q == "what is the maximum sales?":
        return 'SELECT MAX("Sales") AS "Maximum Sales" FROM data'

    if q == "what is the minimum sales?":
        return 'SELECT MIN("Sales") AS "Minimum Sales" FROM data'

    if q == "what is the maximum profit?":
        return 'SELECT MAX("Profit") AS "Maximum Profit" FROM data'

    if q == "what is the minimum profit?":
        return 'SELECT MIN("Profit") AS "Minimum Profit" FROM data'

    # ---------------- CATEGORY ----------------

    if "by category" in q:
        if "quantity" in q:
            return '''
SELECT "Category", SUM("Quantity") AS "Total Quantity"
FROM data
GROUP BY "Category"
ORDER BY "Total Quantity" DESC
'''

        if "average discount" in q:
            return '''
SELECT "Category", AVG("Discount") AS "Average Discount"
FROM data
GROUP BY "Category"
ORDER BY "Average Discount" DESC
'''

        if "average sales" in q:
            return '''
SELECT "Category", AVG("Sales") AS "Average Sales"
FROM data
GROUP BY "Category"
ORDER BY "Average Sales" DESC
'''

        if "average profit" in q:
            return '''
SELECT "Category", AVG("Profit") AS "Average Profit"
FROM data
GROUP BY "Category"
ORDER BY "Average Profit" DESC
'''

        if "profit" in q:
            return '''
SELECT "Category", SUM("Profit") AS "Total Profit"
FROM data
GROUP BY "Category"
ORDER BY "Total Profit" DESC
'''

        return '''
SELECT "Category", SUM("Sales") AS "Total Sales"
FROM data
GROUP BY "Category"
ORDER BY "Total Sales" DESC
'''

    # ---------------- SUB CATEGORY ----------------

    if "by sub-category" in q or "by sub category" in q:
        if "quantity" in q:
            return '''
SELECT "Sub-Category", SUM("Quantity") AS "Total Quantity"
FROM data
GROUP BY "Sub-Category"
ORDER BY "Total Quantity" DESC
'''

        if "discount" in q:
            return '''
SELECT "Sub-Category", AVG("Discount") AS "Average Discount"
FROM data
GROUP BY "Sub-Category"
ORDER BY "Average Discount" DESC
'''

        if "average sales" in q:
            return '''
SELECT "Sub-Category", AVG("Sales") AS "Average Sales"
FROM data
GROUP BY "Sub-Category"
ORDER BY "Average Sales" DESC
'''

        if "average profit" in q:
            return '''
SELECT "Sub-Category", AVG("Profit") AS "Average Profit"
FROM data
GROUP BY "Sub-Category"
ORDER BY "Average Profit" DESC
'''

        if "profit" in q:
            return '''
SELECT "Sub-Category", SUM("Profit") AS "Total Profit"
FROM data
GROUP BY "Sub-Category"
ORDER BY "Total Profit" DESC
'''

        return '''
SELECT "Sub-Category", SUM("Sales") AS "Total Sales"
FROM data
GROUP BY "Sub-Category"
ORDER BY "Total Sales" DESC
'''

    # ---------------- REGION ----------------

    if "by region" in q:
        if "quantity" in q:
            return '''
SELECT "Region", SUM("Quantity") AS "Total Quantity"
FROM data
GROUP BY "Region"
ORDER BY "Total Quantity" DESC
'''

        if "discount" in q:
            return '''
SELECT "Region", AVG("Discount") AS "Average Discount"
FROM data
GROUP BY "Region"
ORDER BY "Average Discount" DESC
'''

        if "average sales" in q:
            return '''
SELECT "Region", AVG("Sales") AS "Average Sales"
FROM data
GROUP BY "Region"
ORDER BY "Average Sales" DESC
'''

        if "average profit" in q:
            return '''
SELECT "Region", AVG("Profit") AS "Average Profit"
FROM data
GROUP BY "Region"
ORDER BY "Average Profit" DESC
'''

        if "profit" in q:
            return '''
SELECT "Region", SUM("Profit") AS "Total Profit"
FROM data
GROUP BY "Region"
ORDER BY "Total Profit" DESC
'''

        return '''
SELECT "Region", SUM("Sales") AS "Total Sales"
FROM data
GROUP BY "Region"
ORDER BY "Total Sales" DESC
'''

    # ---------------- STATE ----------------

    if "state" in q:
        limit = 10 if "top 10" in q else 5

        if "bottom" in q:
            order = "ASC"
        else:
            order = "DESC"

        if "profit" in q:
            return f'''
SELECT "State", SUM("Profit") AS "Total Profit"
FROM data
GROUP BY "State"
ORDER BY "Total Profit" {order}
LIMIT {limit}
'''

        if "average profit" in q:
            return f'''
SELECT "State", AVG("Profit") AS "Average Profit"
FROM data
GROUP BY "State"
ORDER BY "Average Profit" {order}
LIMIT {limit}
'''

        if "quantity" in q:
            return f'''
SELECT "State", SUM("Quantity") AS "Total Quantity"
FROM data
GROUP BY "State"
ORDER BY "Total Quantity" {order}
LIMIT {limit}
'''

        if "average sales" in q:
            return f'''
SELECT "State", AVG("Sales") AS "Average Sales"
FROM data
GROUP BY "State"
ORDER BY "Average Sales" {order}
LIMIT {limit}
'''

        return f'''
SELECT "State", SUM("Sales") AS "Total Sales"
FROM data
GROUP BY "State"
ORDER BY "Total Sales" {order}
LIMIT {limit}
'''

    # ---------------- CITY ----------------

    if "city" in q:
        limit = 10 if "top 10" in q else 5

        if "bottom" in q:
            order = "ASC"
        else:
            order = "DESC"

        if "profit" in q:
            return f'''
SELECT "City", SUM("Profit") AS "Total Profit"
FROM data
GROUP BY "City"
ORDER BY "Total Profit" {order}
LIMIT {limit}
'''

        if "quantity" in q:
            return f'''
SELECT "City", SUM("Quantity") AS "Total Quantity"
FROM data
GROUP BY "City"
ORDER BY "Total Quantity" {order}
LIMIT {limit}
'''

        if "average sales" in q:
            return f'''
SELECT "City", AVG("Sales") AS "Average Sales"
FROM data
GROUP BY "City"
ORDER BY "Average Sales" {order}
LIMIT {limit}
'''

        return f'''
SELECT "City", SUM("Sales") AS "Total Sales"
FROM data
GROUP BY "City"
ORDER BY "Total Sales" {order}
LIMIT {limit}
'''

    # ---------------- SEGMENT ----------------

    if "by segment" in q:
        if "quantity" in q:
            return '''
SELECT "Segment", SUM("Quantity") AS "Total Quantity"
FROM data
GROUP BY "Segment"
ORDER BY "Total Quantity" DESC
'''

        if "discount" in q:
            return '''
SELECT "Segment", AVG("Discount") AS "Average Discount"
FROM data
GROUP BY "Segment"
ORDER BY "Average Discount" DESC
'''

        if "average sales" in q:
            return '''
SELECT "Segment", AVG("Sales") AS "Average Sales"
FROM data
GROUP BY "Segment"
ORDER BY "Average Sales" DESC
'''

        if "average profit" in q:
            return '''
SELECT "Segment", AVG("Profit") AS "Average Profit"
FROM data
GROUP BY "Segment"
ORDER BY "Average Profit" DESC
'''

        if "profit" in q:
            return '''
SELECT "Segment", SUM("Profit") AS "Total Profit"
FROM data
GROUP BY "Segment"
ORDER BY "Total Profit" DESC
'''

        return '''
SELECT "Segment", SUM("Sales") AS "Total Sales"
FROM data
GROUP BY "Segment"
ORDER BY "Total Sales" DESC
'''

    # ---------------- SHIP MODE ----------------

    if "ship mode" in q:
        if "quantity" in q:
            return '''
SELECT "Ship Mode", SUM("Quantity") AS "Total Quantity"
FROM data
GROUP BY "Ship Mode"
ORDER BY "Total Quantity" DESC
'''

        if "discount" in q:
            return '''
SELECT "Ship Mode", AVG("Discount") AS "Average Discount"
FROM data
GROUP BY "Ship Mode"
ORDER BY "Average Discount" DESC
'''

        if "average sales" in q:
            return '''
SELECT "Ship Mode", AVG("Sales") AS "Average Sales"
FROM data
GROUP BY "Ship Mode"
ORDER BY "Average Sales" DESC
'''

        if "average profit" in q:
            return '''
SELECT "Ship Mode", AVG("Profit") AS "Average Profit"
FROM data
GROUP BY "Ship Mode"
ORDER BY "Average Profit" DESC
'''

        if "profit" in q:
            return '''
SELECT "Ship Mode", SUM("Profit") AS "Total Profit"
FROM data
GROUP BY "Ship Mode"
ORDER BY "Total Profit" DESC
'''

        return '''
SELECT "Ship Mode", SUM("Sales") AS "Total Sales"
FROM data
GROUP BY "Ship Mode"
ORDER BY "Total Sales" DESC
'''

    # ---------------- TOP CATEGORY ----------------

    if "top 5 categories by sales" in q:
        return '''
SELECT "Category", SUM("Sales") AS "Total Sales"
FROM data
GROUP BY "Category"
ORDER BY "Total Sales" DESC
LIMIT 5
'''

    if "top 5 categories by profit" in q:
        return '''
SELECT "Category", SUM("Profit") AS "Total Profit"
FROM data
GROUP BY "Category"
ORDER BY "Total Profit" DESC
LIMIT 5
'''

    if "top 5 sub-categories by sales" in q:
        return '''
SELECT "Sub-Category", SUM("Sales") AS "Total Sales"
FROM data
GROUP BY "Sub-Category"
ORDER BY "Total Sales" DESC
LIMIT 5
'''

    if "top 5 sub-categories by profit" in q:
        return '''
SELECT "Sub-Category", SUM("Profit") AS "Total Profit"
FROM data
GROUP BY "Sub-Category"
ORDER BY "Total Profit" DESC
LIMIT 5
'''

    if "top 5 regions by sales" in q:
        return '''
SELECT "Region", SUM("Sales") AS "Total Sales"
FROM data
GROUP BY "Region"
ORDER BY "Total Sales" DESC
LIMIT 5
'''

    if "top 5 regions by profit" in q:
        return '''
SELECT "Region", SUM("Profit") AS "Total Profit"
FROM data
GROUP BY "Region"
ORDER BY "Total Profit" DESC
LIMIT 5
'''

    # ---------------- COMBINATIONS ----------------

    if "category and region" in q:
        if "profit" in q:
            return '''
SELECT "Category", "Region",
       SUM("Profit") AS "Total Profit"
FROM data
GROUP BY "Category", "Region"
ORDER BY "Total Profit" DESC
LIMIT 5
'''

        return '''
SELECT "Category", "Region",
       SUM("Sales") AS "Total Sales"
FROM data
GROUP BY "Category", "Region"
ORDER BY "Total Sales" DESC
LIMIT 5
'''

    if "state and category" in q:
        if "profit" in q:
            return '''
SELECT "State", "Category",
       SUM("Profit") AS "Total Profit"
FROM data
GROUP BY "State", "Category"
ORDER BY "Total Profit" DESC
LIMIT 10
'''

        return '''
SELECT "State", "Category",
       SUM("Sales") AS "Total Sales"
FROM data
GROUP BY "State", "Category"
ORDER BY "Total Sales" DESC
LIMIT 10
'''

    return None


# ============================================================
# CUSTOM QUESTION SQL GENERATOR
# ============================================================

def custom_question_sql(question):
    """Simple natural-language SQL generator."""

    q = question.lower().strip()

    # Exact ready question
    ready = ready_question_sql(question)

    if ready:
        return ready

    # Total questions
    if "total sales" in q:
        return 'SELECT SUM("Sales") AS "Total Sales" FROM data'

    if "total profit" in q:
        return 'SELECT SUM("Profit") AS "Total Profit" FROM data'

    if "total quantity" in q or "total units" in q:
        return 'SELECT SUM("Quantity") AS "Total Quantity" FROM data'

    if "average sales" in q:
        return 'SELECT AVG("Sales") AS "Average Sales" FROM data'

    if "average profit" in q:
        return 'SELECT AVG("Profit") AS "Average Profit" FROM data'

    if "average discount" in q:
        return 'SELECT AVG("Discount") AS "Average Discount" FROM data'

    # Group by category
    if "category" in q:
        if "profit" in q:
            return '''
SELECT "Category", SUM("Profit") AS "Total Profit"
FROM data
GROUP BY "Category"
ORDER BY "Total Profit" DESC
'''

        return '''
SELECT "Category", SUM("Sales") AS "Total Sales"
FROM data
GROUP BY "Category"
ORDER BY "Total Sales" DESC
'''

    # Group by sub-category
    if "sub-category" in q or "sub category" in q:
        if "profit" in q:
            return '''
SELECT "Sub-Category", SUM("Profit") AS "Total Profit"
FROM data
GROUP BY "Sub-Category"
ORDER BY "Total Profit" DESC
'''

        return '''
SELECT "Sub-Category", SUM("Sales") AS "Total Sales"
FROM data
GROUP BY "Sub-Category"
ORDER BY "Total Sales" DESC
'''

    # Region
    if "region" in q:
        if "profit" in q:
            return '''
SELECT "Region", SUM("Profit") AS "Total Profit"
FROM data
GROUP BY "Region"
ORDER BY "Total Profit" DESC
'''

        return '''
SELECT "Region", SUM("Sales") AS "Total Sales"
FROM data
GROUP BY "Region"
ORDER BY "Total Sales" DESC
'''

    # State
    if "state" in q:
        if "profit" in q:
            return '''
SELECT "State", SUM("Profit") AS "Total Profit"
FROM data
GROUP BY "State"
ORDER BY "Total Profit" DESC
LIMIT 10
'''

        return '''
SELECT "State", SUM("Sales") AS "Total Sales"
FROM data
GROUP BY "State"
ORDER BY "Total Sales" DESC
LIMIT 10
'''

    # City
    if "city" in q:
        if "profit" in q:
            return '''
SELECT "City", SUM("Profit") AS "Total Profit"
FROM data
GROUP BY "City"
ORDER BY "Total Profit" DESC
LIMIT 10
'''

        return '''
SELECT "City", SUM("Sales") AS "Total Sales"
FROM data
GROUP BY "City"
ORDER BY "Total Sales" DESC
LIMIT 10
'''

    # Segment
    if "segment" in q:
        if "profit" in q:
            return '''
SELECT "Segment", SUM("Profit") AS "Total Profit"
FROM data
GROUP BY "Segment"
ORDER BY "Total Profit" DESC
'''

        return '''
SELECT "Segment", SUM("Sales") AS "Total Sales"
FROM data
GROUP BY "Segment"
ORDER BY "Total Sales" DESC
'''

    # Ship mode
    if "ship mode" in q:
        if "profit" in q:
            return '''
SELECT "Ship Mode", SUM("Profit") AS "Total Profit"
FROM data
GROUP BY "Ship Mode"
ORDER BY "Total Profit" DESC
'''

        return '''
SELECT "Ship Mode", SUM("Sales") AS "Total Sales"
FROM data
GROUP BY "Ship Mode"
ORDER BY "Total Sales" DESC
'''

    return None


# ============================================================
# VOICE TRANSCRIPTION
# ============================================================

def transcribe_audio(audio_bytes):
    if not SPEECH_AVAILABLE:
        return None, "SpeechRecognition is not installed."

    try:
        recognizer = sr.Recognizer()

        audio_file = io.BytesIO(audio_bytes)

        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)

        return text, None

    except sr.UnknownValueError:
        return None, "I could not understand the audio."

    except sr.RequestError:
        return None, (
            "Speech recognition service is unavailable. "
            "Please check your internet connection."
        )

    except Exception as e:
        return None, str(e)


# ============================================================
# PROCESS QUESTION
# ============================================================

def process_question(question):
    question = question.strip()

    if not question:
        return

    # End conversation
    end_words = [
        "end",
        "end question",
        "end questions",
        "finish",
        "quit",
        "stop"
    ]

    if question.lower() in end_words:
        st.session_state.conversation_active = False
        return

    # Generate SQL
    sql = custom_question_sql(question)

    if not sql:
        st.error(
            "I could not understand that question yet. "
            "Try one of the suggested questions."
        )
        return

    # Validate
    safe, message = validate_sql(sql)

    if not safe:
        st.error(message)
        return

    # Execute
    result, error = execute_sql(sql)

    if error:
        st.error(f"SQL execution error: {error}")
        return

    answer = generate_answer(question, result)

    insight = make_insight(question, result)

    # Save history
    item = {
        "number": len(st.session_state.history) + 1,
        "question": question,
        "answer": answer,
        "insight": insight,
        "sql": sql,
        "result": result.copy(),
        "time": datetime.now().strftime("%H:%M:%S")
    }

    st.session_state.history.append(item)

    st.session_state.question_input = ""


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🩺 DataDoctor AI")

    st.write(
        "Talk to your data. Clean it. "
        "Analyze it. Understand it."
    )

    st.divider()

    st.subheader("📂 Dataset")

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel",
        type=["csv", "xlsx", "xls"]
    )

    if uploaded_file is not None:

        new_df = load_file(uploaded_file)

        if new_df is not None:

            st.session_state.df = new_df
            st.session_state.dataset_name = uploaded_file.name
            st.session_state.db_ready = False

            st.success("Dataset uploaded.")

    elif st.session_state.df is None:

        default_df = load_default_dataset()

        if default_df is not None:

            st.session_state.df = default_df
            st.session_state.dataset_name = "SampleSuperstore.csv"

    st.divider()

    if st.session_state.df is not None:

        st.write(
            f"**Dataset:** "
            f"{st.session_state.dataset_name}"
        )

        st.write(
            f"**Rows:** {len(st.session_state.df):,}"
        )

        st.write(
            f"**Columns:** {len(st.session_state.df.columns)}"
        )

        if st.button(
            "🗄️ Create / Refresh Database",
            width="stretch"
        ):

            with st.spinner("Creating SQLite database..."):

                success = create_database(
                    st.session_state.df
                )

                if success:

                    st.session_state.db_ready = True

                    st.success(
                        "Database created successfully."
                    )

        if os.path.exists(DB_FILE):
            st.caption("SQLite database available.")

    st.divider()

    st.subheader("🧹 Data Cleaning")

    if st.session_state.df is not None:

        if st.button(
            "Clean Dataset",
            width="stretch"
        ):

            cleaned = clean_dataframe(
                st.session_state.df
            )

            st.session_state.cleaned_df = cleaned

            st.success(
                "Dataset cleaned successfully."
            )

            removed = (
                len(st.session_state.df)
                - len(cleaned)
            )

            st.write(
                f"Rows removed: **{removed}**"
            )

            # Automatically update database
            create_database(cleaned)

            st.session_state.db_ready = True

            st.success(
                "Cleaned dataset loaded into database."
            )


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🩺 DataDoctor AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Talk to your data. Clean it. Analyze it. Understand it.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# DATASET INFORMATION
# ============================================================

if st.session_state.df is None:

    st.warning(
        "Please upload a CSV/Excel file or place "
        "SampleSuperstore.csv inside the data folder."
    )

    st.stop()


df = st.session_state.df

# Create database automatically
if not st.session_state.db_ready:

    create_database(df)

    st.session_state.db_ready = True


# ============================================================
# DATA QUALITY DASHBOARD
# ============================================================

st.subheader("📊 Data Quality")

quality = quality_report(df)

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric("Rows", f"{quality['rows']:,}")

with c2:
    st.metric("Columns", quality["columns"])

with c3:
    st.metric("Missing Values", quality["missing"])

with c4:
    st.metric("Duplicates", quality["duplicates"])

with c5:
    st.metric(
        "Quality Score",
        f"{quality['quality_score']}%"
    )


with st.expander("🔎 View Dataset"):

    st.dataframe(
        df.head(100),
        width="stretch"
    )


with st.expander("🧹 Data Quality Details"):

    quality_table = pd.DataFrame({
        "Column": df.columns,
        "Data Type": [
            str(df[c].dtype)
            for c in df.columns
        ],
        "Missing Values": [
            int(df[c].isna().sum())
            for c in df.columns
        ],
        "Unique Values": [
            int(df[c].nunique())
            for c in df.columns
        ]
    })

    st.dataframe(
        quality_table,
        width="stretch"
    )


# ============================================================
# CONVERSATION HISTORY
# ============================================================

if st.session_state.history:

    st.subheader("📜 Conversation History")

    st.write(
        f"**Total Questions: "
        f"{len(st.session_state.history)}**"
    )

    for item in st.session_state.history:

        with st.container(border=True):

            st.markdown(
                f"### Q{item['number']} "
                f"{item['question']}"
            )

            st.write(
                f"**Answer:** {item['answer']}"
            )

            st.write(
                f"**💡 Insight:** {item['insight']}"
            )

            with st.expander("📋 Result"):

                st.dataframe(
                    item["result"],
                    width="stretch"
                )

                choose_chart(item["result"])

            with st.expander("🔐 Generated SQL"):

                st.code(
                    item["sql"],
                    language="sql"
                )

            st.caption(
                f"Asked at {item['time']}"
            )


# ============================================================
# CONVERSATION STATUS
# ============================================================

if not st.session_state.conversation_active:

    st.success(
        "✅ Conversation ended. "
        "Your complete history is still available above."
    )

    if st.button(
        "▶️ Start New Conversation",
        width="stretch"
    ):

        st.session_state.conversation_active = True

        st.rerun()

    st.stop()


# ============================================================
# ASK DATADOCTOR
# ============================================================

st.divider()

st.subheader("🤖 Ask DataDoctor")

st.write(
    "Type a question, choose a suggested question, "
    "or use your microphone."
)


# ============================================================
# VOICE INPUT
# ============================================================

if VOICE_AVAILABLE and SPEECH_AVAILABLE:

    st.markdown("### 🎤 Voice Question")

    voice_audio = mic_recorder(
        start_prompt="🎤 Start Recording",
        stop_prompt="⏹️ Stop Recording",
        just_once=True,
        use_container_width=False,
        format="wav",
        key="voice_recorder"
    )

    if voice_audio:

        audio_bytes = voice_audio.get("bytes")

        if audio_bytes:

            with st.spinner(
                "🎧 Converting your voice to text..."
            ):

                voice_text, voice_error = (
                    transcribe_audio(audio_bytes)
                )

            if voice_error:

                st.error(voice_error)

            elif voice_text:

                st.success(
                    f"Recognized: **{voice_text}**"
                )

                st.session_state.question_input = (
                    voice_text
                )

                process_question(voice_text)

                st.rerun()

else:

    st.info(
        "Voice input is unavailable. "
        "The text question system is still available."
    )


# ============================================================
# QUESTION INPUT
# ============================================================

question = st.text_input(
    "💬 Type your question",
    value=st.session_state.question_input,
    key="main_question_input",
    placeholder="Example: What is total sales?"
)

st.session_state.question_input = question


# ============================================================
# LIVE SEARCH
# ============================================================

if question.strip():

    search_text = question.lower().strip()

    matches = [
        item for item in ALL_QUESTIONS
        if search_text in item["question"].lower()
    ]

    if matches:

        st.markdown("### 🔎 Suggested Questions")

        suggestion_container = st.container(
            height=260,
            border=True
        )

        with suggestion_container:

            for index, item in enumerate(
                matches[:30]
            ):

                if st.button(
                    f"📌 {item['question']}",
                    key=f"suggestion_{index}_{item['question']}",
                    width="stretch"
                ):

                    st.session_state.question_input = (
                        item["question"]
                    )

                    st.rerun()


# ============================================================
# READY-MADE QUESTIONS
# ============================================================

st.markdown("### 📚 Ready-Made Questions")

st.caption(
    f"{len(ALL_QUESTIONS)} questions available"
)

for category, questions in QUESTIONS.items():

    with st.expander(
        f"📁 {category} ({len(questions)})"
    ):

        question_container = st.container(
            height=230,
            border=True
        )

        with question_container:

            for index, ready_question in enumerate(
                questions
            ):

                if st.button(
                    ready_question,
                    key=f"ready_{category}_{index}",
                    width="stretch"
                ):

                    st.session_state.question_input = (
                        ready_question
                    )

                    st.rerun()


# ============================================================
# ACTION BUTTONS
# ============================================================

st.markdown("### ⚡ Actions")

col1, col2, col3 = st.columns(3)

with col1:

    ask_button = st.button(
        "🚀 ASK DATADOCTOR",
        type="primary",
        width="stretch"
    )

with col2:

    end_button = st.button(
        "⏹️ END CONVERSATION",
        width="stretch"
    )

with col3:

    clear_button = st.button(
        "🗑️ CLEAR INPUT",
        width="stretch"
    )


# ============================================================
# ACTION LOGIC
# ============================================================

if clear_button:

    st.session_state.question_input = ""

    st.rerun()


if end_button:

    st.session_state.conversation_active = False

    st.rerun()


if ask_button:

    if not st.session_state.question_input.strip():

        st.warning(
            "Please type or select a question first."
        )

    else:

        current_question = (
            st.session_state.question_input
        )

        with st.spinner(
            "🧠 DataDoctor is analyzing your data..."
        ):

            process_question(current_question)

        st.rerun()


# ============================================================
# EXPORT HISTORY
# ============================================================

if st.session_state.history:

    st.divider()

    st.subheader("📥 Export Conversation")

    export_rows = []

    for item in st.session_state.history:

        export_rows.append({
            "Question Number": item["number"],
            "Question": item["question"],
            "Answer": item["answer"],
            "Insight": item["insight"],
            "SQL": item["sql"],
            "Time": item["time"]
        })

    export_df = pd.DataFrame(export_rows)

    csv_data = export_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "📥 Download Conversation History",
        data=csv_data,
        file_name="datadoctor_conversation_history.csv",
        mime="text/csv",
        width="stretch"
    )

    if st.button(
        "🗑️ Clear Conversation History",
        width="stretch"
    ):

        st.session_state.history = []

        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🩺 DataDoctor AI | "
    "Intelligent Voice-Driven Data Analytics & SQL Assistant"
)

st.caption(
    "Talk to your data. Clean it. Analyze it. Understand it."
)