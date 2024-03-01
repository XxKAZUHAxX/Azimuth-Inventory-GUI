from datetime import datetime

current_year = datetime.now().strftime('%Y')
print(current_year)

current_month_text = datetime.now().strftime('%B').upper()
print(current_month_text)

dr_date = datetime.now().strftime('%d-%h-%Y')
print(dr_date)