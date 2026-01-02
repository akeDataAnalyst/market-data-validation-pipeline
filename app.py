#!/usr/bin/env python
# coding: utf-8

# In[3]:


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pipeline_functions import load_and_profile, validate_and_flag, clean_data
from datetime import datetime

st.set_page_config(page_title="Market Data Validation Pipeline", layout="wide")
st.title("🧹 Market Data Validation & Cleaning Tool")
st.markdown("Built for quantitative research support — validates, cleans, and prepares tick data for analysis.")

uploaded_file = st.file_uploader("Upload raw market data CSV", type=['csv'])

if uploaded_file is not None:
    try:
        df_raw = pd.read_csv(uploaded_file, parse_dates=['timestamp'])
        required_cols = ['timestamp', 'price', 'volume']
        if not all(col in df_raw.columns for col in required_cols):
            st.error(f"CSV must contain columns: {required_cols}")
        else:
            st.success(f"Loaded {len(df_raw):,} rows successfully.")
            
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Profiling", "⚠️ Validation", "🧹 Cleaning", "📥 Download"])
            
            with tab1:
                st.subheader("Initial Profiling Report")
                report = load_and_profile(df_raw)
                st.text(report)
                
                st.subheader("Raw Price Series")
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.plot(df_raw['timestamp'], df_raw['price'], label='Raw Price', alpha=0.7)
                ax.set_title("Raw Price Time Series")
                ax.set_ylabel("Price")
                st.pyplot(fig)
            
            with tab2:
                df_flagged, anomaly_count = validate_and_flag(df_raw.copy())
                st.subheader(f"Anomaly Detection Results: {anomaly_count:,} flagged rows")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write("Flagged Anomalies Breakdown")
                    breakdown = {
                        'Missing Prices': df_flagged['is_missing_price'].sum(),
                        'Negative Prices': df_flagged['is_negative_price'].sum(),
                        'Zero Volume': df_flagged['is_zero_volume'].sum(),
                        'Z-Score Outliers': df_flagged['is_outlier_z'].sum(),
                        'IQR Outliers': df_flagged['is_outlier_iqr'].sum(),
                        'Large Gaps': df_flagged['is_gap_large'].sum(),
                    }
                    st.json(breakdown)
                
                with col2:
                    st.write("Sample Anomalous Rows")
                    st.dataframe(df_flagged[df_flagged['is_anomaly']].head(10))
            
            with tab3:
                st.subheader("Run Cleaning Pipeline")
                if st.button("🧹 Clean Data Now"):
                    with st.spinner("Cleaning in progress..."):
                        df_clean, original, final = clean_data(df_raw.copy())
                    
                    st.success(f"Cleaning complete! {original:,} → {final:,} rows")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("Before vs After Price Series")
                        fig, ax = plt.subplots(figsize=(10, 5))
                        ax.plot(df_raw['timestamp'], df_raw['price'], label='Raw', alpha=0.6)
                        ax.plot(df_clean['timestamp'], df_clean['price'], label='Cleaned', linewidth=2)
                        ax.legend()
                        ax.set_title("Price Series: Before and After Cleaning")
                        st.pyplot(fig)
                    
                    with col2:
                        st.write("Final Clean Data Preview")
                        st.dataframe(df_clean.head(10))
                    
                    st.session_state.df_clean = df_clean  # Save for download
            
            with tab4:
                st.subheader("Download Results")
                if 'df_clean' in st.session_state:
                    clean_csv = st.session_state.df_clean.to_csv(index=False).encode()
                    st.download_button(
                        label="📄 Download Clean Dataset",
                        data=clean_csv,
                        file_name=f"clean_market_data_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                    st.success("Ready for research!")
                else:
                    st.info("Run cleaning first to enable download.")
                    
    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info("👆 Upload a CSV to begin. Example files are included in the repo.")
    st.markdown("### Demo with included sample?")
    if st.button("Load Demo Dataset"):
        df_raw = pd.read_csv('raw_market_data_with_errors.csv', parse_dates=['timestamp'])
        st.session_state.uploaded_file = True
        st.rerun()


# In[ ]:




