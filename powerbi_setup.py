"""
Quick Setup Script for Power BI Integration
==========================================

This script helps you quickly set up the Power BI integration for your
Indian Agriculture Capstone Project.

Run this script to:
1. Validate the environment
2. Prepare sample data
3. Generate all necessary files for Power BI
4. Provide next steps guidance
"""

import os
import sys
import subprocess

def check_requirements():
    """Check if required packages are installed"""
    required_packages = ['pandas', 'numpy']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    if missing_packages:
        print(f"\n🔧 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install'] + missing_packages
            )
            print("✅ Packages installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please install manually:")
            print(f"pip install {' '.join(missing_packages)}")
            return False
    
    return True

def run_data_preparation():
    """Run the Power BI data preparation script"""
    print("\n📊 Running Power BI data preparation...")
    try:
        # Import and run the data preparation
        from powerbi_data_preparation import PowerBIDataPreprocessor
        
        preprocessor = PowerBIDataPreprocessor()
        preprocessor.process_all()
        
        print("\n✅ Data preparation completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error during data preparation: {e}")
        return False

def check_powerbi_desktop():
    """Check if Power BI Desktop is available"""
    print("\n🔍 Checking for Power BI Desktop...")
    
    # Common installation paths for Power BI Desktop
    common_paths = [
        r"C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe",
        r"C:\Users\{}\AppData\Local\Microsoft\WindowsApps\Microsoft.MicrosoftPowerBIDesktop_8wekyb3d8bbwe\PBIDesktop.exe".format(os.getenv('USERNAME', ''))
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            print("✅ Power BI Desktop found!")
            return True
    
    print("⚠️  Power BI Desktop not found in common locations.")
    print("   Please download from: https://powerbi.microsoft.com/desktop/")
    return False

def show_next_steps():
    """Display next steps for the user"""
    print("\n" + "="*70)
    print("🚀 POWER BI SETUP COMPLETE!")
    print("="*70)
    
    print("\n📋 Next Steps:")
    print("1. Open Power BI Desktop")
    print("2. Click 'Get Data' → 'Text/CSV'")
    print("3. Import files from 'powerbi/datasets/' folder:")
    print("   - agriculture_data_powerbi.csv")
    print("   - dim_states.csv")
    print("   - dim_crops.csv")
    print("   - dim_seasons.csv")
    print("   - dim_dates.csv")
    print("   - fact_agriculture.csv")
    print("   - state_summary.csv")
    print("   - crop_summary.csv")
    print("   - yearly_trends.csv")
    
    print("\n4. Set up relationships (Model view):")
    print("   - fact_agriculture[State_ID] ←→ dim_states[State_ID]")
    print("   - fact_agriculture[Crop_ID] ←→ dim_crops[Crop_ID]")
    print("   - fact_agriculture[Season_ID] ←→ dim_seasons[Season_ID]")
    print("   - fact_agriculture[Date_ID] ←→ dim_dates[Date_ID]")
    
    print("\n5. Import DAX measures:")
    print("   - Create a new table called 'Measures'")
    print("   - Copy measures from 'powerbi/dax_measures/agriculture_measures.dax'")
    
    print("\n6. Build your dashboard:")
    print("   - Follow the guide in 'powerbi/templates/PowerBI_Template_Guide.md'")
    
    print("\n📚 Documentation available in:")
    print("   - powerbi/documentation/PowerBI_Integration_Guide.md")
    
    print("\n🎯 Happy analyzing! 🌾")

def main():
    """Main setup function"""
    print("🌾 INDIAN AGRICULTURE CAPSTONE PROJECT")
    print("🔧 Power BI Integration Setup")
    print("="*50)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Setup failed. Please resolve package installation issues.")
        return
    
    # Check if we're in the right directory
    if not os.path.exists('powerbi'):
        print("❌ Please run this script from the main project directory")
        return
    
    # Change to powerbi directory
    os.chdir('powerbi')
    
    # Run data preparation
    if not run_data_preparation():
        print("\n❌ Setup failed during data preparation.")
        return
    
    # Check for Power BI Desktop
    check_powerbi_desktop()
    
    # Show next steps
    show_next_steps()

if __name__ == "__main__":
    main()