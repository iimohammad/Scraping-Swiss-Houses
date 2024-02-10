import time
import argparse
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import matplotlib.pyplot as plt


def load_and_plot_data(csv_file):
    # Load data from CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Print the loaded DataFrame
    print("Loaded Data:")
    print(df)

    # Plotting
    plt.figure(figsize=(12, 6))

    # Example plots (customize based on your data)
    plt.subplot(2, 1, 1)
    plt.bar(df['Apartment'], df['Number of Rooms'], color='skyblue')
    plt.title('Number of Rooms in Apartments')
    plt.xlabel('Apartment')
    plt.ylabel('Number of Rooms')

    plt.subplot(2, 1, 2)
    # Convert 'Living Space' to strings before creating the scatter plot
    plt.scatter(df['Living Space'].astype(str), df['Price'], color='orange')
    plt.title('Living Space vs Price')
    plt.xlabel('Living Space')
    plt.ylabel('Price')

    plt.tight_layout()
    plt.show()


def extract_apartment_details(city, min_rooms, max_rooms, min_price, max_price):
    base_url = "https://www.homegate.ch"
    search_url = f"{base_url}/rent/real-estate/city-{city}/matching-list?ac={min_rooms}&ad={max_rooms}&ag={min_price}&ah={max_price}"

    print(search_url)

    try:
        # Set up Selenium with headless option (invisible browser)
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)

        # Load the page using Selenium
        driver.get(search_url)
        time.sleep(2)  # Allow time for dynamic content to load (you may adjust this)

        # Extract HTML content after the page is fully loaded
        html_content = driver.page_source
        driver.quit()  # Close the browser

        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        soup = soup.body

        # Rest of your code remains unchanged
        details_divs = soup.find_all('div', class_='HgListingRoomsLivingSpace_roomsLivingSpace_GyVgq')
        price_tags = soup.find_all('span', class_='HgListingCard_price_JoPAs')

        # Create lists to store extracted data
        apartment_data = []

        for i, details_div in enumerate(details_divs):
            strong_tags = details_div.find_all('strong')
            rooms = strong_tags[0].text.strip() if strong_tags else "N/A"
            living_space = strong_tags[1].text.strip() if len(strong_tags) > 1 else "N/A"
            price = price_tags[i].text.strip() if i < len(price_tags) else "N/A"

            apartment_data.append({
                "Apartment": i + 1,
                "Number of Rooms": rooms,
                "Living Space": living_space,
                "Price": price
            })

            print(f"Apartment {i + 1} Details:")
            print(f"Number of Rooms: {rooms}")
            print(f"Living Space: {living_space}")
            print(f"Price: {price}")
            print("---")

        # Convert the data to a Pandas DataFrame
        df = pd.DataFrame(apartment_data)

        # Save the DataFrame to a CSV file
        df.to_csv(f"{city}_apartments.csv", index=False)
        print(f"\nData saved to {city}_apartments.csv")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract apartment details from Homegate.ch')
    parser.add_argument('--city', type=str, default='Zurich', help='City name')
    parser.add_argument('--min_rooms', type=int, default=1, help='Minimum number of rooms')
    parser.add_argument('--max_rooms', type=int, default=5, help='Maximum number of rooms')
    parser.add_argument('--min_price', type=int, default=600, help='Minimum price')
    parser.add_argument('--max_price', type=int, default=1300, help='Maximum price')

    args = parser.parse_args()

    print(f"Extracting apartment details in {args.city} with {args.min_rooms}-{args.max_rooms} rooms and price range {args.min_price}-{args.max_price}:")
    extract_apartment_details(args.city, args.min_rooms, args.max_rooms, args.min_price, args.max_price)
    print("\n")

    # Specify the CSV file path
    csv_file_path = 'Zurich_apartments.csv'  # Change this to your actual CSV file

    # Call the function to load and plot the data
    load_and_plot_data(csv_file_path)
