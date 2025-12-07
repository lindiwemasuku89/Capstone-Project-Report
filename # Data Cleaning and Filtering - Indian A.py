# Data Cleaning and Filtering - Indian Agriculture Dataset
# This section handles missing values, outliers, and data quality issues

print("=== DATA CLEANING AND FILTERING SECTION ===\n")

# Import additional libraries for data cleaning
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

try:
    # Use data from previous loading section
    if 'india_df' in globals():
        df = india_df.copy()  # Work with copy to preserve original
        print("✅ Using dataset from loading section")
        print(f"📊 Starting dataset shape: {df.shape}\n")
    else:
        # Load fresh if not available
        df = load_india_data()
        if df is None:
            # Create sample agricultural dataset for demonstration
            print("📝 Creating sample Indian Agriculture dataset for cleaning demonstration...")
            sample_data = {
                'State_Name': ['Uttar Pradesh', 'Maharashtra', 'Punjab', 'Haryana', 'West Bengal', 
                              'Karnataka', 'Gujarat', None, 'Tamil Nadu', 'Rajasthan'] * 3,
                'District_Name': ['Agra', 'Pune', 'Ludhiana', 'Karnal', 'Kolkata', 
                                 'Bangalore', 'Ahmedabad', 'Unknown', 'Chennai', 'Jaipur'] * 3,
                'Crop_Year': [2018, 2019, 2020, 2021, 2022, 2018, 2019, 2020, 2021, None] * 3,
                'Season': ['Kharif', 'Rabi', 'Summer', 'Kharif', 'Rabi', 
                          'Summer', 'Kharif', None, 'Rabi', 'Summer'] * 3,
                'Crop': ['Rice', 'Wheat', 'Sugarcane', 'Cotton', 'Maize', 
                        'Soybean', 'Groundnut', 'Barley', None, 'Mustard'] * 3,
                'Area': [1500.5, 2300.0, 1800.2, 2100.8, None, 
                        1200.3, 1900.7, 2500.0, 1100.5, 3200.0] * 3,
                'Production': [4500.2, 6800.5, 12000.0, 3200.8, 2800.3, 
                              None, 2100.5, 5800.0, 1800.2, 9500.0] * 3
            }
            df = pd.DataFrame(sample_data)
            print("✅ Sample agricultural dataset created for demonstration")
            print(f"📊 Sample dataset shape: {df.shape}\n")
    
    # ===== STEP 1: INITIAL DATA ASSESSMENT =====
    print("=" * 70)
    print("STEP 1: INITIAL DATA ASSESSMENT")
    print("=" * 70)
    
    # Display basic information
    print("📋 DATASET OVERVIEW:")
    print(f"- Shape: {df.shape}")
    print(f"- Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # Check data types and unique values
    print(f"\n📊 COLUMN ANALYSIS:")
    for col in df.columns:
        dtype = df[col].dtype
        unique_count = df[col].nunique()
        null_count = df[col].isnull().sum()
        print(f"- {col:<18}: {str(dtype):<12} | Unique: {unique_count:,} | Missing: {null_count:,}")
    
    # Missing values analysis
    print(f"\n❌ MISSING VALUES ANALYSIS:")
    missing_summary = df.isnull().sum()
    total_missing = missing_summary.sum()
    
    if total_missing > 0:
        print(f"Total missing values: {total_missing:,}")
        print("Missing values by column:")
        for col in missing_summary.index:
            missing_count = missing_summary[col]
            if missing_count > 0:
                missing_pct = (missing_count / len(df)) * 100
                print(f"  - {col}: {missing_count:,} ({missing_pct:.1f}%)")
    else:
        print("✅ No missing values detected")
    
    # ===== STEP 2: STANDARDIZE COLUMN NAMES =====
    print(f"\n" + "=" * 70)
    print("STEP 2: STANDARDIZE COLUMN NAMES")
    print("=" * 70)
    
    # Mapping for common column name variations in agricultural datasets
    column_mapping = {
        'State_Name': 'State_Name', 'State': 'State_Name', 'state': 'State_Name',
        'District_Name': 'District_Name', 'District': 'District_Name', 'district': 'District_Name',
        'Crop_Year': 'Crop_Year', 'Year': 'Crop_Year', 'year': 'Crop_Year',
        'Season': 'Season', 'season': 'Season',
        'Crop': 'Crop', 'crop': 'Crop',
        'Area': 'Area', 'area': 'Area', 'Area_hectares': 'Area',
        'Production': 'Production', 'production': 'Production', 'Production_tonnes': 'Production'
    }
    
    original_columns = df.columns.tolist()
    renamed_count = 0
    
    for old_name, new_name in column_mapping.items():
        if old_name in df.columns and old_name != new_name:
            df.rename(columns={old_name: new_name}, inplace=True)
            print(f"   ✅ Renamed '{old_name}' → '{new_name}'")
            renamed_count += 1
    
    if renamed_count == 0:
        print("   ℹ️  No column renaming needed")
    
    print(f"   📋 Final columns: {list(df.columns)}")
    
    # ===== STEP 3: CLEAN CATEGORICAL DATA =====
    print(f"\n" + "=" * 70)
    print("STEP 3: CLEAN CATEGORICAL DATA")
    print("=" * 70)
    
    # Clean State Names
    if 'State_Name' in df.columns:
        print("🔧 Cleaning State Names:")
        before_cleaning = df['State_Name'].nunique()
        
        # Remove whitespace and standardize case
        df['State_Name'] = df['State_Name'].astype(str).str.strip().str.title()
        
        # Standardize common state name variations
        state_replacements = {
            'Uttar Pradesh': 'Uttar Pradesh',
            'West Bengal': 'West Bengal',
            'Tamil Nadu': 'Tamil Nadu',
            'Andhra Pradesh': 'Andhra Pradesh',
            'Madhya Pradesh': 'Madhya Pradesh',
            'Himachal Pradesh': 'Himachal Pradesh',
            'Arunachal Pradesh': 'Arunachal Pradesh',
            'Nan': None  # Handle 'nan' strings
        }
        
        df['State_Name'] = df['State_Name'].replace(state_replacements)
        after_cleaning = df['State_Name'].nunique()
        print(f"   📊 States before cleaning: {before_cleaning}")
        print(f"   📊 States after cleaning: {after_cleaning}")
    
    # Clean Crop Names
    if 'Crop' in df.columns:
        print(f"\n🔧 Cleaning Crop Names:")
        before_cleaning = df['Crop'].nunique()
        
        # Standardize crop names
        df['Crop'] = df['Crop'].astype(str).str.strip().str.title()
        
        # Standardize common crop variations
        crop_replacements = {
            'Rice': 'Rice',
            'Wheat': 'Wheat',
            'Sugarcane': 'Sugarcane',
            'Sugar Cane': 'Sugarcane',
            'Cotton': 'Cotton',
            'Cotton(Lint)': 'Cotton',
            'Maize': 'Maize',
            'Corn': 'Maize',
            'Groundnut': 'Groundnut',
            'Ground Nut': 'Groundnut',
            'Nan': None
        }
        
        df['Crop'] = df['Crop'].replace(crop_replacements)
        after_cleaning = df['Crop'].nunique()
        print(f"   📊 Crops before cleaning: {before_cleaning}")
        print(f"   📊 Crops after cleaning: {after_cleaning}")
    
    # Clean Season Names
    if 'Season' in df.columns:
        print(f"\n🔧 Cleaning Season Names:")
        df['Season'] = df['Season'].astype(str).str.strip().str.title()
        
        season_replacements = {
            'Kharif': 'Kharif',      # Monsoon season (June-October)
            'Rabi': 'Rabi',          # Winter season (November-April)
            'Summer': 'Summer',       # Summer season (April-June)
            'Whole Year': 'Whole Year',
            'Nan': None
        }
        
        df['Season'] = df['Season'].replace(season_replacements)
        unique_seasons = df['Season'].dropna().unique()
        print(f"   📊 Seasons found: {list(unique_seasons)}")
    
    # ===== STEP 4: HANDLE MISSING VALUES =====
    print(f"\n" + "=" * 70)
    print("STEP 4: HANDLE MISSING VALUES")
    print("=" * 70)
    
    original_rows = len(df)
    
    # Handle missing values based on agricultural context
    for col in df.columns:
        missing_count = df[col].isnull().sum()
        if missing_count > 0:
            missing_pct = (missing_count / len(df)) * 100
            print(f"\n🔧 Processing '{col}' ({missing_pct:.1f}% missing):")
            
            if col in ['State_Name', 'District_Name']:
                # For location data, drop rows with missing values
                if missing_pct < 10:  # Only if less than 10% missing
                    df.dropna(subset=[col], inplace=True)
                    print(f"   ✅ Dropped {missing_count} rows with missing {col}")
                else:
                    df[col].fillna('Unknown', inplace=True)
                    print(f"   ✅ Filled with 'Unknown'")
                    
            elif col in ['Crop', 'Season']:
                # For agricultural categorical data, use mode or 'Unknown'
                mode_val = df[col].mode()
                if not mode_val.empty:
                    df[col].fillna(mode_val.iloc[0], inplace=True)
                    print(f"   ✅ Filled with mode: '{mode_val.iloc[0]}'")
                else:
                    df[col].fillna('Unknown', inplace=True)
                    print(f"   ✅ Filled with 'Unknown'")
                    
            elif col == 'Crop_Year':
                # For year data, use median year
                median_year = int(df[col].median()) if not df[col].isnull().all() else 2020
                df[col].fillna(median_year, inplace=True)
                print(f"   ✅ Filled with median year: {median_year}")
                
            elif col in ['Area', 'Production']:
                # For numerical agricultural data, use median (robust to outliers)
                if missing_pct < 20:  # If less than 20% missing, fill with median
                    median_val = df[col].median()
                    df[col].fillna(median_val, inplace=True)
                    print(f"   ✅ Filled with median: {median_val:.2f}")
                else:
                    # High missing percentage - consider dropping these rows
                    rows_before = len(df)
                    df.dropna(subset=[col], inplace=True)
                    rows_after = len(df)
                    print(f"   ⚠️  Dropped {rows_before - rows_after} rows due to high missing percentage")
    
    rows_after_missing = len(df)
    print(f"\n📊 Rows after handling missing values: {original_rows} → {rows_after_missing}")
    
    # ===== STEP 5: VALIDATE AND CLEAN NUMERICAL DATA =====
    print(f"\n" + "=" * 70)
    print("STEP 5: VALIDATE AND CLEAN NUMERICAL DATA")
    print("=" * 70)
    
    # Validate Area data
    if 'Area' in df.columns:
        print("🔧 Validating Area data:")
        
        # Check for negative values
        negative_area = (df['Area'] < 0).sum()
        if negative_area > 0:
            print(f"   ⚠️  Found {negative_area} negative area values")
            df['Area'] = df['Area'].abs()
            print(f"   ✅ Converted negative values to positive")
        
        # Check for zero values
        zero_area = (df['Area'] == 0).sum()
        if zero_area > 0:
            print(f"   📊 Found {zero_area} zero area values (may indicate data issues)")
        
        # Check for unrealistic values (> 100,000 hectares for a single record)
        unrealistic_area = (df['Area'] > 100000).sum()
        if unrealistic_area > 0:
            print(f"   ⚠️  Found {unrealistic_area} potentially unrealistic area values")
        
        print(f"   📈 Area statistics: Min={df['Area'].min():.2f}, Max={df['Area'].max():.2f}, Mean={df['Area'].mean():.2f}")
    
    # Validate Production data
    if 'Production' in df.columns:
        print(f"\n🔧 Validating Production data:")
        
        # Check for negative values
        negative_prod = (df['Production'] < 0).sum()
        if negative_prod > 0:
            print(f"   ⚠️  Found {negative_prod} negative production values")
            df['Production'] = df['Production'].abs()
            print(f"   ✅ Converted negative values to positive")
        
        # Zero production is valid (crop failure)
        zero_prod = (df['Production'] == 0).sum()
        print(f"   📊 Zero production records: {zero_prod} (may indicate crop failure)")
        
        print(f"   📈 Production statistics: Min={df['Production'].min():.2f}, Max={df['Production'].max():.2f}, Mean={df['Production'].mean():.2f}")
    
    # Calculate and validate productivity (if both Area and Production exist)
    if 'Area' in df.columns and 'Production' in df.columns:
        print(f"\n🔧 Calculating Productivity (Production/Area):")
        
        # Avoid division by zero
        df['Productivity'] = df['Production'] / (df['Area'] + 0.001)  # Add small value to avoid division by zero
        
        # Check for unrealistic productivity values
        high_productivity = (df['Productivity'] > 50).sum()  # > 50 tonnes/hectare is quite high
        if high_productivity > 0:
            print(f"   📊 High productivity records (>50 t/ha): {high_productivity}")
        
        print(f"   📈 Productivity stats: Mean={df['Productivity'].mean():.2f} t/ha, Median={df['Productivity'].median():.2f} t/ha")
    
    # ===== STEP 6: OUTLIER DETECTION =====
    print(f"\n" + "=" * 70)
    print("STEP 6: OUTLIER DETECTION")
    print("=" * 70)
    
    numerical_cols = ['Area', 'Production', 'Productivity']
    numerical_cols = [col for col in numerical_cols if col in df.columns]
    
    print(f"🔍 Analyzing outliers in: {numerical_cols}")
    
    outlier_summary = {}
    
    for col in numerical_cols:
        print(f"\n📊 Outlier analysis for {col}:")
        
        # IQR method
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
        outlier_count = outliers_mask.sum()
        
        if outlier_count > 0:
            outlier_pct = (outlier_count / len(df)) * 100
            outlier_summary[col] = outlier_count
            
            print(f"   📈 Outliers found: {outlier_count} ({outlier_pct:.1f}%)")
            print(f"   📏 Normal range: [{lower_bound:.2f}, {upper_bound:.2f}]")
            
            # Agricultural context: outliers might be valid (drought, exceptional yields, etc.)
            print(f"   ℹ️  Keeping outliers - may represent valid agricultural variations")
        else:
            print(f"   ✅ No outliers detected")
    
    # ===== STEP 7: REMOVE DUPLICATES =====
    print(f"\n" + "=" * 70)
    print("STEP 7: DUPLICATE REMOVAL")
    print("=" * 70)
    
    initial_rows = len(df)
    
    # Check for exact duplicates
    duplicate_count = df.duplicated().sum()
    print(f"🔍 Exact duplicates: {duplicate_count}")
    
    if duplicate_count > 0:
        df.drop_duplicates(inplace=True, ignore_index=True)
        print(f"✅ Removed {duplicate_count} exact duplicate rows")
    
    # Check for logical duplicates (same state, district, crop, year, season)
    key_columns = ['State_Name', 'District_Name', 'Crop', 'Crop_Year', 'Season']
    existing_key_cols = [col for col in key_columns if col in df.columns]
    
    if len(existing_key_cols) >= 3:
        logical_duplicates = df.duplicated(subset=existing_key_cols).sum()
        print(f"🔍 Logical duplicates: {logical_duplicates}")
        
        if logical_duplicates > 0:
            print(f"   ⚠️  Found {logical_duplicates} logical duplicates")
            print(f"   ℹ️  Review manually - may represent multiple crop varieties or data collection issues")
    
    final_rows = len(df)
    rows_removed = initial_rows - final_rows
    print(f"📊 Rows after duplicate removal: {initial_rows} → {final_rows}")
    
    # ===== STEP 8: FINAL DATA VALIDATION =====
    print(f"\n" + "=" * 70)
    print("STEP 8: FINAL DATA VALIDATION AND SUMMARY")
    print("=" * 70)
    
    # Year validation
    if 'Crop_Year' in df.columns:
        min_year, max_year = df['Crop_Year'].min(), df['Crop_Year'].max()
        print(f"📅 Year range: {min_year} to {max_year}")
        
        if min_year < 1990 or max_year > 2024:
            print(f"   ⚠️  Check year range - some values may be unrealistic")
    
    # Final missing values check
    final_missing = df.isnull().sum().sum()
    print(f"❌ Remaining missing values: {final_missing}")
    
    # Data quality summary
    print(f"\n📊 FINAL DATA QUALITY SUMMARY:")
    print(f"   - Original rows: {original_rows:,}")
    print(f"   - Final rows: {len(df):,}")
    print(f"   - Data retention: {(len(df)/original_rows)*100:.1f}%")
    print(f"   - Missing values: {final_missing}")
    
    if 'State_Name' in df.columns:
        print(f"   - States covered: {df['State_Name'].nunique()}")
    if 'Crop' in df.columns:
        print(f"   - Crops covered: {df['Crop'].nunique()}")
    if 'Crop_Year' in df.columns:
        print(f"   - Years covered: {df['Crop_Year'].nunique()}")
    
    # Store cleaned data
    globals()['cleaned_df'] = df
    print(f"\n✅ Cleaned dataset stored in variable 'cleaned_df'")
    
    # Display sample of cleaned data
    print(f"\n📋 SAMPLE OF CLEANED DATA:")
    print("=" * 70)
    print(df.head())
    
    print(f"\n" + "=" * 80)
    print("DATA CLEANING SECTION COMPLETE")
    print("=" * 80)

except Exception as e:
    print(f"❌ ERROR DURING DATA CLEANING: {str(e)}")
    import traceback
    traceback.print_exc()
    print(f"\n🔧 TROUBLESHOOTING:")
    print("1. Ensure data was loaded successfully in the previous section")
    print("2. Check that all required libraries are imported")
    print("3. Verify the dataset structure matches expected format")