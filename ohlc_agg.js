const axios = require("axios");
const fs = require("fs");
const { Parser } = require("json2csv");
require('dotenv').config({ path: './api.env' });

const getAggregates = async (ticker, from, to) => {
    try {
        const key = process.env.POLYGON_API_KEY;
        if (!key) {
            console.error("API Key not found in environment variables.");
            return null;
        }
        console.log("Using API Key:", key);  // Log API key (make sure it's correct and not empty)
        
        const url = `https://api.polygon.io/v2/aggs/ticker/${ticker}/range/1/day/${from}/${to}?adjusted=true&sort=asc&limit=50000&apiKey=${key}`;
        console.log("Fetching data from URL:", url);
        
        const response = await axios.get(url);
        console.log("API response status:", response.status);  // Log the status code of the response
        console.log("API response data:", response.data);  // Log the full response data

        const results = response.data.results;
        if (!results) {
            console.error("No results found in response.");
            return null;
        }
        console.log("Results received:", results.length, "items");  // Log the number of received results
        return results;
    } catch (err) {
        console.error("Error fetching data from API:", err);  // Log any errors
        return null;
    }
}

const saveToCSV = (data, filename) => {
    try {
        const json2csvParser = new Parser();
        const csv = json2csvParser.parse(data);
        fs.writeFileSync(filename, csv);
        console.log("Data saved to", filename);  // Confirm that the data is saved
    } catch (err) {
        console.error("Error saving to CSV:", err);  // Log any errors during saving
    }
}

const main = async () => {
    const ticker = "AAPL";
    const from = "2010-01-01";
    const to = "2022-02-02";
    console.log("Fetching data for ticker:", ticker, "from:", from, "to:", to);  // Log the parameters
    
    const data = await getAggregates(ticker, from, to);
    if (data && data.length > 0) {
        saveToCSV(data, "aggregates.csv");
    } else {
        console.log("No data received or data is empty.");  // Log if no data is received or data is empty
    }
}

main();

module.exports = { getAggregates };
