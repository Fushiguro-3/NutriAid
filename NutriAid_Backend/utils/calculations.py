def calculate_bmi(weight, height):
    h = height / 100
    return round(weight / (h*h), 2)

def calculate_calories(age, gender, height, weight, activity):
    bmr = 10*weight + 6.25*height - 5*age + (5 if gender.lower()=="male" else -161)
    factor = {"low":1.2, "medium":1.55, "high":1.75}.get(activity.lower(), 1.2)
    return round(bmr * factor, 2)
