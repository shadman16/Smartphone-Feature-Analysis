import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

data = pd.read_excel("flipkart_mobiles.xlsx", sheet_name='data')

print(len(data))
# Filter missing rating
# remove missing values
data.dropna(inplace=True)
# remove duplicates
data['rating'] = data['rating'].astype(float)
data.sort_values(by='rating', ascending=False, inplace=True)
data['brand'] = data['brand'].str.upper()
data['name'] = data['name'].str.upper()
data.drop_duplicates(subset=['brand', 'name'], inplace=True)

# sort
data.sort_values(by='name', inplace=True)
data.reset_index(inplace=True, drop=True)

# prepare final dataframe
final_data = pd.DataFrame()

# Simple columns
# Name
final_data['brand'] = data['brand']
final_data['orig_name'] = data['name']
final_data['name'] = data['name'].apply(lambda x: x[:x.find('(')] if '(' in x else x)
# Price
final_data['price'] = data['price']
final_data['price'] = final_data['price'].apply(lambda x: np.nan if x == 'N/A'
                                                else int(str(x).replace('₹', '').replace(',', '')))
# Rating
final_data['rating'] = data['rating']
# Num rating
data['num_rating_reviews'] = data['num_rating_reviews'].str.replace(',', '').str.replace('Reviews', '').str.replace('Ratings', '')
data[['num_rating', 'num_reviews']] = data['num_rating_reviews'].str.replace(' ', '').str.split('&', 1, expand=True)
final_data['num_rating'] = data['num_rating']
final_data['num_reviews'] = data['num_reviews']
# Display
final_data['display'] = data['display'].apply(lambda x: 'N/A' if x == 'N/A' else float(x[:x.find(' cm')]))
# Battery
final_data['battery_capacity'] = data['battery'].apply(lambda x: 'N/A' if x == 'N/A' else x[:x.find(' mah')])
# Processor
final_data['processor'] = data['processor'].str.replace(' processor', '').str.upper()
final_data['ram_rom'] = data['ram_rom']

# other columns
for i in data.index:
    # split
    ram_rom_exp = data.loc[i, 'ram_rom'].lower().split(' | ')
    # set defaults
    # Ram
    final_data.loc[i, 'ram_gb'] = 'N/A'
    # Rom
    final_data.loc[i, 'storage_gb'] = 'N/A'
    # Expandable
    final_data.loc[i, 'expandable_upto_gb'] = 0
    for item_ram_rom_exp in ram_rom_exp:
        if 'ram' in item_ram_rom_exp:
            final_data.loc[i, 'ram_gb'] = item_ram_rom_exp[:item_ram_rom_exp.find('ram')]
        elif 'rom' in item_ram_rom_exp:
            final_data.loc[i, 'storage_gb'] = item_ram_rom_exp[:item_ram_rom_exp.find('rom')]
        elif 'expandable' in item_ram_rom_exp:
            final_data.loc[i, 'expandable_upto_gb'] = item_ram_rom_exp[len('expandable upto'):]
    # Add model and brand and color
    name_value = data.loc[i, 'name']
    if '(' in name_value:
        final_data.loc[i, 'color'] = name_value[name_value.find('(')+1:name_value.find(',')]
    else:
        final_data.loc[i, 'color'] = 'NOT SPECIFIED'

    # Add Cameras
    camera_text = data.loc[i, 'camera']
    if '|' in camera_text:
        cameras_list = camera_text.split(' | ')
        if 'front' in cameras_list[0]:
            final_data.loc[i, 'Front - Camera'] = cameras_list[0].replace(' front camera', '')
            final_data.loc[i, 'Rear - Camera'] = cameras_list[1].replace(' rear camera', '')
            final_data.loc[i, 'n_rear_cams'] = final_data.loc[i, 'Rear - Camera'].count('+') + 1
            final_data.loc[i, 'n_front_cams'] = final_data.loc[i, 'Rear - Camera'].count('+') + 1
            final_data.loc[i, 'best_rear_cam'] = float(final_data.loc[i, 'Rear - Camera'][
                                                      :final_data.loc[i, 'Rear - Camera'].find('mp')])
            final_data.loc[i, 'best_front_cam'] = float(final_data.loc[i, 'Front - Camera'][
                                                      :final_data.loc[i, 'Front - Camera'].find('mp')])
        else:
            final_data.loc[i, 'Front - Camera'] = cameras_list[1].replace(' front camera', '')
            final_data.loc[i, 'Rear - Camera'] = cameras_list[0].replace(' rear camera', '')
            final_data.loc[i, 'n_rear_cams'] = final_data.loc[i, 'Rear - Camera'].count('+') + 1
            final_data.loc[i, 'best_rear_cam'] = float(final_data.loc[i, 'Rear - Camera'][
                                                      :final_data.loc[i, 'Rear - Camera'].find('mp')])
            final_data.loc[i, 'best_front_cam'] = float(final_data.loc[i, 'Front - Camera'][
                                                       :final_data.loc[i, 'Front - Camera'].find('mp')])
            final_data.loc[i, 'n_front_cams'] = final_data.loc[i, 'Front - Camera'].count('+') + 1
    elif data.loc[i, 'camera'] != 'N/A':
        final_data.loc[i, 'Rear - Camera'] = camera_text.replace(' rear camera', '')
        final_data.loc[i, 'n_rear_cams'] = final_data.loc[i, 'Rear - Camera'].count('+') + 1
        final_data.loc[i, 'best_rear_cam'] = float(final_data.loc[i, 'Rear - Camera'][
                                                  :final_data.loc[i, 'Rear - Camera'].find('mp')])
        final_data.loc[i, 'Front - Camera'] = 'No Front Camera'
        final_data.loc[i, 'best_front_cam'] = 0
        final_data.loc[i, 'n_front_cams'] = 0
    else:
        final_data.loc[i, 'Rear - Camera'] = 0
        final_data.loc[i, 'n_rear_cams'] = 0
        final_data.loc[i, 'best_rear_cam'] = 0
        final_data.loc[i, 'Front - Camera'] = 0
        final_data.loc[i, 'n_front_cams'] = 0

# drop missing values
final_data = final_data.replace('N/A', np.nan)
final_data.dropna(inplace=True)

# finalize ram rom
for col in ['ram_gb', 'storage_gb', 'expandable_upto_gb']:
    final_data[col] = final_data[col].apply(lambda x: x if type(x) != str else
                                            float(x[:x.find('gb')]) if 'gb' in x else
                                            float(x[:x.find('mb')])/1000 if 'mb' in x else
                                            float(x[:x.find('kb')])/1e6 if 'kb' in x else
                                            float(x[:x.find('tb')])*1000)
# drop useless columns
final_data.drop(['Front - Camera', 'Rear - Camera', 'ram_rom', 'orig_name'], axis=1, inplace=True)
# drop duplicates
final_data.drop_duplicates(inplace=True)

print(final_data)
final_data.to_excel("processed_flipkart_mobiles.xlsx", index=False, sheet_name='data')
