# Dependencies
import pandas as pd
import numpy as np
from datetime import datetime as dt
import json

# Read the crowndfunding.xlsx data into a Pandas DataFrame
crowdfunding_info_df = pd.read_excel('Resources/crowdfunding.xlsx', engine='openpyxl')

# Assign the category and subcategory values to category and subcategory columns.
crowdfunding_info_df[['category', 'subcategory']] = crowdfunding_info_df['category & sub-category'].str.split('/', n=2, expand=True)

# Get the unique categories and subcategories in separate lists.
categories = crowdfunding_info_df['category'].unique()
subcategories = crowdfunding_info_df['subcategory'].unique()

# Get the number of categories and subcategories for id creation
len_cat = len(categories)
len_scat = len(subcategories)

# Create numpy arrays for lengths of categories and subcategories
category_ids = np.arange(1, (len_cat + 1))
subcategory_ids = np.arange(1, (len_scat + 1))

# Use a list comprehension to add "cat" to each category_id. 
cat_ids = ['cat'+str(x) for x in category_ids]

# Use a list comprehension to add "subcat" to each subcategory_id.    
scat_ids = ['subcat'+str(x) for x in subcategory_ids]

# Create a category DataFrame with the category_id array as the category_id and categories list as the category name.
category_df = pd.DataFrame({'category_id': cat_ids, 'category': categories})

# Create a category DataFrame with the subcategory_id array as the subcategory_id and subcategories list as the subcategory name. 
subcategory_df = pd.DataFrame({'subcategory_id': scat_ids, 'subcategory': subcategories})

# Export categories_df and subcategories_df as CSV files.
category_df.to_csv("Output/category.csv", index=False)
subcategory_df.to_csv("Output/subcategory.csv", index=False)

# Create a copy of the crowdfunding_info_df DataFrame name campaign_df. 
campaign_df = crowdfunding_info_df.copy()

# Rename the blurb, launched_at, and deadline columns.
campaign_df.rename(columns={'blurb': 'description', 'launched_at': 'launch_date', 'deadline': 'end_date'}, inplace=True)

# Convert the goal and pledged columns to a `float` data type.
campaign_df = campaign_df.astype({'goal': float, 'pledged': float})

# Format the launch_date and end_date columns to datetime format
campaign_df['launch_date'] = pd.to_datetime(campaign_df['launch_date'], unit='s').dt.strftime('%Y-%m-%d')
campaign_df['end_date'] = pd.to_datetime(campaign_df['end_date'], unit='s').dt.strftime('%Y-%m-%d')

# Merge the campaign_df with the category_df on the "category" column and 
# the subcategory_df on the "subcategory" column.
campaign_cat = pd.merge(campaign_df, category_df, on='category', how='left')
campaign_merged_df = pd.merge(campaign_cat, subcategory_df, on='subcategory', how='left')

# Reorder columns and drop unwanted columns
campaign_cleaned = campaign_merged_df[['cf_id', 'contact_id', 'company_name',
                                         'description', 'goal', 'pledged', 'outcome', 'backers_count',
                                         'country', 'currency', 'launch_date', 'end_date', 'category_id',
                                         'subcategory_id']]

# Export the DataFrame as a CSV file. 
campaign_cleaned.to_csv("Output/campaign.csv", index=False)

# Read the contacts.xlsx into a Pandas DataFrame.
contact_info_df = pd.read_excel('Resources/contacts.xlsx', header=2, engine='openpyxl')

# Create two list one for the keys and one for the values.
keys = []
values = []
#  Iterate through the DataFrame.
for i, row in contact_info_df.iterrows():
    data = row[0]
    # Convert each row to a Python dictionary.
    converted_data = json.loads(data)
    # Use a list comprehension to get the keys from the converted data.
    columns = [k for k,v in converted_data.items()]
    # Use a list comprehension to get the values for each row.
    row_values = [v for k, v in converted_data.items()]
    # Append the keys and list values to the lists created.  
    keys.append(columns)
    values.append(row_values)

# Create a contact_info DataFrame and add each list of values, i.e., each row 
# to the 'contact_id', 'name', 'email' columns.
contact_info_df = pd.DataFrame(values, columns=keys[0])

# Split name into first name and last name
contact_info_df[['first_name', 'last_name']] = contact_info_df['name'].str.split(' ', n=2, expand=True)

# Reorder columns and drop unwanted columns
contact_info_df = contact_info_df[['contact_id', 'first_name', 'last_name', 'email']]

# Export the DataFrame as a CSV file. 
contact_info_df.to_csv("Output/contacts.csv", encoding='utf8', index=False)