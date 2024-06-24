import pandas as pd
import numpy as np
from scipy import stats


data = {
    'transaction_id': ['TRX001', 'TRX002', 'TRX003', 'TRX004', 'TRX005', 'TRX006', 'TRX007'],
    'date': ['2024-06-01', '2024-06-01', '2024-06-01', '2024-06-02', '2024-06-02', '2024-06-03', '2024-06-03'],
    'category': ['Food', 'Utilities', 'Entertainment', 'Food', 'Transport', 'Utilities', 'Food'],
    'amount': [25.00, 150.00, 200.00, 3000.00, 45.00, 135.00, 20.00]
}


df = pd.DataFrame(data)


df['date'] = pd.to_datetime(df['date'])

def detect_anomalies(df, threshold=3):
    anomalies = []
    for category in df['category'].unique():
        category_df = df[df['category'] == category]


        mean = category_df['amount'].mean()
        std = category_df['amount'].std()


        print(f"Category: {category}")
        print(f"Mean: {mean}")
        print(f"Standard Deviation: {std}")

        if std == 0:
            continue


        z_scores = (category_df['amount'] - mean) / std


        print(f"Z-scores:\n{z_scores}")

        category_anomalies = category_df[np.abs(z_scores) > threshold]
        for index, row in category_anomalies.iterrows():
            anomalies.append({
                'transaction_id': row['transaction_id'],
                'date': row['date'].strftime('%Y-%m-%d'),
                'category': row['category'],
                'amount': row['amount'],
                'reason_for_anomaly': f'{z_scores.loc[index]:.2f} standard deviations from the mean'
            })
    return anomalies

anomalies = detect_anomalies(df, threshold=3)


if anomalies:
    for anomaly in anomalies:
        print(anomaly)
else:
    print("No anomalies detected")


report = pd.DataFrame(anomalies)
print(report)
