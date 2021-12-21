#!/usr/bin/env python
# coding: utf-8

# In[456]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

df = pd.read_csv('C:\\Users\\Mahmoud M. Shehata\\Downloads\\noshowappointments-kagglev2-may-2016.csv')
df.dtypes


# In[457]:


df.head(2)


# In[458]:


#Converting all column names to lowercase for accessibility
df.columns= df.columns.str.lower()
df.rename(columns={"no-show":"no_show"}, inplace=True)


# In[459]:


#Changing the 'ScheduledDay' and 'AppointmentDay' to date format to be more readable
df['scheduledday'] = pd.to_datetime(df['scheduledday'])
df['scheduledday'] = df['scheduledday'].dt.strftime("%m/%d/%y")
df['scheduledday'] = pd.to_datetime(df['scheduledday'])
df['appointmentday'] = pd.to_datetime(df['appointmentday'])
df['appointmentday'] = df['appointmentday'].dt.strftime("%m/%d/%y")
df['appointmentday'] = pd.to_datetime(df['appointmentday'])


# In[460]:


df.head()


# In[461]:


#Checking for incorrect values in age column
df['age'].value_counts()


# In[462]:


#droping rows containing age with -1 or 0
df.drop(df.loc[df['age'] == -1].index, inplace=True)
df.drop(df.loc[df['age'] == 0].index, inplace=True)


# In[463]:


#Confirming rows droping
print((df['age'] == -1).any())
print((df['age'] == 0).any())


# In[464]:


#Checking for incorrect values in handcap column
df.handcap.value_counts()


# In[465]:


df.drop(df.loc[df['handcap'] == 2].index, inplace=True)
df.drop(df.loc[df['handcap'] == 3].index, inplace=True)
df.drop(df.loc[df['handcap'] == 4].index, inplace=True)


# In[466]:


#Confirming rows droping
print((df['handcap'] == 2).any())
print((df['handcap'] == 3).any())
print((df['handcap'] == 4).any())


# In[467]:


#Maping no_show column values to 0 & 1 instead of Yes & No
df["no_show"].replace({'No':'0', 'Yes':'1'}, inplace=True)


# In[469]:


df["no_show"] = df["no_show"].astype(str).astype(int)


# In[455]:


df.dtypes


# In[473]:


#Masking
does_not_show = df.query('no_show == 0')
diabetic = df.query('diabetes == 1')
avg_age = does_not_show['age'].mean()


# In[474]:


avg_age


# In[475]:


avg_low_age = does_not_show.query('age < 39')
avg_high_age = does_not_show.query('age >= 39')


# In[476]:


scholars = does_not_show.query('scholarship == 1')
non_scholars = does_not_show.query('scholarship == 0')
print(scholars.shape)
print(non_scholars.shape)


# In[413]:


########################################################################################################################
df.columns


# In[477]:


does_not_show.head()


# ## First question that popped in my head is : does a single patient miss more than a single appointment ? and how much are these missers ?

# In[564]:


#setting the next visualizations to suitable size
sns.set(rc = {'figure.figsize':(10,8)})

patients = df.groupby('patientid')['no_show']
patient_total = patient_grouped.sum()
patients_mean = patient_grouped.mean()
patient_missed_dist = patient_sum.to_frame().value_counts().to_frame()
p = sns.lineplot(data=patient_missed_dist, x='no_show', y=0)
p.set(ylabel='Number of patients', xlabel='Number of no shows', xticks=list(range(20)));


# ### Looks like the answers is YES, but on the other hand, the majority of patients don't miss much

# ## How about the patient's age ? does it play a role in the game ?

# In[560]:


grouped_ages = df.groupby('age')['no_show']
age_sum = grouped_ages.sum()
age_mean = grouped_ages.mean()
plot = sns.histplot(data=age_sum.to_frame(), x='age', y='no_show', bins=10)
plot.set(ylabel='No-show count')
plt.show()


# ### From the previous plot : As people age, they act more responsibly and don't miss their appointments but that's not the dilemma here, because older people here less appoinments than younger people and I find it weird as we all know that the more people get older, the they need more medical care.
# 

# ## I also wondered, does recieving SMS message have an impact of missing the appointments ?

# In[521]:


# Let's group no-shows by 'SMS_received'
sms_grouped = df.groupby('sms_received')['no_show']
# Let's compute and take a look at the summary statistics
sms_sum = sms_grouped.sum()
sms_mean = sms_grouped.mean()
# Now, it's time to create a histogram
p = sns.histplot(data=sms_sum.to_frame(), x='sms_received', y='no_show', hue='sms_received', palette=['red', 'green'])
p.set(ylim=(0,15000), ylabel='No-show count')
plt.show()


# ### - It seems that people who received SMS messages are more likely to miss their appointments but the difference between receivers and non-receivers isn't much in regards of their count
