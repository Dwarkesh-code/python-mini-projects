import pandas as pd
import matplotlib.pyplot as plt
from pandas.api.types import is_numeric_dtype

def currency_checker(d, s):
    a = d[s]
    if len(a.iloc[1]) >=2 :
        num = a.str.extract(r'(\d+)')
        st = a.str.extract(r'([^0-9]+)')
        if len(st.iloc[0])==1 and pd.notna(num.iloc[0, 0]) and pd.notna(num.iloc[-1, 0]):
            currency = st.drop_duplicates()
            return num, currency
    return None, None

def high_value_checker(ax, num):
    ticks = ax.get_yticks()
    high_value = num.max()
    if len(ticks)>1:
        difference = ticks[1]-ticks[0]
        high_value = int(high_value) + difference
    else:
        high_value +=10

    return high_value

def generate_visual(ax, chart_type, x, num, fmt, sym):

    chart_type = chart_type.lower().strip()

    if chart_type == 'bar':
        bars = ax.bar(x, num)
        ax.bar_label(bars, fmt=fmt, padding=3)
        ax.set_title("Bar Chart")
        high_value = high_value_checker(ax, num)
        ax.set_ylim(0, high_value)

    elif chart_type == 'plot' or chart_type == 'line':
        line, = ax.plot(x, num, marker='o')
        for i, val in enumerate(num):
            ax.annotate(f'{val}', (x[i], num[i]), xytext=(0, 7),
                        textcoords="offset points", ha='center')
        ax.set_title("Line Plot")
        high_value = high_value_checker(ax, num)
        ax.set_ylim(0, high_value)

    elif chart_type == 'scatter':
        scat = ax.scatter(x, num)
        for i, val in enumerate(num):
            ax.annotate(val, (x[i], num[i]), xytext=(5, 5),
                        textcoords="offset points")
        ax.set_title("Scatter Plot")
        high_value = high_value_checker(ax, num)
        ax.set_ylim(0, high_value)

    elif chart_type == 'hist':
        # Histogram mein 'num' ka distribution dekha jata hai
        n, bins, patches = ax.hist(num, bins=10, edgecolor='black')
        ax.bar_label(patches, fmt=fmt, padding=3)
        ax.set_title("Histogram")
        #ax.set_ylim(0, high_value)

    elif chart_type == 'pie':
        ax.pie(num, labels=x, autopct='%1.1f%%')
        ax.axis('equal')
        ax.set_title("Pie Chart")
        print(sym.strip(),sum(num))

while True:
    file_name = input("Enter Your File Name : ").strip()
    if file_name:
        file_ = file_name.split('.')
        if len(file_) != 2:
            file_name = f"{file_[0]}.csv"
    try:
        file_data = pd.read_csv(file_name)
        break
    except FileNotFoundError:
        print(file_name," is not exist")
        continue

numeric_values = file_data.select_dtypes(include=['number']).columns.tolist()
string_values = file_data.select_dtypes(exclude=['number']).columns.tolist()


for s in string_values:
    num, currency = currency_checker(file_data, s)
    if num is not None and not num.empty:
        numeric_values.append(s)
column_names = file_data.columns.tolist()


while True:
    try:
        print(f'\nThese are the columns names for X-Axis')
        print(', '.join(column_names))
        x = input('What You want on X-Axis : ').strip()
        print('\nThese are the columns names for Y-Axis')
        print(', '.join(numeric_values))
        y = input('What You want on Y-Axis : ').strip()
        x_lab = x
        y_lab = y
        x = file_data[x]
        num = file_data[y]
        break

    except KeyError as e:
        print()
        print(e.args[0],"column name is does not exist")
        try :
            g = e.args[0].title()
            v = file_data[g]
            print(f'{e.args[0]} is not right but {g} is right ')
            print(f'Try to type {e.args[0]} in Uppercase ')
        except KeyError:
            print()
        print('\n')
        continue

fmt =f'%g'
sym=''
if not is_numeric_dtype(num.iloc[:]) :
    num, currency = currency_checker(file_data, y)
    num =num[0]
    if currency[0] is not None and not currency.empty :
        sym = currency[0].iloc[0]
        fmt = f'{sym}%g'
    else:
        fmt =f'%g'
else:
    num = num[:]

chart_types = ['bar', 'line', 'plot', 'scatter', 'hist', 'pie']
num = pd.to_numeric(num, errors='coerce')
fig, ax = plt.subplots()

print("\nThese chart types are available for You")
print(", ".join(chart_types))
while True:
    user_choice = input("Enter Chart type : ").lower().strip()
    if user_choice in chart_types:
        generate_visual(ax, user_choice, x, num, fmt, sym)
        break
    else:
        print("Invalid chart type!")
        continue
plt.xlabel(x_lab)
plt.ylabel(y_lab)
plt.xticks(rotation=90)

print()
while True:
    asking = input("Do You want save this chart : ").strip().lower()
    try:
        if asking not in ['', 'no', 'not', 'n', 'nahi']:
            file_save_name = input("What Name Do You want to save : ").strip()
            with open(file_save_name, 'r') as file:
                print(f"{file_save_name} file exists")
                print("Change file name")
                continue
        else:
            break
    except FileNotFoundError as e :
        plt.savefig(file_save_name)
        break

plt.show()
