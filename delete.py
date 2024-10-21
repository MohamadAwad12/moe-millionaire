from flask import Flask, render_template_string, jsonify
import requests

app = Flask(__name__)

MOE_ADDRESS = "HKprCtGbnh1j8xeQggzWhhVd3kwDUdphqPqDP8vMay8b"
INITIAL_TOKENS = 169893235666.24582
MILLION_USD = 1000000

def fetch_token_price(address):
    base_url = "https://api.dexscreener.com/latest/dex/pairs/solana"
    url = f"{base_url}/{address}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if 'pairs' in data and len(data['pairs']) > 0:
            price = data['pairs'][0].get('priceUsd', '0')
            return float(price)
        else:
            return 0
    else:
        return 0

@app.route('/')
def home():
    initial_price = fetch_token_price(MOE_ADDRESS)
    initial_value = initial_price * INITIAL_TOKENS
    
    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Is Moe a Millionaire Yet?</title>
        <style>
            :root {
                --bg-color: #1a0505;
                --text-color: #e0e0e0;
                --accent-color: #ff4d4d;
                --progress-bg: #4a0f0f;
                --progress-fill: #ff4d4d;
            }
            @keyframes gradient {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            @keyframes celebrate {
                0%, 100% { transform: rotate(-5deg); }
                50% { transform: rotate(5deg); }
            }
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            html, body {
                height: 100vh;
                width: 100vw;
                overflow: hidden;
            }
            body {
                font-family: 'Arial', sans-serif;
                background-color: var(--bg-color);
                color: var(--text-color);
                display: flex;
                justify-content: center;
                align-items: center;
                transition: background-color 1s ease;
            }
            .container {
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                width: 100vw;
                height: 100vh;
                padding: 5vw;
            }
            h1 {
                font-size: 5vw;
                margin-bottom: 2vh;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            }
            #status {
                font-size: 8vw;
                font-weight: bold;
                margin: 2vh 0;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            }
            #totalValue {
                font-size: 6vw;
                margin: 2vh 0;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            }
            .progress-bar {
                background-color: var(--progress-bg);
                height: 4vh;
                width: 90vw;
                border-radius: 2vh;
                overflow: hidden;
                margin: 2vh 0;
                box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            #progressFill {
                height: 100%;
                width: 0%;
                background: var(--progress-fill);
                background-size: 200% 200%;
                animation: gradient 5s ease infinite;
                transition: width 0.5s ease-out;
            }
            #progressText {
                margin-top: 1vh;
                font-weight: bold;
                font-size: 3vw;
            }
            @media (orientation: portrait) {
                h1 { font-size: 8vw; }
                #status { font-size: 12vw; }
                #totalValue { font-size: 10vw; }
                #progressText { font-size: 5vw; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Is Moe a Millionaire Yet?</h1>
            <div id="status">Not Yet</div>
            <div id="totalValue">${{ '{:,.2f}'.format(initial_value) }}</div>
            <div class="progress-bar">
                <div id="progressFill"></div>
            </div>
            <div id="progressText">0% to $1,000,000</div>
        </div>
        <script>
            let currentValue = {{ initial_value }};
            let targetValue = {{ initial_value }};
            const millionUSD = {{ MILLION_USD }};
            let isMillionaire = false;

            function formatNumber(num) {
                return num.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
            }

            function updateDisplay() {
                const statusElement = document.getElementById('status');
                const totalValueElement = document.getElementById('totalValue');
                const progressFill = document.getElementById('progressFill');
                const progressText = document.getElementById('progressText');
                
                totalValueElement.textContent = '$' + formatNumber(currentValue);
                
                const progress = (currentValue / millionUSD) * 100;
                progressFill.style.width = Math.min(progress, 100) + '%';
                progressText.textContent = `${progress.toFixed(2)}% to $1,000,000`;

                if (currentValue >= millionUSD && !isMillionaire) {
                    isMillionaire = true;
                    statusElement.textContent = "YES!";
                    statusElement.style.color = "#4CAF50";
                    statusElement.style.animation = "celebrate 0.5s ease infinite";
                    document.body.style.backgroundColor = "#05150a";
                    document.documentElement.style.setProperty('--progress-bg', '#0f4a1f');
                    document.documentElement.style.setProperty('--progress-fill', '#4CAF50');
                    progressFill.style.background = "linear-gradient(270deg, #4CAF50, #45a049, #4CAF50)";
                    totalValueElement.style.animation = "pulse 2s infinite";
                } else if (currentValue < millionUSD && isMillionaire) {
                    isMillionaire = false;
                    statusElement.textContent = "Not Yet";
                    statusElement.style.color = "#e0e0e0";
                    statusElement.style.animation = "none";
                    document.body.style.backgroundColor = "#1a0505";
                    document.documentElement.style.setProperty('--progress-bg', '#4a0f0f');
                    document.documentElement.style.setProperty('--progress-fill', '#ff4d4d');
                    progressFill.style.background = "linear-gradient(270deg, #ff4d4d, #ff3333, #ff4d4d)";
                    totalValueElement.style.animation = "none";
                }
            }

            function interpolateValues() {
                const interpolationFactor = 0.1;
                currentValue += (targetValue - currentValue) * interpolationFactor;
                updateDisplay();
            }

            function fetchLatestData() {
                fetch('/get_status')
                    .then(response => response.json())
                    .then(data => {
                        targetValue = parseFloat(data.total_value);
                    })
                    .catch(error => console.error('Error:', error));
            }

            setInterval(interpolateValues, 50);
            setInterval(fetchLatestData, 1000);

            updateDisplay();
            fetchLatestData();
        </script>
    </body>
    </html>
    '''
    return render_template_string(html, initial_value=initial_value, MILLION_USD=MILLION_USD)

@app.route('/get_status')
def get_status():
    price = fetch_token_price(MOE_ADDRESS)
    total_value = price * INITIAL_TOKENS
    return jsonify({
        'total_value': total_value
    })

if __name__ == '__main__':
    app.run(debug=True)
