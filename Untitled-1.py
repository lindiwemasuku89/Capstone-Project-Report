# STEP 1: Download and Load the India Dataset from GitHub Repository
# Repository: https://github.com/lindiwemasuku89/Capstone-Project-Report

import pandas as pd
import numpy as np
import os
import requests
from io import StringIO

print("=== STEP 1: DOWNLOADING AND LOADING INDIA DATASET ===\n")

def download_india_dataset():
    """Download the India dataset from the GitHub repository"""
    
    # GitHub repository details
    repo_url = "https://github.com/lindiwemasuku89/Capstone-Project-Report"
    
    # Try different possible dataset file locations in the repository
    possible_files = [
        "https://raw.githubusercontent.com/lindiwemasuku89/Capstone-Project-Report/main/data.csv",
        "https://raw.githubusercontent.com/lindiwemasuku89/Capstone-Project-Report/main/dataset.csv",
        "https://raw.githubusercontent.com/lindiwemasuku89/Capstone-Project-Report/main/india_data.csv",
        "https://raw.githubusercontent.com/lindiwemasuku89/Capstone-Project-Report/main/Data/data.csv",
        "https://raw.githubusercontent.com/lindiwemasuku89/Capstone-Project-Report/master/data.csv",
        "https://raw.githubusercontent.com/lindiwemasuku89/Capstone-Project-Report/master/dataset.csv"
    ]
    
    print("🔍 SEARCHING FOR DATASET IN REPOSITORY...")
    print(f"Repository: {repo_url}\n")
    
    for i, file_url in enumerate(possible_files, 1):
        try:
            print(f"Attempt {i}: Trying {file_url.split('/')[-1]}...")
            
            response = requests.get(file_url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ Found dataset at: {file_url}")
                
                # Try to read the CSV content
                df = pd.read_csv(StringIO(response.text))
                
                # Save locally for future use
                local_filename = "india_dataset.csv"
                df.to_csv(local_filename, index=False)
                print(f"💾 Saved locally as: {local_filename}")
                
                return df, file_url
                
            else:
                print(f"❌ Not found (Status: {response.status_code})")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print(f"\n⚠️ Could not find dataset automatically.")
    print(f"Please manually check the repository: {repo_url}")
    print(f"Look for CSV files and update the file paths in the code.")
    
    return None, None

def load_local_dataset():
    """Try to load dataset from local files"""
    
    print("🔍 CHECKING FOR LOCAL DATASET FILES...")
    
    local_files = [
        "india_dataset.csv",
        "data.csv", 
        "dataset.csv",
        "india_data.csv",
        "Data/data.csv",
        "Data/dataset.csv"
    ]
    
    for file_path in local_files:
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                print(f"✅ Loaded local file: {file_path}")
                return df, file_path
            except Exception as e:
                print(f"❌ Error loading {file_path}: {str(e)}")
    
    return None, None

# Main loading process
print("📊 LOADING INDIA DATASET...")
print("="*50)

# First try to download from GitHub
df, source_url = download_india_dataset()

# If download fails, try local files
if df is None:
    print("\n📁 TRYING LOCAL FILES...")
    df, source_file = load_local_dataset()
    
    if df is None:
        print("\n❌ DATASET NOT FOUND")
        print("\n🔧 MANUAL STEPS TO GET THE DATASET:")
        print("1. Visit: https://github.com/lindiwemasuku89/Capstone-Project-Report")
        print("2. Look for CSV files in the repository")
        print("3. Download the dataset file")
        print("4. Place it in your working directory")
        print("5. Update the filename in the code if needed")
        
        # Create a sample dataset structure for demonstration
        print("\n🏗️ CREATING SAMPLE DATASET STRUCTURE FOR TESTING...")
        sample_data = {
            'State': ['Maharashtra', 'Karnataka', 'Tamil Nadu', 'Gujarat', 'Rajasthan'],
            'Population': [112000000, 61000000, 72000000, 60000000, 68000000],
            'GDP': [32.5, 21.6, 23.1, 20.8, 11.9],
            'Literacy_Rate': [82.3, 75.4, 80.1, 78.0, 66.1],
            'Urban_Population_Pct': [45.2, 38.7, 48.4, 42.6, 24.9]
        }
        df = pd.DataFrame(sample_data)
        print("✅ Sample dataset created for demonstration")

# Dataset loaded successfully
if df is not None:
    print("\n" + "="*60)
    print("✅ DATASET LOADED SUCCESSFULLY!")
    print("="*60)
    
    # Basic dataset information
    print(f"\n📈 DATASET OVERVIEW:")
    print(f"- Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"- Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # Display first few rows
    print(f"\n📋 FIRST 5 ROWS:")
    print(df.head())
    
    # Column information
    print(f"\n🏷️ COLUMN INFORMATION:")
    for i, (col, dtype) in enumerate(df.dtypes.items(), 1):
        non_null = df[col].count()
        null_count = df[col].isnull().sum()
        print(f"{i:2d}. {col:<20} | Type: {str(dtype):<10} | Non-null: {non_null:,} | Missing: {null_count:,}")
    
    # Missing values summary
    total_missing = df.isnull().sum().sum()
    print(f"\n❌ MISSING DATA SUMMARY:")
    print(f"- Total missing values: {total_missing:,}")
    print(f"- Missing percentage: {(total_missing / df.size * 100):.2f}%")
    
    # Store for next steps
    globals()['india_df'] = df
    print(f"\n✅ Dataset stored in variable 'india_df'")
    
print("\n" + "="*60)
print("STEP 1 COMPLETE - READY FOR DATA CLEANING")
print("="*60)

# Data Cleaning and Filtering - India Dataset
# This section handles missing values, outliers, and data quality issues

print("=== DATA CLEANING AND FILTERING SECTION ===\n")

# Check if we have data loaded from previous section
try:
    # Try to use the dataframe from the loading section
    if 'india_df' in globals():
        df = india_df.copy()  # Work with a copy to preserve original data
        print("✅ Using previously loaded dataset")
    else:
        # Load fresh if not available
        df = load_india_data()
        if df is None:
            print("❌ No data available for cleaning")
            raise Exception("Dataset not found")
    
    print(f"📊 Starting with dataset shape: {df.shape}")
    
    # ===== STEP 1: INITIAL DATA ASSESSMENT =====
    print("\n" + "="*60)
    print("STEP 1: INITIAL DATA ASSESSMENT")
    print("="*60)
    
    # Check basic information
    print("📋 COLUMN DATA TYPES:")
    for col, dtype in df.dtypes.items():
        print(f"- {col}: {dtype}")
    
    # Missing values analysis
    print(f"\n❌ MISSING VALUES ANALYSIS:")
    missing_summary = df.isnull().sum()
    missing_cols = missing_summary[missing_summary > 0]
    
    if len(missing_cols) > 0:
        print("Columns with missing values:")
        for col, missing_count in missing_cols.items():
            missing_pct = (missing_count / len(df)) * 100
            print(f"- {col}: {missing_count} ({missing_pct:.2f}%)")
    else:
        print("✅ No missing values found!")
    
    # ===== STEP 2: HANDLE MISSING VALUES =====
    print("\n" + "="*60)
    print("STEP 2: HANDLING MISSING VALUES")
    print("="*60)
    
    # Store original shape for comparison
    original_shape = df.shape
    
    # Handle missing values based on data type and percentage
    for col in df.columns:
        missing_count = df[col].isnull().sum()
        missing_pct = (missing_count / len(df)) * 100
        
        if missing_count > 0:
            print(f"\n🔧 Processing column '{col}' ({missing_pct:.2f}% missing):")
            
            if missing_pct > 50:
                # If more than 50% missing, consider dropping the column
                print(f"   ⚠️  High missing percentage - consider dropping column")
                print(f"   Action: Keeping for now, but flagged for review")
                
            elif df[col].dtype in ['object', 'category']:
                # For categorical data, fill with mode or 'Unknown'
                if df[col].mode().empty:
                    df[col].fillna('Unknown', inplace=True)
                    print(f"   ✅ Filled with 'Unknown'")
                else:
                    mode_value = df[col].mode().iloc[0]
                    df[col].fillna(mode_value, inplace=True)
                    print(f"   ✅ Filled with mode: '{mode_value}'")
                    
            elif df[col].dtype in ['int64', 'float64']:
                # For numerical data, use median (more robust than mean)
                median_value = df[col].median()
                df[col].fillna(median_value, inplace=True)
                print(f"   ✅ Filled with median: {median_value}")
    
    # ===== STEP 3: REMOVE DUPLICATES =====
    print("\n" + "="*60)
    print("STEP 3: REMOVE DUPLICATE ROWS")
    print("="*60)
    
    duplicate_count = df.duplicated().sum()
    print(f"🔍 Found {duplicate_count} duplicate rows")
    
    if duplicate_count > 0:
        df.drop_duplicates(inplace=True)
        print(f"✅ Removed {duplicate_count} duplicate rows")
    else:
        print("✅ No duplicate rows found")
    
    # ===== STEP 4: OUTLIER DETECTION =====
    print("\n" + "="*60)
    print("STEP 4: OUTLIER DETECTION")
    print("="*60)
    
    # Get numerical columns
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numerical_cols) > 0:
        print(f"📊 Analyzing outliers in {len(numerical_cols)} numerical columns:")
        
        outlier_summary = {}
        
        for col in numerical_cols:
            # Use IQR method for outlier detection
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            # Define outlier bounds
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Count outliers
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            outlier_count = len(outliers)
            outlier_pct = (outlier_count / len(df)) * 100
            
            outlier_summary[col] = {
                'count': outlier_count,
                'percentage': outlier_pct,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound
            }
            
            print(f"- {col}: {outlier_count} outliers ({outlier_pct:.2f}%)")
            
        # Option to remove outliers (conservative approach - only if < 5% of data)
        print(f"\n🔧 OUTLIER TREATMENT:")
        for col, info in outlier_summary.items():
            if info['percentage'] > 0 and info['percentage'] < 5:
                print(f"- {col}: Outliers within acceptable range ({info['percentage']:.2f}%)")
                # Optionally cap outliers instead of removing
                # df[col] = df[col].clip(lower=info['lower_bound'], upper=info['upper_bound'])
            elif info['percentage'] >= 5:
                print(f"- {col}: High outlier percentage ({info['percentage']:.2f}%) - keeping for domain analysis")
            else:
                print(f"- {col}: No outliers detected")
    
    else:
        print("ℹ️ No numerical columns found for outlier analysis")
    
    # ===== STEP 5: DATA TYPE OPTIMIZATION =====
    print("\n" + "="*60)
    print("STEP 5: DATA TYPE OPTIMIZATION")
    print("="*60)
    
    print("🔧 Optimizing data types for memory efficiency:")
    
    # Convert object columns that should be categorical
    for col in df.select_dtypes(include=['object']).columns:
        unique_ratio = df[col].nunique() / len(df)
        if unique_ratio < 0.1:  # If less than 10% unique values, convert to category
            df[col] = df[col].astype('category')
            print(f"- {col}: converted to category ({df[col].nunique()} unique values)")
    
    # ===== STEP 6: FINAL DATA VALIDATION =====
    print("\n" + "="*60)
    print("STEP 6: FINAL DATA VALIDATION")
    print("="*60)
    
    # Final statistics
    final_shape = df.shape
    rows_removed = original_shape[0] - final_shape[0]
    
    print("📈 CLEANING SUMMARY:")
    print(f"- Original shape: {original_shape}")
    print(f"- Final shape: {final_shape}")
    print(f"- Rows removed: {rows_removed}")
    print(f"- Data retention: {(final_shape[0]/original_shape[0]*100):.2f}%")
    
    # Check for any remaining missing values
    remaining_missing = df.isnull().sum().sum()
    print(f"- Remaining missing values: {remaining_missing}")
    
    # Memory usage
    memory_usage = df.memory_usage(deep=True).sum() / 1024**2
    print(f"- Memory usage: {memory_usage:.2f} MB")
    
    # Store cleaned dataset
    globals()['cleaned_df'] = df
    print(f"\n✅ Cleaned dataset stored in variable 'cleaned_df'")
    
    print("\n" + "="*80)
    print("DATA CLEANING SECTION COMPLETE")
    print("="*80)

except Exception as e:
    print(f"❌ ERROR DURING DATA CLEANING: {str(e)}")
    print("\n🔧 TROUBLESHOOTING:")
    print("1. Ensure data was loaded in the previous section")
    print("2. Check that the dataset has valid structure")
    print("3. Verify sufficient memory for processing")