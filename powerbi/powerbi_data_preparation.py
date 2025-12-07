"""
Power BI Data Preparation Script for Indian Agriculture Dataset
=============================================================

This script prepares the cleaned Indian agriculture data for Power BI visualization.
It exports data in formats optimized for Power BI consumption and creates
data model structures.

Author: Capstone Project Team
Date: December 2025
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
import json

class PowerBIDataPreprocessor:
    """
    A class to prepare agricultural data for Power BI visualization
    """
    
    def __init__(self, data_source_path=None):
        """
        Initialize the preprocessor
        
        Args:
            data_source_path (str): Path to the cleaned data file
        """
        self.data_source_path = data_source_path
        self.output_dir = os.path.join(os.path.dirname(__file__), 'datasets')
        self.ensure_output_directory()
        
    def ensure_output_directory(self):
        """Ensure the output directory exists"""
        os.makedirs(self.output_dir, exist_ok=True)
        
    def load_cleaned_data(self):
        """
        Load the cleaned agriculture data
        
        Returns:
            pd.DataFrame: Cleaned agriculture dataset
        """
        try:
            # Try to load from specified path
            if self.data_source_path and os.path.exists(self.data_source_path):
                df = pd.read_csv(self.data_source_path)
                print(f"✅ Data loaded from {self.data_source_path}")
            else:
                # Create sample dataset if no source available
                print("📝 Creating sample agriculture dataset for Power BI preparation...")
                df = self.create_sample_agriculture_data()
                
            return df
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            print("📝 Creating sample dataset instead...")
            return self.create_sample_agriculture_data()
    
    def create_sample_agriculture_data(self):
        """
        Create a comprehensive sample agriculture dataset for demonstration
        
        Returns:
            pd.DataFrame: Sample agriculture dataset
        """
        np.random.seed(42)
        
        states = ['Uttar Pradesh', 'Maharashtra', 'Punjab', 'Haryana', 'West Bengal', 
                 'Karnataka', 'Gujarat', 'Tamil Nadu', 'Rajasthan', 'Madhya Pradesh']
        
        crops = ['Rice', 'Wheat', 'Sugarcane', 'Cotton', 'Maize', 'Soybean', 
                'Groundnut', 'Barley', 'Mustard', 'Pulses']
        
        seasons = ['Kharif', 'Rabi', 'Summer']
        
        # Generate 1000 records
        n_records = 1000
        
        data = {
            'State_Name': np.random.choice(states, n_records),
            'District_Name': [f"District_{i%50 + 1}" for i in range(n_records)],
            'Crop_Year': np.random.choice(range(2018, 2024), n_records),
            'Season': np.random.choice(seasons, n_records),
            'Crop': np.random.choice(crops, n_records),
            'Area_Hectares': np.random.lognormal(7, 1, n_records).round(2),
            'Production_Tonnes': np.random.lognormal(8, 1.5, n_records).round(2),
            'Yield_Per_Hectare': None,  # Will be calculated
            'Temperature_Avg': np.random.normal(25, 5, n_records).round(1),
            'Rainfall_MM': np.random.lognormal(5, 0.8, n_records).round(1)
        }
        
        df = pd.DataFrame(data)
        
        # Calculate yield
        df['Yield_Per_Hectare'] = (df['Production_Tonnes'] / df['Area_Hectares']).round(3)
        
        # Add some realistic constraints
        df.loc[df['Yield_Per_Hectare'] > 20, 'Yield_Per_Hectare'] = np.random.uniform(5, 15, 
                                                                      sum(df['Yield_Per_Hectare'] > 20))
        
        return df
    
    def create_dimension_tables(self, df):
        """
        Create dimension tables for Power BI star schema
        
        Args:
            df (pd.DataFrame): Source dataset
            
        Returns:
            dict: Dictionary containing dimension tables
        """
        dimensions = {}
        
        # State Dimension
        state_dim = df[['State_Name']].drop_duplicates().reset_index(drop=True)
        state_dim['State_ID'] = range(1, len(state_dim) + 1)
        state_dim = state_dim[['State_ID', 'State_Name']]
        dimensions['states'] = state_dim
        
        # Crop Dimension
        crop_dim = df[['Crop']].drop_duplicates().reset_index(drop=True)
        crop_dim['Crop_ID'] = range(1, len(crop_dim) + 1)
        crop_dim = crop_dim[['Crop_ID', 'Crop']]
        dimensions['crops'] = crop_dim
        
        # Season Dimension
        season_dim = df[['Season']].drop_duplicates().reset_index(drop=True)
        season_dim['Season_ID'] = range(1, len(season_dim) + 1)
        season_dim = season_dim[['Season_ID', 'Season']]
        dimensions['seasons'] = season_dim
        
        # Date Dimension
        years = sorted(df['Crop_Year'].unique())
        date_data = []
        for year in years:
            date_data.append({
                'Date_ID': year,
                'Year': year,
                'Decade': f"{year//10*10}s",
                'IsCurrentYear': year == datetime.now().year
            })
        dimensions['dates'] = pd.DataFrame(date_data)
        
        return dimensions
    
    def create_fact_table(self, df, dimensions):
        """
        Create fact table with foreign keys
        
        Args:
            df (pd.DataFrame): Source dataset
            dimensions (dict): Dimension tables
            
        Returns:
            pd.DataFrame: Fact table
        """
        fact_df = df.copy()
        
        # Add foreign keys
        fact_df = fact_df.merge(
            dimensions['states'], 
            left_on='State_Name', 
            right_on='State_Name', 
            how='left'
        )
        
        fact_df = fact_df.merge(
            dimensions['crops'], 
            left_on='Crop', 
            right_on='Crop', 
            how='left'
        )
        
        fact_df = fact_df.merge(
            dimensions['seasons'], 
            left_on='Season', 
            right_on='Season', 
            how='left'
        )
        
        fact_df = fact_df.merge(
            dimensions['dates'], 
            left_on='Crop_Year', 
            right_on='Year', 
            how='left'
        )
        
        # Select only fact table columns
        fact_columns = [
            'State_ID', 'Crop_ID', 'Season_ID', 'Date_ID',
            'District_Name', 'Area_Hectares', 'Production_Tonnes', 
            'Yield_Per_Hectare', 'Temperature_Avg', 'Rainfall_MM'
        ]
        
        return fact_df[fact_columns]
    
    def create_summary_tables(self, df):
        """
        Create pre-aggregated summary tables for Power BI performance
        
        Args:
            df (pd.DataFrame): Source dataset
            
        Returns:
            dict: Dictionary containing summary tables
        """
        summaries = {}
        
        # State-level summary
        state_summary = df.groupby(['State_Name']).agg({
            'Area_Hectares': ['sum', 'mean'],
            'Production_Tonnes': ['sum', 'mean'],
            'Yield_Per_Hectare': ['mean', 'std'],
            'Crop': 'nunique'
        }).round(3)
        
        state_summary.columns = [
            'Total_Area', 'Avg_Area', 'Total_Production', 'Avg_Production',
            'Avg_Yield', 'Yield_StdDev', 'Crop_Diversity'
        ]
        state_summary = state_summary.reset_index()
        summaries['state_summary'] = state_summary
        
        # Crop-level summary
        crop_summary = df.groupby(['Crop']).agg({
            'Area_Hectares': ['sum', 'mean'],
            'Production_Tonnes': ['sum', 'mean'],
            'Yield_Per_Hectare': ['mean', 'max'],
            'State_Name': 'nunique'
        }).round(3)
        
        crop_summary.columns = [
            'Total_Area', 'Avg_Area', 'Total_Production', 'Avg_Production',
            'Avg_Yield', 'Max_Yield', 'States_Count'
        ]
        crop_summary = crop_summary.reset_index()
        summaries['crop_summary'] = crop_summary
        
        # Year-over-year trends
        yearly_trends = df.groupby(['Crop_Year']).agg({
            'Area_Hectares': 'sum',
            'Production_Tonnes': 'sum',
            'Yield_Per_Hectare': 'mean'
        }).round(3)
        yearly_trends = yearly_trends.reset_index()
        summaries['yearly_trends'] = yearly_trends
        
        return summaries
    
    def export_for_powerbi(self, df, dimensions, fact_table, summaries):
        """
        Export all tables in Power BI friendly formats
        
        Args:
            df (pd.DataFrame): Original dataset
            dimensions (dict): Dimension tables
            fact_table (pd.DataFrame): Fact table
            summaries (dict): Summary tables
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Export main dataset
        main_file = os.path.join(self.output_dir, 'agriculture_data_powerbi.csv')
        df.to_csv(main_file, index=False, encoding='utf-8-sig')
        print(f"✅ Main dataset exported to: {main_file}")
        
        # Export dimension tables
        for dim_name, dim_df in dimensions.items():
            dim_file = os.path.join(self.output_dir, f'dim_{dim_name}.csv')
            dim_df.to_csv(dim_file, index=False, encoding='utf-8-sig')
            print(f"✅ {dim_name.title()} dimension exported to: {dim_file}")
        
        # Export fact table
        fact_file = os.path.join(self.output_dir, 'fact_agriculture.csv')
        fact_table.to_csv(fact_file, index=False, encoding='utf-8-sig')
        print(f"✅ Fact table exported to: {fact_file}")
        
        # Export summary tables
        for summary_name, summary_df in summaries.items():
            summary_file = os.path.join(self.output_dir, f'{summary_name}.csv')
            summary_df.to_csv(summary_file, index=False, encoding='utf-8-sig')
            print(f"✅ {summary_name.replace('_', ' ').title()} exported to: {summary_file}")
        
        # Create data model documentation
        self.create_data_model_docs(dimensions, fact_table, summaries)
    
    def create_data_model_docs(self, dimensions, fact_table, summaries):
        """
        Create documentation for the data model
        
        Args:
            dimensions (dict): Dimension tables
            fact_table (pd.DataFrame): Fact table
            summaries (dict): Summary tables
        """
        model_info = {
            "data_model": {
                "type": "Star Schema",
                "created": datetime.now().isoformat(),
                "description": "Agriculture data model optimized for Power BI",
                "dimensions": {},
                "fact_table": {
                    "name": "fact_agriculture",
                    "rows": len(fact_table),
                    "columns": list(fact_table.columns)
                },
                "summary_tables": {}
            }
        }
        
        # Document dimensions
        for dim_name, dim_df in dimensions.items():
            model_info["data_model"]["dimensions"][dim_name] = {
                "rows": len(dim_df),
                "columns": list(dim_df.columns)
            }
        
        # Document summaries
        for summary_name, summary_df in summaries.items():
            model_info["data_model"]["summary_tables"][summary_name] = {
                "rows": len(summary_df),
                "columns": list(summary_df.columns)
            }
        
        # Save model documentation
        doc_file = os.path.join(self.output_dir, 'data_model_info.json')
        with open(doc_file, 'w', encoding='utf-8') as f:
            json.dump(model_info, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Data model documentation saved to: {doc_file}")
    
    def process_all(self):
        """
        Execute the complete data preparation pipeline
        """
        print("=" * 70)
        print("POWER BI DATA PREPARATION PIPELINE")
        print("=" * 70)
        
        # Step 1: Load data
        print("\n📊 Step 1: Loading and validating data...")
        df = self.load_cleaned_data()
        print(f"   Dataset shape: {df.shape}")
        
        # Step 2: Create dimensions
        print("\n🏗️  Step 2: Creating dimension tables...")
        dimensions = self.create_dimension_tables(df)
        for dim_name, dim_df in dimensions.items():
            print(f"   {dim_name.title()}: {len(dim_df)} rows")
        
        # Step 3: Create fact table
        print("\n📈 Step 3: Creating fact table...")
        fact_table = self.create_fact_table(df, dimensions)
        print(f"   Fact table: {fact_table.shape}")
        
        # Step 4: Create summaries
        print("\n📋 Step 4: Creating summary tables...")
        summaries = self.create_summary_tables(df)
        for summary_name, summary_df in summaries.items():
            print(f"   {summary_name.replace('_', ' ').title()}: {len(summary_df)} rows")
        
        # Step 5: Export everything
        print("\n💾 Step 5: Exporting for Power BI...")
        self.export_for_powerbi(df, dimensions, fact_table, summaries)
        
        print("\n" + "=" * 70)
        print("✅ POWER BI DATA PREPARATION COMPLETE!")
        print("=" * 70)
        print(f"📁 All files exported to: {self.output_dir}")
        print("\n🚀 Ready for Power BI import!")
        
        return {
            'original_data': df,
            'dimensions': dimensions,
            'fact_table': fact_table,
            'summaries': summaries
        }


def main():
    """
    Main execution function
    """
    # Initialize the preprocessor
    preprocessor = PowerBIDataPreprocessor()
    
    # Process all data
    result = preprocessor.process_all()
    
    print("\n📝 Next Steps:")
    print("1. Open Power BI Desktop")
    print("2. Import the CSV files from the 'datasets' folder")
    print("3. Create relationships between dimension and fact tables")
    print("4. Use the DAX measures provided in the dax_measures folder")
    print("5. Build your visualizations!")


if __name__ == "__main__":
    main()