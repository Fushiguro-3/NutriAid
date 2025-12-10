# utils/recommender.py

import pandas as pd
from functools import lru_cache

DATA_PATH = "data/food_data.csv"


@lru_cache
def _load_food_df():
    """Load food data once and cache it."""
    return pd.read_csv(DATA_PATH)


def _sample_meal(df, keyword: str):
    """
    Pick one random row where 'category' contains the keyword.
    If nothing matches, fall back to whole dataframe.
    """
    cat = df["category"].astype(str).str.lower()
    subset = df[cat.str.contains(keyword)]
    if subset.empty:
        subset = df
    return subset.sample(1).iloc[0]


def generate_day_plan(calories: float):
    """
    Generate a single day's plan (breakfast, lunch, dinner, snacks)
    based on your food_data.csv.
    """
    df = _load_food_df()

    breakfast = _sample_meal(df, "break")
    lunch = _sample_meal(df, "lunch")
    dinner = _sample_meal(df, "din")
    snacks = _sample_meal(df, "snack")

    return {
        "target_calories": calories,
        "breakfast": breakfast.to_dict(),
        "lunch": lunch.to_dict(),
        "dinner": dinner.to_dict(),
        "snacks": snacks.to_dict(),
    }


def generate_meal_plan(calories: float, days: int = 1):
    """
    Backwards compatible:
      - days == 1 → return ONE dict (like before)
      - days > 1  → return a LIST of day plans (for weekly view)
    """
    if days <= 1:
        return generate_day_plan(calories)

    week = []
    for i in range(days):
        day_plan = generate_day_plan(calories)
        day_plan["day_index"] = i + 1
        week.append(day_plan)

    return week
