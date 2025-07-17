import pandas as pd

df_launched = pd.read_csv("2.analisis_launched.csv")
df_rumored = pd.read_csv("3.analisis_rumored.csv")
df_upcoming = pd.read_csv("4.analisis_upcoming.csv")

threshold = df_launched['SpecScore'].quantile(0.75)

launched_scores = df_launched[['Name', 'SpecScore']].copy()

def find_worth_it(df_input):
    filtered = df_input[df_input['SpecScore'] >= threshold].copy()
    enriched_rows = []

    for _, row in filtered.iterrows():
        name = row['Name']
        score = row['SpecScore']

        launched_scores['ScoreDiff'] = (launched_scores['SpecScore'] - score).abs()
        closest = launched_scores.loc[launched_scores['ScoreDiff'].idxmin()]

        enriched = row.to_dict()
        enriched['Closest_Launched'] = closest['Name']
        enriched['Launched_SpecScore'] = closest['SpecScore']
        enriched['ScoreDifference'] = closest['ScoreDiff']
        enriched_rows.append(enriched)

    df_result = pd.DataFrame(enriched_rows)
    df_result = df_result.sort_values(by='SpecScore', ascending=False).reset_index(drop=True)
    df_result.index += 1
    df_result.insert(0, 'Rank', df_result.index)
    return df_result

df_worth_rumored = find_worth_it(df_rumored)
df_worth_upcoming = find_worth_it(df_upcoming)

df_worth_rumored.to_csv("5.final_rumored.csv", index=False)
df_worth_upcoming.to_csv("6.final_upcoming.csv", index=False)
print ("==========DONE==========")