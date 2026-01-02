#!/usr/bin/env python
# coding: utf-8

# In[1]:


# pipeline_functions.py
import pandas as pd
import numpy as np
from datetime import datetime

def load_and_profile(df):
    report = f"""
INITIAL DATA PROFILING REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Rows: {len(df):,}
Columns: {list(df.columns)}
Timestamp range: {df['timestamp'].min()} → {df['timestamp'].max()}

Missing values:
{df.isnull().sum()[df.isnull().sum() > 0]}

Duplicates: {df.duplicated().sum()}
Negative prices: {(df['price'] < 0).sum()}
Zero volumes: {(df['volume'] == 0).sum()}
"""
    return report

def validate_and_flag(df):
    df = df.sort_values('timestamp').reset_index(drop=True)
    
    df['is_missing_price'] = df['price'].isna()
    df['is_negative_price'] = df['price'] < 0
    df['is_zero_volume'] = df['volume'] == 0
    
    valid_prices = df['price'].dropna()
    if len(valid_prices) > 0:
        z = np.abs((valid_prices - valid_prices.mean()) / valid_prices.std())
        df['is_outlier_z'] = (z > 3).reindex(df.index, fill_value=False)
        
        Q1, Q3 = valid_prices.quantile([0.25, 0.75])
        IQR = Q3 - Q1
        df['is_outlier_iqr'] = ((df['price'] < Q1 - 1.5*IQR) | (df['price'] > Q3 + 1.5*IQR)) & (~df['price'].isna())
    
    time_diffs = df['timestamp'].diff().dt.total_seconds().fillna(0)
    df['is_gap_large'] = time_diffs > 10
    
    df['is_anomaly'] = df[['is_missing_price', 'is_negative_price', 'is_zero_volume',
                           'is_outlier_z', 'is_outlier_iqr', 'is_gap_large']].any(axis=1)
    
    anomaly_count = df['is_anomaly'].sum()
    return df, anomaly_count

def clean_data(df):
    original_rows = len(df)
    
    # Deduplicate
    df = df.drop_duplicates(subset=['timestamp', 'exchange', 'price', 'volume'], keep='first')
    
    # Interpolate missing prices
    df['price'] = df['price'].interpolate(method='linear', limit_direction='both')
    
    # Cap outliers robustly
    positive_prices = df['price'][df['price'] > 0]
    lower = max(positive_prices.quantile(0.001), 0.01)
    upper = positive_prices.quantile(0.999)
    df['price'] = df['price'].clip(lower, upper)
    
    # Remove invalid
    invalid = (df['price'] < 0) | (df['is_zero_volume'])
    df = df[~invalid].copy()
    
    cleaned_rows = len(df)
    return df, original_rows, cleaned_rows


# In[ ]:




