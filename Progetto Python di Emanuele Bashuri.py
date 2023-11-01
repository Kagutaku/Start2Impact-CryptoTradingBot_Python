# make a python program bot that can find from coinmarketcap api:
# 1 - The cryptocurrency with the highest volume (in $) over the past 24 hours
# 2 - The best and worst 10 cryptocurrencies (by percentage increase over the past 24 hours)
# 3 - The amount of money needed to buy one unit of each of the top 20 cryptocurrencies*
# 4 - The amount of money needed to buy one unit of all cryptocurrencies whose volume in the last 24 hours is greater than $76,000,000
# 5 - The percentage gain or loss you would have made if you had bought one unit of each of the top 20 cryptocurrencies* the day before (assuming the rankings have not changed)

# To prevent your program from overwriting the same JSON file, name it with the date of when the program runs.
# *The top 20 cryptocurrencies according to CoinMarketCap's default ranking, the one visible on the site, so sorted by capitalization.

import requests
from datetime import datetime
import json

# Define the API endpoint and API key
endpoint = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
api_key = '9feeebf4-a762-49c0-8d3a-51a34e10e035'

# Define the API parameters
params = {
    'start': '1',
    'limit': '100',
    'convert': 'USD'
}

# Define the API headers
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': api_key
}

# Make the API request and get the response
response = requests.get(endpoint, headers=headers, params=params)

# Parse the response data
data = response.json()['data']

# Get the current date to use in the filename
now = datetime.now()
date_string = now.strftime("%Y-%m-%d")

# 1 - Find the cryptocurrency with the largest 24-hour volume
best_volume = None
for currency in data:
    volume = currency['quote']['USD']['volume_24h']
    if best_volume is None or volume > best_volume['quote']['USD']['volume_24h']:
        best_volume = currency

# Format the 24-hour volume as a string with 2 decimal places
volume_str = format(best_volume['quote']['USD']['volume_24h'], '.2f')

# Print the name and 24-hour volume of the best cryptocurrency
print('The cryptocurrency with the largest 24-hour volume is', best_volume['name'], 'with a volume of', volume_str, '$')
print()

# 2 - Find the top and bottom 10 cryptocurrencies by 24-hour percent change
data.sort(key=lambda c: c['quote']['USD']['percent_change_24h'])
best_percent = data[-10:]
worst_percent = data[:10]

# Format the 24-hour percent change as a string with 2 decimal places
best_percent_str = [format(currency['quote']['USD']['percent_change_24h'], '.2f') for currency in best_percent]
worst_percent_str = [format(currency['quote']['USD']['percent_change_24h'], '.2f') for currency in worst_percent]

# Print the names and 24-hour percent changes of the best and worst cryptocurrencies
print('The top 10 cryptocurrencies by 24-hour percent change are:')
print(', '.join(['{} ({}%)'.format(currency['name'], best_percent_str[i]) for i, currency in enumerate(best_percent)]))
print()
print('The bottom 10 cryptocurrencies by 24-hour percent change are:')
print(', '.join(['{} ({}%)'.format(currency['name'], worst_percent_str[i]) for i, currency in enumerate(worst_percent)]))
print()

# 3 - Find the amount of money needed to buy one unit of each of the top 20 cryptocurrencies
# Sort the cryptocurrencies by market capitalization
top_20 = sorted(data, key=lambda c: c['quote']['USD']['market_cap'], reverse=True)[:20]

# Calculate the total amount of money needed to buy one unit of each currency
total_cost_volume = 0
for currency in top_20:
    price = currency['quote']['USD']['price']
    total_cost_volume += price

# Format the total cost as a string with 2 decimal places
total_cost_volume_str = format(total_cost_volume, '.2f')

# Print the total cost
print('The total amount of money needed to buy one unit of each of the top 20 cryptocurrencies is ', total_cost_volume_str, '$')
print()

# 4 - Find the amount of money needed to buy one unit of all cryptocurrencies whose volume in the last 24 hours is greater than $76,000,000
# Set the minimum volume threshold
min_volume = 76000000

# Calculate the total amount of money needed to buy one unit of each qualifying currency
total_cost = 0
for currency in data:
    volume = currency['quote']['USD']['volume_24h']
    if volume > min_volume:
        price = currency['quote']['USD']['price']
        # Round the price to 2 decimal places before adding it to the total cost
        total_cost += round(price, 2)

# Format the total cost as a string with 2 decimal places
total_cost_str = format(total_cost, '.2f')

# Print the total cost
print('The total amount of money needed to buy one unit of all cryptocurrencies whose volume in the last 24 hours is greater than $76,000,000 is', total_cost_str, '$')
print()

# 5 - Find the percentage gain or loss you would have made if you had bought one unit of each of the top 20 cryptocurrencies the day before
# Sort the cryptocurrencies by market capitalization
data.sort(key=lambda c: c['quote']['USD']['market_cap'], reverse=True)

# Initialize the total_change variable to 0
total_change = 0

# Iterate through the top 20 cryptocurrencies
for currency in data[:20]:
    # Get the unit price and 24-hour percent change for the currency
    current_price = currency['quote']['USD']['price']
    percent_change = currency['quote']['USD']['percent_change_24h']

    # Find the previous price
    previous_price = current_price / (1 + percent_change / 100)

    # Calculate the change in value of the currency
    change_in_value = current_price - previous_price

    # Add the change in value to the total_change variable
    total_change += change_in_value

# Calculate the total value of the portfolio
total_value = sum([currency['quote']['USD']['price'] for currency in data[:20]])

# Calculate the total percentage change in the portfolio
total_percent_change = total_change / total_value * 100

# Print the total percentage change in the portfolio
print('The total percentage change in the portfolio is', format(total_percent_change, '.2f'), '%')

# Define the data to include in the JSON report
report_data = {
    'best_volume': volume_str,
    'best_percent': best_percent_str,
    'worst_percent': worst_percent_str,
    'top_20': total_cost_volume_str,
    'high_volume': total_cost_str,
    'gain_loss': total_percent_change
}

# Encode the data as JSON
json_data = json.dumps(report_data, indent=2)

# Write the JSON data to a file`
with open(f'{date_string}.json', 'w') as f:
    f.write(json_data)