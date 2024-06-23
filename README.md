# Backed Assets

Backed Assets is a Python-based bot designed to search, filter, and analyze assets on the AtomicHub market. It identifies assets based on specified criteria and generates insightful data, helping users make informed decisions on asset purchases.

## Features

- Fetches and analyzes assets from the AtomicHub market.
- Filters assets based on backed token value and price.
- Displays detailed information about each asset.
- Identifies potential buying opportunities based on asset value.
- Outputs data in a structured tabular format.
- Saves fetched data to a JSON file for further analysis.

## Installation

1. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

2. Set up environment variables:
    Make a copy of `.env.example` file to `.env` file

## Output

- The bot prints two tables:
  - A general table of all fetched assets with details such as ID, Name, Collection, Price, Median, Average, and Backed value.
  - A filtered table showing assets that meet specific buying criteria.
- The data is also saved to `data.json` for further analysis.

## Example Output

| ID      | Name                | Collection    | Price | Median | Average | Backed |
|---------|---------------------|---------------|-------|--------|---------|--------|
| 1234567 | Chess Piece Knight  | chessunivers  | 10.5  | 11.0   | 10.8    | 12.0   |
| 1234568 | Upland Property     | uplandislive  | 5.0   | 5.5    | 5.3     | 6.0    |


=============BUY=============

| ID      | Name                | Collection    | Price | Median | Average | Backed | Buy |
|---------|---------------------|---------------|-------|--------|---------|--------|-----|
| 1234567 | Chess Piece Knight  | chessunivers  | 10.5  | 11.0   | 10.8    | 12.0   | ✅  |

## Link
  
  - https://eos.atomichub.io/market/sale/eos-mainnet/{sale_id_here}
  - https://eos.atomichub.io/explorer/asset/eos-mainnet/{asset_id_here}
