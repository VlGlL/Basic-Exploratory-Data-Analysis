import pandas as pd
import matplotlib.pyplot as plt

# Our task is to explore how the market performance looks like:

# Q1. What is the monthly invoice volume?
# Q2. How many invoices were processed by the processors?
# Q3. A. Who are the top 3 processors?
# Q3. B. How many invoices should be assigned to a processor on a daily basis,
# to cover the average monthly invoice volume on a monthly basis?
# Q4. What is the average processing and payment time?

# Load the dataset and perform EDA
data = pd.read_excel('/Users/somahelik/PycharmProjects/Data_Analysis_Projects/AccountsPayable_Raw_data.xlsx')

print(data.head())
print(data.columns)

# From the dataset we can observe the following columns:

# The dataset contains data from 10-2022 until 07-2023 = period

# DocNo - document number for each invoice
# Vendor details - name of the vendors
# Payment block - reason that inhibits the clearing of the invoice
# Processor - someone / something that processed invoices
# Inv receipt date - when the company entered the invoice to the ERP system
# Posting date - when the invoice was processed
# Due date - when the invoice was due to pay
# Clearing date - when the invoice was cleared (most likely end of the process)

# Checking for missing values:
missing_values = data.isnull().sum()
print(missing_values)

# Working on the questions:

# Q1. - Monthly invoice volume
# To calculate this - we need to extract the month and year from the invoice receipt date
data['Year_Month'] = data['Invoice receipt date'].dt.to_period('M')

# Calculate the monthly invoice volume
monthly_invoice_volume = data.groupby('Year_Month').size()

# Basic visualization for the above
# Setting up the figure and axis
fig, ax = plt.subplots(figsize=(12, 6))

# Plot the monthly invoice volume
bars = ax.bar(monthly_invoice_volume.index.astype(str), monthly_invoice_volume.values)

# Set labels and title
ax.set_xlabel('Month-Year')
ax.set_ylabel('Number of Invoices')
ax.set_title('Monthly Invoice Volume')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Highlight the top 3 bars
top_3_indices = monthly_invoice_volume.values.argsort()[-3:][::-1]
colors = ['red' if i in top_3_indices else 'blue' for i in range(len(monthly_invoice_volume))]
for i, bar in enumerate(bars):
    bar.set_color(colors[i])

    # Annotate the bars with their values
    ax.text(bar.get_x() + bar.get_width() / 2 - 0.15,
            bar.get_height() + 20,
            str(int(bar.get_height())),
            ha='center',
            color='black',
            fontsize=10)

plt.tight_layout()
plt.show()

# Q2. To answer this, we'll group the data by the Processor column and
# count the number of invoices for each processor during the whole period.
invoices_per_processor = data.groupby('Processor').size()

# Q3.A - We need to sort the Processors, based on the number of invoices they processed
top_3_processors = invoices_per_processor.sort_values(ascending=False).head(3)

# Basic visualization
plt.figure(figsize=(12, 7))
bars = plt.bar(invoices_per_processor.index, invoices_per_processor.values, color='lightblue')

# Highlighting the top 3 processors and annotating the bars
for i, bar in enumerate(bars):
    processor_name = invoices_per_processor.index[i]
    if processor_name in top_3_processors.index:
        bar.set_color('red')
    # Annotate the bars with their values
    plt.text(bar.get_x() + bar.get_width() / 2,
             bar.get_height() + 10,
             str(int(bar.get_height())),
             ha='center',
             color='black',
             fontsize=10)

# Customize the Plot
plt.xlabel('Processor')
plt.ylabel('Number of Invoices Processed')
plt.title('Number of Invoices Processed by Each Processor')
plt.xticks(rotation=45)
plt.tight_layout()

# Display the plot
plt.show()

# Q3.B -
# To determine how many invoices need to be assigned to a processor on a daily basis, we follow the below steps

# 1. Calculate the average monthly invoice volume
average_monthly_invoice_volume = monthly_invoice_volume.mean()

# Given that the team only has 2 members who are exclusively focusing on invoice processing
num_processors = 2

# 2. Compute the average daily invoice volume, assuming 20 working days in a month
average_daily_invoice_volume = average_monthly_invoice_volume / 20

# 3. Compute the number of invoices per processor per day
invoices_per_processor_per_day = average_daily_invoice_volume / num_processors
print(invoices_per_processor_per_day)

# Q4. What is the average processing and payment time?
# To answer this we will:
# Calculate the processing time as the difference between the 'Posting date and the Invoice receipt date'.
# Calculate the payment time as the difference between the 'Clearing date and the Posting date'.

# Calculate the processing and payment time for each invoice
data['Processing Time'] = (data['Posting date'] - data['Invoice receipt date']).dt.days
data['Payment Time'] = (data['Clearing date'] - data['Posting date']).dt.days

# Compute the average processing and payment times
average_processing_time = round(data['Processing Time'].mean(), 2)
average_payment_time = round(data['Payment Time'].mean(), 2)

print(average_processing_time, average_payment_time)
