import pandas as pd
import numpy as np
import random

# Set random seed for reproducibility
np.random.seed(42)

# Number of users
num_users = 1000

# Generate User IDs
user_ids = [f"U{str(i).zfill(3)}" for i in range(1, num_users + 1)]

# Generate salaries (Low: 30k-50k, Mid: 50k-80k, High: 80k-150k)
salary_ranges = [(30000, 50000), (50000, 80000), (80000, 300000)]
salaries = [random.randint(*random.choice(salary_ranges)) for _ in range(num_users)]

# Generate fixed expenses
fixed_rent = [int(s * random.uniform(0.25, 0.35)) for s in salaries]  # 25-35% of salary
emi = [int(s * random.uniform(0.05, 0.15)) for s in salaries]  # 5-15% of salary

# Generate variable expenses
groceries = [int(s * random.uniform(0.08, 0.12)) for s in salaries]  # 8-12% of salary
subscriptions = [random.randint(0, 3000) for _ in range(num_users)]
upi_spent = [int(s * random.uniform(0.07, 0.25)) for s in salaries]  # 7-25% of salary
credit_spent = [int(s * random.uniform(0.10, 0.25)) for s in salaries]  # 10-25% of salary
utilities = [random.randint(1000, 8000) for _ in range(num_users)]

# Generate savings and investments
# bills_savings = [int(s * random.uniform(0.10, 0.20)) for s in salaries]  # 10-20% of salary
investment_percentage = [random.randint(10, 30) for _ in range(num_users)]  # 10-30% investment

# Generate month labels
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
month_column = [random.choice(months) for _ in range(num_users)]

# Create DataFrame
df = pd.DataFrame({
    "UserID": user_ids,
    "Salary": salaries,
    "Fixed_Rent": fixed_rent,
    "EMI": emi,
    "Groceries": groceries,
    "Subscriptions": subscriptions,
    "UPI_Spent": upi_spent,
    "CreditCard_Spent": credit_spent,
    "Utilities": utilities,
    # "Bills_Savings": bills_savings,
    "Investment_Percentage": investment_percentage,
    "Month": month_column
})

# Introduce null values in Subscriptions (randomly select 10% of rows)
num_nulls = int(0.17 * num_users)  # 17% of data
null_indices = random.sample(range(num_users), num_nulls)  # Pick random indices

df.loc[null_indices, "Subscriptions"] = np.nan  # Set selected indices to NaN

# Save to CSV
df.to_csv("synthetic_budget_data.csv", index=False)

# Display sample data
print(df.head())
