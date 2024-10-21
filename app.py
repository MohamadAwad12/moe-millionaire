from flask import Flask, render_template_string, jsonify
import requests
import time

app = Flask(__name__)

MOE_ADDRESS = "HKprCtGbnh1j8xeQggzWhhVd3kwDUdphqPqDP8vMay8b"
INITIAL_TOKENS = 169893235666.24582
MILLION_USD = 1000000

# Cache variables
last_price = 0
last_update_time = 0
cache_duration = 5  # Cache duration in seconds

def fetch_token_price():
    global last_price, last_update_time
    current_time = time.time()

    if current_time - last_update_time < cache_duration:
        return last_price

    base_url = "https://api.dexscreener.com/latest/dex/pairs/solana"
    url = f"{base_url}/{MOE_ADDRESS}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=3)
        if response.status_code == 200:
            data = response.json()
            if 'pairs' in data and len(data['pairs']) > 0:
                last_price = float(data['pairs'][0].get('priceUsd', '0'))
                last_update_time = current_time
    except Exception as e:
        print(f"Error fetching price: {str(e)}")
    
    return last_price

@app.route('/')
def home():
    initial_price = fetch_token_price()
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
            body {
                font-family: 'Arial', sans-serif;
                background-color: var(--bg-color);
                color: var(--text-color);
                transition: background-color 1s ease;
                overflow: hidden;
            }
            .container {
                height: 100vh;
                overflow-y: hidden;
            }
            .page {
                height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                padding: 5vw;
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                transition: transform 0.5s cubic-bezier(0.65, 0, 0.35, 1);
            }
            #page2 {
                transform: translateY(100%);
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
            .scroll-indicator {
                position: absolute;
                bottom: 7%;
                left: 50%;
                transform: translateX(-50%);
                font-size: 3rem;
                cursor: pointer;
                animation: pulse 2s infinite;
                transition: opacity 0.3s ease;
            }
            .scroll-indicator:hover {
                opacity: 0.7;
            }
            #page2 {
                background-color: rgba(26, 5, 5, 0.9);
            }
            #page2 h2 {
                font-size: 4vw;
                margin-bottom: 3vh;
            }
            #page2 p {
                font-size: 2.5vw;
                margin-bottom: 2vh;
            }
            @media (orientation: portrait) {
                h1 { font-size: 8vw; }
                #status { font-size: 12vw; }
                #totalValue { font-size: 10vw; }
                #progressText { font-size: 5vw; }
                #page2 h2 { font-size: 6vw; }
                #page2 p { font-size: 4vw; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="page" id="page1">
                <h1>Is Moe a Millionaire Yet?</h1>
                <div id="status">Not Yet</div>
                <div id="totalValue">${{ '{:,.2f}'.format(initial_value) }}</div>
                <div class="progress-bar">
                    <div id="progressFill"></div>
                </div>
                <div id="progressText">0% to $1,000,000</div>
                <div class="scroll-indicator" onclick="smoothScroll()">▼</div>
            </div>
            <div class="page" id="page2">
                <h2>About Moe's Journey</h2>
                <p>Follow Moe's exciting journey to becoming a millionaire! This page tracks Moe's progress in real-time, updating every few seconds to show the latest value of his holdings.</p>
                <h2>How It Works</h2>
                <p>We're tracking the value of Moe's tokens using live data from the cryptocurrency markets. As the token price fluctuates, you'll see Moe's total value change in real-time.</p>
                <div class="scroll-indicator" onclick="smoothScroll()">▲</div>
            </div>
        </div>
        <script>
            let currentValue = {{ initial_value }};
            let targetValue = {{ initial_value }};
            const millionUSD = {{ MILLION_USD }};
            let isMillionaire = false;
            let isSecondPageVisible = false;
            let isScrolling = false;

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

            function smoothScroll() {
                if (isScrolling) return;
                isScrolling = true;
                isSecondPageVisible = !isSecondPageVisible;
                const page1 = document.getElementById('page1');
                const page2 = document.getElementById('page2');
                if (isSecondPageVisible) {
                    page1.style.transform = 'translateY(-100%)';
                    page2.style.transform = 'translateY(0)';
                } else {
                    page1.style.transform = 'translateY(0)';
                    page2.style.transform = 'translateY(100%)';
                }
                setTimeout(() => { isScrolling = false; }, 500);
            }

            let touchStartY = 0;
            let touchEndY = 0;

            document.addEventListener('touchstart', e => {
                touchStartY = e.touches[0].clientY;
            }, false);

            document.addEventListener('touchmove', e => {
                touchEndY = e.touches[0].clientY;
            }, false);

            document.addEventListener('touchend', e => {
                if (touchStartY - touchEndY > 20 && !isSecondPageVisible) {
                    smoothScroll();
                } else if (touchEndY - touchStartY > 20 && isSecondPageVisible) {
                    smoothScroll();
                }
                touchStartY = 0;
                touchEndY = 0;
            }, false);

            window.addEventListener('wheel', (e) => {
                if (e.deltaY > 0 && !isSecondPageVisible) {
                    smoothScroll();
                } else if (e.deltaY < 0 && isSecondPageVisible) {
                    smoothScroll();
                }
            }, { passive: true });

            // Interpolate values every 50ms for smooth animation
            setInterval(interpolateValues, 50);

            // Fetch new data every 3 seconds
            setInterval(fetchLatestData, 3000);

            // Initial fetch
            fetchLatestData();
        </script>
    </body>
    </html>
    '''
    return render_template_string(html, initial_value=initial_value, MILLION_USD=MILLION_USD)

@app.route('/get_status')
def get_status():
    price = fetch_token_price()
    total_value = price * INITIAL_TOKENS
    return jsonify({
        'total_value': total_value
    })

if __name__ == '__main__':
    app.run(debug=True)
