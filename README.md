# Polygon.IO Financial Data Analysis

A Python-based financial data analysis tool that fetches stock data from Polygon.IO API and calculates various technical indicators including Simple Moving Averages (SMA) and Average True Range (ATR).

## Features

- **Stock Data Fetching**: Retrieves daily OHLCV data from Polygon.IO API
- **Technical Indicators**: Calculates multiple SMA periods (10, 20, 50, 200 days)
- **ATR Calculation**: Computes Average True Range for various periods (1, 3, 5, 7, 14, 28 days)
- **Gap Analysis**: Calculates overnight gaps and percentage changes
- **Data Export**: Saves processed data to CSV format

## Prerequisites

- Python 3.7+
- Polygon.IO API key
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd Polygon.IO
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up your API key:
   - Create a `.env` file in the root directory
   - Add your Polygon.IO API key:
   ```
   POLYGON_API_KEY=your_api_key_here
   ```

## Usage

### Basic Usage

Run the main analysis script:
```bash
python single_agg_calc_SMA_ATR.py
```

### Configuration

You can modify the following parameters in the script:
- `ticker`: Stock symbol (default: "MU")
- `start_date`: Start date for data collection (default: "2019-01-01")
- `end_date`: End date for data collection (default: "2024-09-18")

## Output

The script generates a CSV file with the following columns:
- Ticker symbol
- Date
- OHLCV data (Open, High, Low, Close, Volume)
- Overnight gap and percentage
- 1-day percentage change
- SMA values for periods: 10, 20, 50, 200 days
- ATR values for periods: 1, 3, 5, 7, 14, 28 days

## Project Structure

```
Polygon.IO/
├── single_agg_calc_SMA_ATR.py    # Main analysis script
├── requirements.txt               # Python dependencies
├── README.md                     # This file
├── .gitignore                    # Git ignore rules
└── .env                          # API key (not tracked by git)
```

## API Key Setup

1. Sign up for a Polygon.IO account at https://polygon.io/
2. Get your API key from the dashboard
3. Create a `.env` file in the project root
4. Add your API key: `POLYGON_API_KEY=your_key_here`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is for educational and personal use. Please ensure you comply with Polygon.IO's terms of service.

## Disclaimer

This tool is for educational purposes only. Always verify data accuracy and consult with financial professionals before making investment decisions. 