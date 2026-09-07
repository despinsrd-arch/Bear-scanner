from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

# Import your async screener function
from screener import run_screen

app = FastAPI()

# ---------------------------
# HOMEPAGE (Vibrant Neon Dashboard with Live Chart Links)
# ---------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bear Scanner - Live Momentum Screener</title>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
        <style>
            :root {
                --bg-primary: #070913;
                --bg-card: rgba(20, 24, 45, 0.75);
                --gradient-brand: linear-gradient(135deg, #00f2fe 0%, #4facfe 50%, #00c6ff 100%);
                --gradient-btn: linear-gradient(135deg, #7928CA 0%, #FF0080 100%);
                --gradient-badge: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                --accent-cyan: #00f2fe;
                --accent-pink: #ff007a;
                --accent-purple: #7928ca;
                --accent-green: #00e676;
                --accent-amber: #ffab00;
                --text-main: #ffffff;
                --text-muted: #a0aec0;
                --border-color: rgba(255, 255, 255, 0.12);
            }

            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            }

            body {
                background: radial-gradient(circle at 10% 20%, rgba(121, 40, 202, 0.15) 0%, transparent 40%),
                            radial-gradient(circle at 90% 80%, rgba(0, 242, 254, 0.15) 0%, transparent 40%),
                            var(--bg-primary);
                background-attachment: fixed;
                color: var(--text-main);
                padding: 2rem;
                min-height: 100vh;
            }

            .container {
                max-width: 1280px;
                margin: 0 auto;
            }

            header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding-bottom: 2rem;
                border-bottom: 1px solid var(--border-color);
                margin-bottom: 2rem;
            }

            .brand {
                display: flex;
                align-items: center;
                gap: 14px;
            }

            .brand-logo {
                background: var(--gradient-brand);
                width: 48px;
                height: 48px;
                border-radius: 14px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 800;
                font-size: 24px;
                color: #000;
                box-shadow: 0 0 20px rgba(0, 242, 254, 0.4);
            }

            h1 {
                font-size: 2rem;
                font-weight: 800;
                letter-spacing: -0.5px;
                background: var(--gradient-brand);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .subtitle {
                color: var(--text-muted);
                font-size: 0.95rem;
                margin-top: 2px;
            }

            .scan-btn {
                background: var(--gradient-btn);
                color: #fff;
                border: none;
                padding: 14px 32px;
                font-size: 1.05rem;
                font-weight: 800;
                border-radius: 12px;
                cursor: pointer;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: 0 4px 20px rgba(255, 0, 128, 0.4);
                display: flex;
                align-items: center;
                gap: 10px;
                letter-spacing: 0.5px;
            }

            .scan-btn:hover {
                transform: translateY(-3px) scale(1.02);
                box-shadow: 0 8px 30px rgba(255, 0, 128, 0.6);
            }

            .scan-btn:disabled {
                background: #2a2e45;
                cursor: not-allowed;
                box-shadow: none;
                transform: none;
            }

            .status-bar {
                display: flex;
                align-items: center;
                justify-content: space-between;
                background: var(--bg-card);
                backdrop-filter: blur(12px);
                padding: 1.1rem 1.75rem;
                border-radius: 16px;
                border: 1px solid var(--border-color);
                margin-bottom: 2rem;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            }

            .status-indicator {
                display: flex;
                align-items: center;
                gap: 10px;
                font-size: 1rem;
                color: var(--text-main);
            }

            .dot {
                width: 12px;
                height: 12px;
                border-radius: 50%;
                background-color: var(--accent-green);
                box-shadow: 0 0 14px var(--accent-green);
                animation: pulse 2s infinite;
            }

            @keyframes pulse {
                0% { box-shadow: 0 0 0 0 rgba(0, 230, 118, 0.7); }
                70% { box-shadow: 0 0 0 10px rgba(0, 230, 118, 0); }
                100% { box-shadow: 0 0 0 0 rgba(0, 230, 118, 0); }
            }

            .grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
                gap: 1.5rem;
            }

            /* Clickable Card Link Styling */
            .card-link {
                text-decoration: none;
                color: inherit;
                display: block;
            }

            .card {
                background: var(--bg-card);
                backdrop-filter: blur(16px);
                border: 1px solid var(--border-color);
                border-radius: 18px;
                padding: 1.4rem;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                overflow: hidden;
                cursor: pointer;
            }

            .card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: var(--gradient-brand);
                opacity: 0;
                transition: opacity 0.3s ease;
            }

            .card:hover {
                transform: translateY(-6px);
                border-color: rgba(0, 242, 254, 0.5);
                box-shadow: 0 12px 30px rgba(0, 242, 254, 0.25);
            }

            .card:hover::before {
                opacity: 1;
            }

            .card-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1.2rem;
            }

            .symbol-container {
                display: flex;
                align-items: center;
                gap: 6px;
            }

            .symbol {
                font-size: 1.5rem;
                font-weight: 800;
                letter-spacing: 0.5px;
                color: #fff;
                text-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
            }

            .external-icon {
                font-size: 0.85rem;
                color: var(--accent-cyan);
                opacity: 0.7;
                transition: opacity 0.2s ease;
            }

            .card:hover .external-icon {
                opacity: 1;
            }

            .score-badge {
                background: var(--gradient-badge);
                color: #000;
                padding: 5px 12px;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: 800;
                box-shadow: 0 0 12px rgba(56, 239, 125, 0.4);
            }

            .metric-row {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 0.7rem;
                padding: 6px 10px;
                background: rgba(255, 255, 255, 0.03);
                border-radius: 8px;
                font-size: 0.92rem;
            }

            .metric-label {
                color: var(--text-muted);
                font-weight: 600;
            }

            .price-val {
                color: var(--accent-cyan);
                font-weight: 700;
                font-size: 1.05rem;
            }

            .vol-val {
                color: #ffffff;
                font-weight: 700;
            }

            .rvol-val {
                color: var(--accent-pink);
                font-weight: 800;
                background: rgba(255, 0, 122, 0.1);
                padding: 2px 8px;
                border-radius: 6px;
                border: 1px solid rgba(255, 0, 122, 0.3);
            }

            .chart-hint {
                margin-top: 10px;
                text-align: center;
                font-size: 0.78rem;
                font-weight: 700;
                color: var(--accent-cyan);
                letter-spacing: 0.5px;
                opacity: 0.8;
            }

            .empty-state {
                text-align: center;
                padding: 4rem 2rem;
                color: var(--text-muted);
                grid-column: 1 / -1;
                background: var(--bg-card);
                border-radius: 18px;
                border: 1px dashed var(--border-color);
            }

            .spinner {
                width: 22px;
                height: 22px;
                border: 3px solid rgba(255,255,255,0.3);
                border-radius: 50%;
                border-top-color: #fff;
                animation: spin 0.8s linear infinite;
                display: none;
            }

            @keyframes spin {
                to { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <div class="brand">
                    <div class="brand-logo">B</div>
                    <div>
                        <h1>Bear Scanner</h1>
                        <div class="subtitle">Live High-Momentum Low-Price Stock Screener</div>
                    </div>
                </div>
                <button id="scanBtn" class="scan-btn" onclick="runScan()">
                    <div id="spinner" class="spinner"></div>
                    <span id="btnText">⚡ RUN LIVE SCAN</span>
                </button>
            </header>

            <div class="status-bar">
                <div class="status-indicator">
                    <div class="dot"></div>
                    <span>Universe: <strong style="color: var(--accent-cyan);">2,765 Tickers</strong> ($0.001 - $35.00)</span>
                </div>
                <div id="statusText" style="color: var(--accent-amber); font-weight: 600; font-size: 0.95rem;">
                    Ready for scan
                </div>
            </div>

            <div id="resultsGrid" class="grid">
                <div class="empty-state">
                    <h3 style="color: #fff; margin-bottom: 8px;">No scan results loaded yet</h3>
                    <p>Click <strong style="color: var(--accent-pink);">"⚡ RUN LIVE SCAN"</strong> above to pull real-time market momentum.</p>
                </div>
            </div>
        </div>

        <script>
            async function runScan() {
                const btn = document.getElementById('scanBtn');
                const btnText = document.getElementById('btnText');
                const spinner = document.getElementById('spinner');
                const statusText = document.getElementById('statusText');
                const grid = document.getElementById('resultsGrid');

                btn.disabled = true;
                spinner.style.display = 'block';
                btnText.innerText = 'Scanning...';
                statusText.innerText = 'Connecting to Yahoo Finance live feeds...';
                statusText.style.color = 'var(--accent-cyan)';

                try {
                    const res = await fetch('/screen');
                    const data = await res.json();

                    grid.innerHTML = '';

                    if (!data || data.length === 0) {
                        grid.innerHTML = `
                            <div class="empty-state">
                                <h3 style="color: #fff;">No stocks matched criteria</h3>
                                <p>Try running the scan during active market hours.</p>
                            </div>`;
                        statusText.innerText = 'Scan complete: 0 stocks matched.';
                    } else {
                        data.forEach(stock => {
                            const priceFormatted = stock.price ? '$' + stock.price.toFixed(2) : 'N/A';
                            const volFormatted = stock.volume ? stock.volume.toLocaleString() : 'N/A';
                            const rvolFormatted = stock.rvol ? stock.rvol + 'x' : 'N/A';

                            // External TradingView chart link for each ticker
                            const chartUrl = `https://www.tradingview.com/symbols/${stock.symbol}/`;

                            const cardHtml = `
                                <a href="${chartUrl}" target="_blank" rel="noopener noreferrer" class="card-link">
                                    <div class="card">
                                        <div class="card-header">
                                            <div class="symbol-container">
                                                <div class="symbol">${stock.symbol}</div>
                                                <span class="external-icon">↗</span>
                                            </div>
                                            <div class="score-badge">Score: ${stock.score}</div>
                                        </div>
                                        <div class="metric-row">
                                            <span class="metric-label">Current Price</span>
                                            <span class="price-val">${priceFormatted}</span>
                                        </div>
                                        <div class="metric-row">
                                            <span class="metric-label">Volume</span>
                                            <span class="vol-val">${volFormatted}</span>
                                        </div>
                                        <div class="metric-row">
                                            <span class="metric-label">Relative Vol (RVOL)</span>
                                            <span class="rvol-val">${rvolFormatted}</span>
                                        </div>
                                        <div class="chart-hint">📈 CLICK TO OPEN TRADINGVIEW CHART</div>
                                    </div>
                                </a>`;
                            grid.innerHTML += cardHtml;
                        });
                        statusText.innerText = `Scan success: Rendered top ${data.length} momentum stocks!`;
                        statusText.style.color = 'var(--accent-green)';
                    }
                } catch (err) {
                    statusText.innerText = 'Scan error: ' + err;
                    statusText.style.color = 'var(--accent-pink)';
                    grid.innerHTML = `
                        <div class="empty-state" style="border-color: var(--accent-pink);">
                            <h3 style="color: var(--accent-pink);">Error executing scan</h3>
                            <p>${err}</p>
                        </div>`;
                } finally {
                    btn.disabled = false;
                    spinner.style.display = 'none';
                    btnText.innerText = '⚡ RUN LIVE SCAN';
                }
            }
        </script>
    </body>
    </html>
    """

# ---------------------------
# SCREENER ENDPOINT
# ---------------------------
@app.get("/screen")
async def screen():
    results = await run_screen()
    return JSONResponse(content=results)
