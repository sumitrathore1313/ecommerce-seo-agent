from company import get_xlsx_data_from_dir
from dotenv import load_dotenv
import pandas as pd
import asyncio
from agents.ecommerce import main as ecommerce_check
from agents.traffic import main as traffic_check

load_dotenv()

# Define Constants
DIR_LOC = "./data"

async def enrich_data():
    # Get data from Excel files
    data = get_xlsx_data_from_dir(DIR_LOC)[:10]
    
    # Convert to DataFrame with first row as header
    df = pd.DataFrame(data[1:], columns=data[0])
    
    # Add new columns for ecommerce check results
    df['is_ecommerce'] = None
    df['ecommerce_reason'] = None
    
    # Process each website
    for idx, row in df.iterrows():
        website_url = row['Website Url']
        
        # Check if the website is ecommerce
        try:
            result = await ecommerce_check(website_url)
            df.at[idx, 'is_ecommerce'] = result.is_ecommerce
            df.at[idx, 'ecommerce_reason'] = result.reason
        except Exception as e:
            print(f"Error processing {website_url}: {str(e)}")
            df.at[idx, 'is_ecommerce'] = None
            df.at[idx, 'ecommerce_reason'] = f"Error: {str(e)}"
        
        # Check if the website has lost the traffic n past 2 years
        try:
            result = await traffic_check(website_url)
            df.at[idx, 'has_lost_traffic'] = result.has_traffic_loss
            df.at[idx, 'traffic_last_2_year'] = result.traffic_last_2_year
            df.at[idx, 'traffic_last_year'] = result.traffic_last_year
            df.at[idx, 'traffic_now'] = result.traffic_now
        except Exception as e:
            print(f"Error processing {website_url}: {str(e)}")
            df.at[idx, 'has_lost_traffic'] = None
            df.at[idx, 'traffic_last_2_year'] = None
            df.at[idx, 'traffic_last_year'] = None
            df.at[idx, 'traffic_now'] = None
            
    
    # Save to CSV
    df.to_csv('output.csv', index=False)
    print("Data enrichment completed. Results saved to output.csv")

if __name__ == "__main__":
    asyncio.run(enrich_data())
