# Power BI Template Setup Guide

## Overview
This template provides a comprehensive Power BI solution for visualizing Indian Agriculture data from your capstone project.

## Template Structure

### Data Model
- **Star Schema Design** optimized for performance
- **Dimension Tables**: States, Crops, Seasons, Dates
- **Fact Table**: Agriculture metrics (Area, Production, Yield)
- **Summary Tables**: Pre-aggregated data for faster visuals

## Manual Template Creation Steps

Since .pbit files are binary and cannot be created as text files, follow these steps to create your Power BI template:

### Step 1: Data Import
1. Open Power BI Desktop
2. Click "Get Data" → "Text/CSV"
3. Import the following files from the `powerbi/datasets/` folder:
   - `agriculture_data_powerbi.csv` (Main dataset)
   - `dim_states.csv`
   - `dim_crops.csv`
   - `dim_seasons.csv`
   - `dim_dates.csv`
   - `fact_agriculture.csv`
   - Summary tables (state_summary.csv, crop_summary.csv, yearly_trends.csv)

### Step 2: Create Relationships
Set up the following relationships in Model view:

```
fact_agriculture[State_ID] ← → dim_states[State_ID]
fact_agriculture[Crop_ID] ← → dim_crops[Crop_ID]
fact_agriculture[Season_ID] ← → dim_seasons[Season_ID]
fact_agriculture[Date_ID] ← → dim_dates[Date_ID]
```

### Step 3: Apply DAX Measures
Copy and paste the DAX measures from `dax_measures/agriculture_measures.dax`

### Step 4: Create Visualizations

#### Page 1: Executive Dashboard
- **KPI Cards**: Total Production, Total Area, Average Yield
- **Map Visual**: Production by State
- **Line Chart**: Yearly Trends
- **Donut Chart**: Production by Crop Category

#### Page 2: State Analysis
- **Table**: State-wise performance metrics
- **Bar Chart**: Top 10 states by production
- **Scatter Plot**: Area vs Production by State
- **Tree Map**: State contribution to total production

#### Page 3: Crop Analysis
- **Column Chart**: Production by Crop Type
- **Box Plot**: Yield distribution by Crop
- **Heat Map**: Crop performance by Season
- **Funnel Chart**: Crop area hierarchy

#### Page 4: Temporal Analysis
- **Line Chart**: Multi-year trends
- **Seasonal Charts**: Performance by Season
- **Calendar Heat Map**: Monthly patterns
- **Forecast Visual**: Trend predictions

#### Page 5: Performance Metrics
- **Gauge Charts**: Yield efficiency metrics
- **Waterfall Chart**: Year-over-year changes
- **Decomposition Tree**: Factor analysis
- **Key Influencers**: Driver analysis

### Step 5: Setup Filters and Slicers
Add slicers for:
- Year (2018-2023)
- State
- Crop Type
- Season

### Step 6: Format and Style
Apply consistent formatting:
- Color Scheme: Green (#228B22) for agriculture theme
- Font: Segoe UI
- Background: Light green gradient
- Consistent chart spacing and alignment

### Step 7: Save as Template
1. Click File → Export → Power BI Template (.pbit)
2. Save as `Indian_Agriculture_Dashboard_Template.pbit`
3. Place in the `powerbi/templates/` folder

## Data Refresh Setup

### Automatic Refresh (Power BI Service)
1. Publish to Power BI Service
2. Configure dataset refresh schedule
3. Set up data gateway if needed

### Manual Refresh
- Data → Refresh All (Ctrl + F5)

## Performance Optimization Tips

1. **Use Summary Tables**: Utilize pre-aggregated summary tables for heavy calculations
2. **Proper Data Types**: Ensure numeric columns are set to appropriate data types
3. **Relationships**: Use proper cardinality settings
4. **DAX Optimization**: Use variables and avoid row-by-row calculations
5. **Visual Optimization**: Limit data points in visuals when possible

## Troubleshooting

### Common Issues
1. **Data Import Errors**: Check file encoding (UTF-8-BOM)
2. **Relationship Issues**: Verify foreign key integrity
3. **Performance Issues**: Use DirectQuery for large datasets
4. **Date Issues**: Ensure proper date formatting

### Solutions
- Clear cache: File → Options → Data Load → Clear Cache
- Reset visuals: Remove and recreate problematic visuals
- Check data quality: Use Column Quality indicators

## Security Considerations
- Row-level security for multi-tenant scenarios
- Data classification for sensitive information
- Regular access reviews for published content

## Next Steps
1. Customize visuals based on specific requirements
2. Add additional KPIs as needed
3. Set up automated data refresh
4. Train end users on dashboard usage
5. Implement feedback collection mechanism