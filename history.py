import pandas as pd


# ============================================================
# ADD HISTORY ITEM
# ============================================================

def add_history(
    history,
    question,
    sql,
    result,
    answer,
    insight,
    timestamp
):

    item = {

        "question_number":
            len(history) + 1,

        "question":
            question,

        "sql":
            sql.strip(),

        "result":
            result.copy()
            if result is not None
            else pd.DataFrame(),

        "answer":
            answer,

        "insight":
            insight,

        "timestamp":
            timestamp
    }

    history.append(item)

    return history


# ============================================================
# EXPORT HISTORY
# ============================================================

def history_to_dataframe(history):

    rows = []

    for item in history:

        if item["result"] is not None:

            result_text = item[
                "result"
            ].to_string(
                index=False
            )

        else:

            result_text = "No result"

        rows.append({

            "Question Number":
                item["question_number"],

            "Question":
                item["question"],

            "Answer":
                item["answer"],

            "SQL":
                item["sql"],

            "Insight":
                item["insight"],

            "Timestamp":
                item["timestamp"],

            "Result":
                result_text
        })

    return pd.DataFrame(rows)


def export_history_csv(history):

    df = history_to_dataframe(
        history
    )

    return df.to_csv(
        index=False
    ).encode("utf-8")