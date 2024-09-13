import tkinter as tk
from tkinter import ttk
import os
import re
from datetime import date

def read_salary_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    pattern = r'(\w+(?:\s+\w+)?): ([\d.]+) شيكل \(Total Jobs: (\d+)\)'
    matches = re.findall(pattern, content)
    
    salary_data = {}
    for match in matches:
        name, amount, jobs = match
        salary_data[name] = {'amount': float(amount), 'jobs': int(jobs)}
    
    return salary_data

def round_to_nearest_100(value):
    return round(value / 100) * 100

def calculate_expected_salary(name, amount):
    fixed_salaries = {
        'العزموطي': 800,
        'ابو النبيل': 700,
        'ادهم': 800,
        'علاء': 700,
        'عبد': 500,
        'خنفر': 1200
    }
    
    if name in fixed_salaries:
        return fixed_salaries[name]
    
    if name == 'زيد':
        salary = min(1300, amount * 0.33)
    elif name == 'شجاع':
        salary = min(1500, max(1400, amount * 0.44))
    elif name in ['اسامه', 'العزب', 'ابو المشايخ']:
        base_salary = 2300 if name in ['العزب', 'ابو المشايخ'] else 2200
        if amount > 3900:
            extra = (amount - 3900) * 0.1  # 10% of the extra amount
            salary = base_salary + extra
        else:
            salary = min(base_salary, amount * 0.56)
    elif name == 'ابو الشيخ':
        salary = min(900, amount * 0.56)
    else:
        salary = min(2200, amount * 0.56)
    
    return salary

def save_results(results):
    if not os.path.exists('output-salary-expected'):
        os.makedirs('output-salary-expected')
    
    total_salaries = sum(data['expected_salary'] for data in results.values())
    today = date.today().strftime("%Y-%m-%d")
    
    with open('output-salary-expected/expected_salaries.txt', 'w', encoding='utf-8') as file:
        file.write("حاسبة الكاش للموظفين\n")
        file.write(f"Date: {today}\n")
        file.write("=" * 30 + "\n\n")
        for name, data in results.items():
            file.write(f"{name}: {data['expected_salary']:.2f} شيكل\n")
        file.write("\n" + "=" * 30 + "\n")
        file.write(f"Total salaries: {total_salaries:.2f} شيكل\n")

def calculate_salaries():
    results = {}
    rounded_employees = ['زيد', 'اسامه', 'العزب', 'ابو المشايخ', 'شجاع', 'ابو الشيخ']
    
    for name, var in attendance_vars.items():
        days_worked = var.get()
        amount = salary_data.get(name, {}).get('amount', 0)
        expected_salary = calculate_expected_salary(name, amount)
        
        if days_worked < 6:
            daily_rate = expected_salary / 6
            expected_salary = daily_rate * days_worked
        
        if name in rounded_employees:
            expected_salary = round_to_nearest_100(expected_salary)
        
        results[name] = {'expected_salary': expected_salary}
    
    save_results(results)
    result_label.config(text="تم حفظ النتائج في output-salary-expected/expected_salaries.txt")

# Read salary data
salary_data = read_salary_data('salary.txt')

# Create GUI
root = tk.Tk()
root.title("حاسبة الكاش للموظفين")
root.geometry("400x600")  # Make the window bigger

# Create and pack widgets
frame = ttk.Frame(root, padding="20")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Configure grid to expand
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)

# Add title
title_label = ttk.Label(frame, text="حاسبة الكاش للموظفين", font=("Arial", 16, "bold"))
title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

attendance_vars = {}
row = 1

ttk.Label(frame, text="الموظف", font=("Arial", 12, "bold")).grid(row=row, column=0, sticky=tk.W, pady=(0, 10))
ttk.Label(frame, text="أيام العمل", font=("Arial", 12, "bold")).grid(row=row, column=1, sticky=tk.W, pady=(0, 10))
row += 1

employees = ['زيد', 'اسامه', 'ابو الشيخ', 'العزب', 'العزموطي', 'ابو المشايخ', 'شجاع', 
             'ابو النبيل', 'ادهم', 'علاء', 'عبد', 'خنفر']

for name in employees:
    ttk.Label(frame, text=name, font=("Arial", 11)).grid(row=row, column=0, sticky=tk.W, pady=5)
    var = tk.IntVar(value=6)  # Default to 6 days worked
    attendance_vars[name] = var
    ttk.Entry(frame, textvariable=var, width=5, font=("Arial", 11)).grid(row=row, column=1, sticky=tk.W, pady=5)
    row += 1

calculate_button = ttk.Button(frame, text="احسب الرواتب", command=calculate_salaries, style="AccentButton.TButton")
calculate_button.grid(row=row, column=0, columnspan=2, pady=20)

result_label = ttk.Label(frame, text="", font=("Arial", 11))
result_label.grid(row=row+1, column=0, columnspan=2)

# Style configuration
style = ttk.Style()
style.configure("AccentButton.TButton", font=("Arial", 12, "bold"))

root.mainloop()
