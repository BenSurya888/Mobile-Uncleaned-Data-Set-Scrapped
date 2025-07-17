import pandas as pd
import re
from processor_score import processor_score 
df = pd.read_csv("mobile.csv")

df_cleaned = df.copy()

df_cleaned['RAM_GB'] = df_cleaned['storage'].str.extract(r'(\\d+)\\s*GB\\s*RAM').astype(float)
df_cleaned['Storage_GB'] = df_cleaned['storage'].str.extract(r'(\\d+)\\s*GB\\s*inbuilt').astype(float)

df_cleaned['Battery_mAh'] = df_cleaned['battery'].str.extract(r'(\\d+)\\s*mAh').astype(float)

df_cleaned['Screen_inches'] = df_cleaned['display'].str.extract(r'([\\d.]+)\\s*inches').astype(float)

df_cleaned['FrontCamera_MP'] = df_cleaned['camera'].str.extract(r'&\\s*(\\d+)\\s*MP').astype(float)

def sum_back_camera(text):
    if isinstance(text, str):
        back_part = text.split('&')[0]
        mps = re.findall(r'(\\d+)\\s*MP', back_part)
        return sum(map(int, mps))
    return None
df_cleaned['BackCamera_MP'] = df_cleaned['camera'].apply(sum_back_camera)

df_cleaned['Processor_Speed_GHz'] = df_cleaned['processor'].str.extract(r'([\\d.]+)\\s*GHz').astype(float)
df_cleaned['Processor_Name'] = df_cleaned['processor'].str.extract(r'^(.*?),')

def clean_proc(name):
    if pd.isna(name):
        return None
    return re.sub(r'\\s+', ' ', name).strip()

df_cleaned['Processor_Name_Cleaned'] = df_cleaned['Processor_Name'].apply(clean_proc)

df_cleaned['tag'] = df_cleaned['tag'].str.upper()
df_cleaned['ProcessorScore'] = df_cleaned['Processor_Name_Cleaned'].map(processor_score)

img = df_cleaned.pop('img')
df_cleaned['img'] = img

df_cleaned.to_csv("1.cleaned_mobile_data.csv", index=False)
print ("==========DONE==========")
