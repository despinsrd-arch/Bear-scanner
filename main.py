from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

# Import your screener function
from screener import run_screen   # <-- make sure this matches your actual file/function name

app = FastAPI()

# ---------------------------
# HOMEPAGE (Website UI)
# ---------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Bear Scanner</title>
            <style>
                body { font-family: Arial; padding: 40px; background: #f5f5f5; }
                h1 { color: #333; }
                button {
                    padding: 12px 20px;
                    font-size: 18px;
                    background: #0078ff;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    cursor: pointer;
                }
                button:hover { background: #005fcc; }
                pre {
                    background: white;
                    padding: 20px;
                    border-radius: 6px;
                    margin-top: 20px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }
            </style>
        </head>
        <body>
            <h1>Bear Scanner</h1>
            <p>Click the button below to run the advanced stock screener.</p>
            <button onclick="runScan()">Run Scan</button>
            <pre id="results">Results will appear here...</pre>

            <script>
                async function runScan() {
                    document.getElementById('results').innerText = "Running scan...";
                    const res = await fetch('/screen');
                    const data = await res.json();
                    document.getElementById('results').innerText = JSON.stringify(data, null, 2);
                }
            </script>
        </body>
    </html>
    """

# ---------------------------
# SCREENER ENDPOINT
# ---------------------------
@app.get("/screen")
def screen():
    results = run_screen()
    return JSONResponse(content=results)


