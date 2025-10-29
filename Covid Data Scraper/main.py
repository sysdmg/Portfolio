import requests
import json
from datetime import datetime

def get_covid_stats():
    # URL of Disease.sh API for Canadian COVID data
    url = "https://disease.sh/v3/covid-19/countries/canada"
    
    try:
        # Send HTTP request
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        
        # Initialize statistics dictionary with the latest data
        stats = {
            'Total Cases': f"{data['cases']:,}",
            'Deaths': f"{data['deaths']:,}",
            'Recovered': f"{data['recovered']:,}",
            'Active Cases': f"{data['active']:,}",
            'Critical Cases': f"{data['critical']:,}",
            'Tests Completed': f"{data['tests']:,}",
            'Cases per Million': f"{data['casesPerOneMillion']:,}",
            'Deaths per Million': f"{data['deathsPerOneMillion']:,}",
            'Last Updated': datetime.fromtimestamp(data['updated']/1000).strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Get current timestamp
        stats['Last Updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return stats
        
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def display_stats(stats):
    if not stats:
        print("No data available")
        return
    
    print("\n=== Canadian COVID-19 Statistics ===")
    print(f"Last Updated: {stats.get('Last Updated', 'N/A')}\n")
    
    # Display all available statistics
    for key, value in stats.items():
        if key != 'Last Updated':
            print(f"{key}: {value}")

def save_to_csv(stats):
    if not stats:
        return
    
    # Save to CSV
    filename = f"covid_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, 'w') as f:
        # Write header
        f.write(','.join(stats.keys()) + '\n')
        # Write values
        f.write(','.join(str(v) for v in stats.values()) + '\n')
    print(f"\nData saved to {filename}")

def main():
    while True:
        print("Fetching latest COVID-19 statistics from Canada...")
        stats = get_covid_stats()
        display_stats(stats)
        save_to_csv(stats)
        
        # Ask if user wants to continue
        choice = input("\nContinue to iterate? (y/n): ").lower().strip()
        if choice != 'y':
            break

if __name__ == "__main__":
    main()
