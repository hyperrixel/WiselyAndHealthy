"""
WiselyAndHealthy
================

Data source
-----------
Fehring, Richard J., "Menstrual Cycle Data" (2012).
Randomized Comparison of Two Internet-Supported Methods of Natural Family Planning. 7.
https://epublications.marquette.edu/data_nfp/7
"""
from collections import Counter
import numpy as np
import pandas as pd



#############################
# Exploratory Data Analysis #
#############################



# Load the data
data = pd.read_csv('dataset.csv', sep=',')
pd.options.mode.chained_assignment = None
len_data = len(data)



# Show generic information
print('-------------------------------')
data.info()
print('-------------------------------')
print('Count of records: {}'.format(len_data))
print('-------------------------------')


# CONCLUSION: Most of datapoints has issues since except of ClientID they should
#  be sort of int or float instead of object.

# There are a lot of columns that are useless in our case so lets focus on
# important data fields only.



# +----------+
# | Patients |
# +----------+

patient_data_row_counter = Counter()
for id, row in data['ClientID'].iteritems():
    patient_data_row_counter[row] += 1
per_user_rows = sorted(set(patient_data_row_counter.values()))
print('Unique patients: {}'.format(data['ClientID'].nunique()))
print('Data row count per patient between {} - {}'.format(per_user_rows[0], per_user_rows[-1]))



# +--------------+
# | Cycle length |
# +--------------+

print('Cycle length between {} - {}'.format(data['LengthofCycle'].min(), data['LengthofCycle'].max()))



# +---------------------+
# | Luteal phase length |
# +---------------------+

clean_luteal_data = data[data['LengthofLutealPhase'] != ' ']
clean_luteal_data['LengthofLutealPhase'] = pd.to_numeric(clean_luteal_data['LengthofLutealPhase'], downcast='unsigned')
print('Luteal phase length between {} - {} days.'.format(clean_luteal_data['LengthofLutealPhase'].min(),
                                                         clean_luteal_data['LengthofLutealPhase'].max()))
print('--- {} records are good from {}.'.format(len(clean_luteal_data), len_data))



# +-----------------+
# | Ovulation's day |
# +-----------------+

clean_ovulation_data = data[data['EstimatedDayofOvulation'] != ' ']
clean_ovulation_data['EstimatedDayofOvulation'] = pd.to_numeric(clean_ovulation_data['EstimatedDayofOvulation'], downcast='unsigned')
print('Estimated day of ovulation between {} - {} days.'.format(clean_ovulation_data['EstimatedDayofOvulation'].min(),
                                                                clean_ovulation_data['EstimatedDayofOvulation'].max()))
print('--- {} records are good from {}.'.format(len(clean_ovulation_data), len_data))



# +------------------+
# | Length of menses |
# +------------------+

clean_menses_data = data[data['LengthofMenses'] != ' ']
clean_menses_data['LengthofMenses'] = pd.to_numeric(clean_menses_data['LengthofMenses'], downcast='unsigned')
print('Length of menses between {} - {} days.'.format(clean_menses_data['LengthofMenses'].min(),
                                                      clean_menses_data['LengthofMenses'].max()))
print('--- {} records are good from {}.'.format(len(clean_menses_data), len_data))



# +-----+
# | Age |
# +-----+

clean_age_data = data[data['AgeM'] != ' ']
clean_age_data['Age'] = pd.to_numeric(clean_age_data['Age'], downcast='unsigned')
print('Age between {} - {} years.'.format(clean_age_data['Age'].min(),
                                          clean_age_data['Age'].max()))
print('--- {} records are good from {}.'.format(len(clean_age_data), len_data))
age_of_patient = {}
for id, row in clean_age_data[['ClientID', 'Age']].iterrows():
    if row['ClientID'] not in age_of_patient.keys():
        age_of_patient[row['ClientID']] = row['Age']
    else:
        if age_of_patient[row['ClientID']] != row['Age']:
            print('[!] User {} has different age values old: {}, new {}.'.format(row['ClientID'],
                                                                                 age_of_patient[row['ClientID']],
                                                                                 row['Age']))
print('{} patients have age value.'.format(len(age_of_patient)))


#######################
# Creating clean data #
#######################

clean_data = data[data['LengthofLutealPhase'] != ' ']
clean_data = clean_data[clean_data['EstimatedDayofOvulation'] != ' ']
clean_data = clean_data[clean_data['LengthofMenses'] != ' ']
clean_data = clean_data[['ClientID', 'LengthofCycle', 'LengthofLutealPhase', 'EstimatedDayofOvulation', 'LengthofMenses']]
for i, key in enumerate(patient_data_row_counter.keys()):
    clean_data = clean_data.replace(key, i)
print('-------------------------------')
clean_data.info()
print('-------------------------------')
print('Count of records: {}'.format(len(clean_data)))
print('-------------------------------')
clean_data.to_csv('clean_dataset.csv', sep=',', index=False)
