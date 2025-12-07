import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.metrics import classification_report, mean_squared_error, r2_score, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import os
import requests
from io import StringIO

def load_india_data():
    '''Enhanced function to load Indian Agriculture dataset from Kaggle'''
    print('=== LOADING INDIAN AGRICULTURE DATASET ===')
    
    # First try to load from local files (if already downloaded)
    local_paths = [
        'indian_agriculture_dataset.csv',
        'agriculture_dataset.csv', 
        'DATA/indian_agriculture_dataset.csv',
        'data/agriculture_dataset.csv',
        'Agriculture_dataset.csv'
    ]
    
    print('📁 Checking for local dataset files...')
    for path in local_paths:
        if os.path.exists(path):
            try:
                df = pd.read_csv(path)
                print(f'✅ Loaded local file from {path}: {df.shape}')
                return df
            except Exception as e:
                print(f'❌ Error loading {path}: {str(e)}')
                continue
    
    print('❌ Local dataset not found')
    print('\n📝 DATASET INFORMATION:')
    print('- Source: Kaggle - Indian Agriculture Dataset')
    print('- URL: https://www.kaggle.com/datasets/vineetkukreti/indian-agriculture-dataset')
    print('- Content: Agricultural production data across Indian states')
    print('- Features: State, District, Crop, Year, Season, Area, Production')
    
    print('\n🔧 TO DOWNLOAD THE DATASET:')
    print('1. Visit: https://www.kaggle.com/datasets/vineetkukreti/indian-agriculture-dataset')
    print('2. Click "Download" to get the CSV file')
    print('3. Place the downloaded file in your working directory')
    print('4. Rename it to "indian_agriculture_dataset.csv" (optional)')
    
    # Create a sample dataset based on the actual structure for demonstration
    print('\n🏗️ Creating sample Indian Agriculture dataset for demonstration...')
    
    sample_data = {
        'State_Name': ['Uttar Pradesh', 'Maharashtra', 'Punjab', 'Haryana', 'West Bengal'] * 4,
        'District_Name': ['Agra', 'Pune', 'Ludhiana', 'Karnal', 'Kolkata'] * 4,
        'Crop_Year': [2018, 2019, 2020, 2021] * 5,
        'Season': ['Kharif', 'Rabi', 'Summer', 'Kharif', 'Rabi'] * 4,
        'Crop': ['Rice', 'Wheat', 'Sugarcane', 'Cotton', 'Maize'] * 4,
        'Area': np.random.uniform(1000, 50000, 20),  # Area in hectares
        'Production': np.random.uniform(5000, 200000, 20)  # Production in tonnes
    }
    
    df = pd.DataFrame(sample_data)
    print(f'✅ Sample dataset created: {df.shape}')
    print('Note: This is sample data. Please download the actual Kaggle dataset for real analysis.')
    
    return df

def explore_india_data():
    '''Explore and analyze the Indian Agriculture dataset'''
    
    # Load data
    df = load_india_data()
    
    if df is None:
        print('Cannot proceed without data files')
        return
    
    print('\n=== INITIAL DATA EXPLORATION ===')
    print(f'Dataset shape: {df.shape}')
    print('Columns:', df.columns.tolist())
    print('\nFirst few rows:')
    print(df.head())
    
    print('\nData types:')
    print(df.dtypes)
    
    print('\nMissing values:')
    print(df.isnull().sum())
    
    print('\nBasic statistics:')
    print(df.describe())
    
    return df

# Data Collection and Description for Indian Agriculture Dataset
# This section describes the data source and collection methodology

print("=== INDIAN AGRICULTURE DATASET - DATA COLLECTION AND DESCRIPTION ===\n")

# Data Source Information
print("📊 DATA SOURCE:")
print("- Platform: Kaggle")
print("- Dataset: Indian Agriculture Dataset")
print("- URL: https://www.kaggle.com/datasets/vineetkukreti/indian-agriculture-dataset")
print("- Author: Vineet Kukreti")
print("- Collection Method: Kaggle API or Manual Download")
print("- Data Format: CSV (Comma Separated Values)")
print("- License: Open Dataset\n")

# Dataset Context and Domain Information
print("🌾 DOMAIN CONTEXT:")
print("- Domain: Agriculture and Food Production")
print("- Geographic Scope: India (State and District Level)")
print("- Time Period: Multiple years of agricultural data")
print("- Purpose: Analysis of crop production patterns across Indian states")
print("- Use Cases: Agricultural planning, policy making, trend analysis\n")

