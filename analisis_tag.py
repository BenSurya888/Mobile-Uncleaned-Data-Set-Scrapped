import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from processor_score import processor_score  # structured as {TAG: [ranked_processor_names]}

# 1. Load data yang sudah di-clean
df = pd.read_csv("1.cleaned_mobile_data.csv")
df['tag'] = df['tag'].str.upper()

# 2. Bangun dictionary prosesor -> skor (berdasarkan urutan ranking)
score_map = {}
for tag, proc_list in processor_score.items():
    n = len(proc_list)
    for rank, proc in enumerate(proc_list):
        score_map[(tag, proc)] = round((n - rank) / n, 4)  # Skor dari 1.0 ke 0.0

# 3. Bersihkan Processor_Name_Cleaned jika belum
import re
def clean_proc(name):
    if pd.isna(name):
        return None
    return re.sub(r'\\s+', ' ', name).strip()

df['Processor_Name_Cleaned'] = df['Processor_Name_Cleaned'].apply(clean_proc)

# 4. Buat kolom ProcessorScore berdasarkan tag dan processor name
df['ProcessorScore'] = df.apply(
    lambda row: score_map.get((row['tag'], row['Processor_Name_Cleaned']), None),
    axis=1
)

# 5. Kolom spesifikasi & bobot
spec_cols = {
    'RAM_GB': 0.25,
    'Battery_mAh': 0.20,
    'BackCamera_MP': 0.15,
    'FrontCamera_MP': 0.10,
    'Storage_GB': 0.10,
    'Screen_inches': 0.05,
    'ProcessorScore': 0.15
}

# 6. Fungsi untuk menghitung SpecScore per-tag
def calculate_specscore(df_subset):
    df_subset = df_subset.copy()
    df_subset = df_subset.dropna(subset=spec_cols.keys())
    scaler = MinMaxScaler()
    weighted_score = 0

    for col, weight in spec_cols.items():
        norm = scaler.fit_transform(df_subset[[col]])
        weighted_score += norm.flatten() * weight
        

    df_subset['SpecScore'] = (weighted_score * 50 + 50).round().astype(int)
    if 'Spec Score' in df_subset.columns:
        df_subset.drop(columns=['Spec Score'], inplace=True)

    # Pindahkan SpecScore ke kolom ke-2
    cols = list(df_subset.columns)
    cols.insert(1, cols.pop(cols.index('SpecScore')))
    df_subset = df_subset[cols]

    df_subset = df_subset.sort_values(by='SpecScore', ascending=False).reset_index(drop=True)
    return df_subset

# 7. Hitung dan urutkan SpecScore per tag
df_launched = calculate_specscore(df[df['tag'] == 'LAUNCHED'])
df_rumored = calculate_specscore(df[df['tag'] == 'RUMORED'])
df_upcoming = calculate_specscore(df[df['tag'] == 'UPCOMING'])

# 8. Simpan ke file
df_launched.to_csv("2.analisis_launched.csv", index=False)
df_rumored.to_csv("3.analisis_rumored.csv", index=False)
df_upcoming.to_csv("4.analisis_upcoming.csv", index=False)

print ("==========DONE==========")