require('dotenv').config({ path: './api.env' });

const testEnv = () => {
    const key = process.env.POLYGON_API_KEY;
    if (!key) {
        console.error("API Key not found in environment variables.");
    } else {
        console.log("Using API Key:", key);
    }
}

testEnv();
