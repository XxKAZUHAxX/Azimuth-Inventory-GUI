import pandas as pd

# Create a sample dataframe
data = {'name': ['John', 'Jane', 'Bob', 'Alice'],
        'age': [25, 30, 35, 40]}
df = pd.DataFrame(data)

# # Get the row number of the row with name 'Bob'
# for i, row in df.iterrows():
#     if row['name'] == 'Bob':
#         row_number = i
#         break

row_number = df.index[df['name'] == 'Bob'][0]

print(row_number)