# Attempt to load and describe the dataset
try:
    # Load the Indian Agriculture dataset
    df = load_india_data()
    
    if df is not None:
        print("✅ DATASET SUCCESSFULLY LOADED\n")
        
        # Basic Dataset Information
        print("📈 DATASET CHARACTERISTICS:")
        print(f"- Total Records: {df.shape[0]:,}")
        print(f"- Total Features: {df.shape[1]}")
        print(f"- Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        print(f"- Data Density: {((df.size - df.isnull().sum().sum()) / df.size * 100):.1f}% non-null values")
        
        # Expected Column Information (based on Kaggle dataset)
        expected_columns = {
            'State_Name': 'Name of the Indian state',
            'District_Name': 'Name of the district within the state',
            'Crop_Year': 'Year when the crop was harvested',
            'Season': 'Agricultural season (Kharif/Rabi/Summer)',
            'Crop': 'Type of crop grown',
            'Area': 'Area under cultivation (hectares)',
            'Production': 'Total production (tonnes)'
        }
        
        print(f"\n📋 COLUMN INFORMATION:")
        for i, col in enumerate(df.columns, 1):
            dtype = str(df[col].dtype)
            non_null = df[col].count()
            null_count = df[col].isnull().sum()
            unique_vals = df[col].nunique()
            
            # Get description if available
            description = expected_columns.get(col, "Data column")
            
            print(f"  {i:2d}. {col:<20} | Type: {dtype:<10} | Non-null: {non_null:,} | Missing: {null_count:,} | Unique: {unique_vals:,}")
            print(f"      Description: {description}")
        
        # Data Types Summary
        print(f"\n🔢 DATA TYPES SUMMARY:")
        dtype_counts = df.dtypes.value_counts()
        for dtype, count in dtype_counts.items():
            print(f"- {dtype}: {count} columns")
        
        # Agricultural Context Analysis
        print(f"\n🌾 AGRICULTURAL DATA ANALYSIS:")
        
        # Check for key agricultural columns
        if 'State_Name' in df.columns or 'State' in df.columns:
            state_col = 'State_Name' if 'State_Name' in df.columns else 'State'
            unique_states = df[state_col].nunique()
            print(f"- Geographic Coverage: {unique_states} states/regions")
            if unique_states <= 15:
                print(f"  Top states: {list(df[state_col].value_counts().head(5).index)}")
        
        if 'Crop' in df.columns:
            unique_crops = df['Crop'].nunique()
            print(f"- Crop Diversity: {unique_crops} different crops")
            if unique_crops <= 20:
                print(f"  Main crops: {list(df['Crop'].value_counts().head(5).index)}")
        
        if 'Crop_Year' in df.columns or 'Year' in df.columns:
            year_col = 'Crop_Year' if 'Crop_Year' in df.columns else 'Year'
            year_range = f"{df[year_col].min()}-{df[year_col].max()}"
            print(f"- Time Period: {year_range}")
            print(f"- Years of data: {df[year_col].nunique()} years")
        
        if 'Season' in df.columns:
            seasons = list(df['Season'].unique())
            print(f"- Seasons covered: {seasons}")
        
        # Production and Area Statistics
        if 'Production' in df.columns:
            total_production = df['Production'].sum()
            print(f"- Total Production: {total_production:,.0f} tonnes")
            print(f"- Average Production per record: {df['Production'].mean():,.1f} tonnes")
        
        if 'Area' in df.columns:
            total_area = df['Area'].sum()
            print(f"- Total Area: {total_area:,.0f} hectares")
            print(f"- Average Area per record: {df['Area'].mean():,.1f} hectares")
        
        # Missing Data Overview
        total_missing = df.isnull().sum().sum()
        missing_percentage = (total_missing / (df.shape[0] * df.shape[1])) * 100
        print(f"\n❌ MISSING DATA OVERVIEW:")
        print(f"- Total Missing Values: {total_missing:,}")
        print(f"- Missing Data Percentage: {missing_percentage:.2f}%")
        
        if total_missing > 0:
            print("\nColumns with Missing Values:")
            missing_data = df.isnull().sum()[df.isnull().sum() > 0].sort_values(ascending=False)
            for col, missing in missing_data.items():
                percentage = (missing / len(df)) * 100
                print(f"  - {col}: {missing:,} ({percentage:.1f}%)")
        else:
            print("✅ No missing values detected!")
        
        # Data Quality Insights
        print(f"\n🔍 DATA QUALITY INSIGHTS:")
        
        # Check for potential data quality issues
        quality_notes = []
        
        if 'Production' in df.columns:
            zero_production = (df['Production'] == 0).sum()
            if zero_production > 0:
                quality_notes.append(f"Zero production records: {zero_production}")
        
        if 'Area' in df.columns:
            zero_area = (df['Area'] == 0).sum()
            if zero_area > 0:
                quality_notes.append(f"Zero area records: {zero_area}")
        
        duplicate_records = df.duplicated().sum()
        if duplicate_records > 0:
            quality_notes.append(f"Duplicate records: {duplicate_records}")
        
        if quality_notes:
            for note in quality_notes:
                print(f"  ⚠️  {note}")
        else:
            print("  ✅ No obvious data quality issues detected")
    
    else:
        print("❌ DATASET NOT FOUND")
        print("Please download the dataset from Kaggle:")
        print("https://www.kaggle.com/datasets/vineetkukreti/indian-agriculture-dataset")

except Exception as e:
    print(f"❌ ERROR LOADING DATASET: {str(e)}")
    print("\n📝 EXPECTED DATASET STRUCTURE:")
    print("Based on the Kaggle Indian Agriculture Dataset:")
    print("- State_Name: Name of Indian states")
    print("- District_Name: District within each state") 
    print("- Crop_Year: Year of crop harvest")
    print("- Season: Agricultural season (Kharif/Rabi/Summer)")
    print("- Crop: Type of crop (Rice, Wheat, Cotton, etc.)")
    print("- Area: Area under cultivation in hectares")
    print("- Production: Total production in tonnes")

print("\n" + "="*70)
print("Next Step: Download dataset from Kaggle and proceed with analysis")
print("="*70)