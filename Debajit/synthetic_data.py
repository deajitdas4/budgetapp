import pandas as pd
import numpy as np

# Parameters
num_users = 1000  # Number of users
years = [2024]  # Year range
months = list(range(1, 13))  # Months (1 to 12)
scenarios = [
    ("Stable Salary & Stable Fixed Expenses", 0.20),
    ("Stable Salary & Increasing Fixed Expenses", 0.15),
    ("Stable Salary & Decreasing Fixed Expenses", 0.05),
    ("Salary Increases & Fixed Expenses Remain Stable", 0.30),
    ("Salary Increases & Fixed Expenses Increase", 0.25),
    ("Salary Increases & Fixed Expenses Decrease", 0.05),
]

# Spending behavior types
spending_behaviors = {
    "Frugal": (0.2, 0.3),   # Saves more, spends less
    "Balanced": (0.3, 0.5), # Moderate spending
    "Extravagant": (0.5, 0.7) # High spending
}

# Festive spending months
festive_months = {3: (1.1, 1.3), 9: (1.05, 1.15), 10: (1.1, 1.3), 11: (1.05, 1.15), 12: (1.1, 1.3)}

# Festive spending profiles
festive_profiles = {
    "All Festivals": list(festive_months.keys()),  # Spends in all festive months
    "Selective Festivals": np.random.choice(list(festive_months.keys()), size=2, replace=False).tolist(),  # Spends in selected months
    "No Impact": []  # No festive impact
}

# Function to determine realistic fixed expenses
def calculate_fixed_expenses(salary):
    if salary < 50000:
        return np.random.randint(10000, 23000)
    elif salary < 100000:
        return np.random.randint(23000, 40000)
    elif salary < 200000:
        return np.random.randint(40000, 80000)
    else:
        return np.random.randint(60000, 120000)

# Function to generate data
def generate_data():
    data = []
    user_ids = [f"U{str(i).zfill(3)}" for i in range(1, num_users + 1)]
    # Assigning categories to users
    user_increase_limits = {}  # Store the max increases allowed for each user
    for user_id in user_ids:
        # Assigning increase limits to users based on probability
        increase_category = np.random.choice([3, 5, 999], p=[0.7, 0.2, 0.1])  # 999 means no strict limit
        user_increase_limits[user_id] = increase_category  # Store per user

        base_salary = np.random.randint(20000, 300000)
        fixed_expenses = calculate_fixed_expenses(base_salary)
        salary_increase_applied = False
        salary_increase_month = np.random.choice(months[2:8])  # Between March and August
        scenario = np.random.choice([s[0] for s in scenarios], p=[s[1] for s in scenarios])
        expense_increase_count = 0  # Track how many times expenses increased for the user
        spending_type = np.random.choice(list(spending_behaviors.keys()), p=[0.35, 0.5, 0.15])
        min_expense_ratio, max_expense_ratio = spending_behaviors[spending_type]
        festive_spending_type = np.random.choice(list(festive_profiles.keys()), p=[0.3, 0.4, 0.3])
        user_festive_months = festive_profiles[festive_spending_type]
        
        # Initialize balance for January
        balance = np.random.randint(min(base_salary, 250000), 250000 + 1)
        previous_savings = 0  # Store last month's savings for balance update

        for year in years:
            for month in months:
                # Apply scenario rules
                if scenario.startswith("Stable Salary"):
                    salary = base_salary
                    if "Increasing" in scenario:
                        if expense_increase_count < user_increase_limits[user_id]:
                            if np.random.rand() < 0.15:
                                fixed_expenses += np.random.randint(500, 2000)
                                expense_increase_count += 1
                    elif "Decreasing" in scenario:
                        if np.random.rand() < 0.05:  # 5% chance per month
                            decrease_amount = np.random.randint(500, 2000)
                            fixed_expenses = max(fixed_expenses - decrease_amount, fixed_expenses * 0.9)  # More stable decrease
                else:
                    if not salary_increase_applied and month == salary_increase_month:
                        base_salary += np.random.randint(5000, 30000)
                        salary_increase_applied = True
                    salary = base_salary
                    
                    if "Fixed Expenses Increase" in scenario:
                        if expense_increase_count < user_increase_limits[user_id]:
                            if np.random.rand() < 0.20:
                                fixed_expenses += np.random.randint(500, 2000)
                                expense_increase_count += 1
                    elif "Fixed Expenses Decrease" in scenario:
                        if np.random.rand() < 0.05:  # 5% chance per month
                            decrease_amount = np.random.randint(500, 2000)
                            fixed_expenses = max(fixed_expenses - decrease_amount, fixed_expenses * 0.9)
                
                # Apply base spending behavior
                variable_expenses = np.random.randint(int(min_expense_ratio * salary), int(max_expense_ratio * salary))
                
                # Apply festive spending multiplier only if user spends in this month
                if month in user_festive_months:
                    min_multiplier, max_multiplier = festive_months[month]
                    variable_expenses = int(variable_expenses * np.random.uniform(min_multiplier, max_multiplier))
                
                total_expenses = fixed_expenses + variable_expenses
                savings = salary - total_expenses
                savings_rate = savings / salary * 100 if salary > 0 else 0
                expense_fluctuation = np.random.uniform(-0.05, 0.05)
                
                # ✅ **Correct Balance Calculation**
                if month > 1:
                    balance += previous_savings  # Add previous month's savings
                
                previous_savings = savings  # Store savings for next month

                # Assign risk category
                risk_category = "Low Risk" if savings_rate >= 25 else "Medium Risk" if savings_rate >= 15 else "High Risk"
                
                data.append([
                    user_id, year, month, balance, scenario, salary, fixed_expenses, 
                    variable_expenses, total_expenses, savings, 
                    round(savings_rate, 2), round(expense_fluctuation, 2), risk_category
                ])
    
    return pd.DataFrame(data, columns=[
        "User_ID", "Year", "Month", "Balance", "Scenario", "Salary", "Fixed_Expenses", 
        "Variable_Expenses", "Total_Expenses", "Savings", "Savings_Rate", 
        "Expense_Fluctuation", "Risk_Category"
    ])

# Generate dataset
df = generate_data()
print(df.head())  # Preview data
df.to_csv("synthetic_budget_data2.csv", index=False)
