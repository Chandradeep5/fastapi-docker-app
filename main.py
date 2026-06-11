from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os
from datetime import datetime
import platform
import pkg_resources

app = FastAPI()

APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

# ---------------- API ENDPOINTS ---------------- #

from datetime import datetime
import pytz

@app.get("/health")
def health():
    ist = pytz.timezone("Asia/Kolkata")
    current_time = datetime.now(ist)

    return {
        "status": "OK",
        "time": current_time.strftime("%Y-%m-%d %H:%M:%S %Z")
    }

@app.get("/version")
def version():
    return {"version": APP_VERSION}

@app.get("/hello")
def hello():
    return {"message": "Hello from FastAPI!"}

@app.get("/info")
def info():
    important = ["fastapi", "uvicorn", "gunicorn"]
    packages = [pkg.key for pkg in pkg_resources.working_set if pkg.key in important]

    return {
        "version": APP_VERSION,
        "libraries": packages
    }

import sys
import os
import platform

@app.get("/system")
def system_info():

    # Get Python version
    python_version = sys.version

    # Try to get detailed OS info
    os_info = "Unknown"

    try:
        with open("/etc/os-release") as f:
            os_info = f.read()
    except:
        os_info = platform.platform()

    return {
        "python_version": python_version,
        "os_details": os_info.split("\\n")[0],  # cleaner display
        "machine": platform.machine(),
        "processor": platform.processor()
    }

import os
import time

@app.get("/metrics")
def metrics():
    try:
        # Uptime
        uptime = time.time() - os.stat('/proc/1').st_ctime

        # Memory info
        with open('/proc/meminfo') as f:
            meminfo = f.readlines()

        mem_total = int(meminfo[0].split()[1])  # kB
        mem_free = int(meminfo[1].split()[1])

        # CPU load
        load1, load5, load15 = os.getloadavg()

        # ✅ CPU cores
        cpu_cores = os.cpu_count()

        # ✅ Load percentage (relative to cores)
        load_percent = round((load1 / cpu_cores) * 100, 2)

        return {
            "uptime_seconds": round(uptime, 2),
            "cpu_cores": cpu_cores,
            "cpu_load_1min": load1,
            "cpu_load_percent": load_percent,
            "memory_total_kb": mem_total,
            "memory_free_kb": mem_free
        }

    except Exception as e:
        return {"error": str(e)}

# ---------------- FRONTEND UI ---------------- #

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>FastAPI Dashboard</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f6f8;
                text-align: center;
                margin-top: 40px;
            }

            .container {
                background: white;
                padding: 30px;
                border-radius: 12px;
                width: 450px;
                margin: auto;
                box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
            }

            h1 {
                color: #333;
            }

            button {
                padding: 10px 15px;
                margin: 8px;
                border: none;
                border-radius: 8px;
                background-color: #007BFF;
                color: white;
                font-size: 14px;
                cursor: pointer;
                transition: 0.3s;
            }

            button:hover {
                background-color: #0056b3;
            }

            #output {
                margin-top: 20px;
                font-size: 16px;
            }

            table {
                margin: auto;
                border-collapse: collapse;
                margin-top: 15px;
            }

            th, td {
                padding: 8px 12px;
                border: 1px solid #ccc;
            }

            .green { color: green; font-weight: bold; }
            .red { color: red; font-weight: bold; }
        </style>
    </head>

    <body>

        <div class="container">
            <h1>🚀 FastAPI Dashboard</h1>

            <button onclick="checkHealth()">✅ Health</button>
            <button onclick="getVersion()">📦 Version</button>
            <button onclick="sayHello()">👋 Hello</button>
            <button onclick="getInfo()">📊 App Info</button>
            <button onclick="getSystem()">💻 System</button>
            <button onclick="openDocs()">📘 API Docs</button>
            <button id="themeBtn" onclick="toggleTheme()">🌙</button>
            <button onclick="getMetrics()">📈 Metrics</button>


            <div id="output">Click a button to see results</div>
        </div>

        <script>

            function showLoading() {
                document.getElementById('output').innerText = "Loading...";
            }

            async function fetchData(url) {
                try {
                    showLoading();
                    let res = await fetch(url);

                    if (!res.ok) throw new Error("Request failed");

                    return await res.json();

                } catch (error) {
                    document.getElementById('output').innerText = "Error: " + error.message;
                }
            }

            async function checkHealth() {
                let data = await fetchData('/health');
                if (!data) return;

                let color = data.status === "OK" ? "green" : "red";

                document.getElementById('output').innerHTML =
                    `<span class="${color}">● ${data.status}</span><br>Time: ${data.time}`;
            }

            async function getVersion() {
                let data = await fetchData('/version');
                if (!data) return;

                document.getElementById('output').innerText = "Version: " + data.version;
            }

            async function sayHello() {
                let data = await fetchData('/hello');
                if (!data) return;

                document.getElementById('output').innerText = data.message;
            }

            async function getInfo() {
                let data = await fetchData('/info');
                if (!data) return;

                document.getElementById('output').innerHTML = `
                    <table>
                        <tr><th>Version</th><td>${data.version}</td></tr>
                        <tr><th>Libraries</th><td>${data.libraries.join(", ")}</td></tr>
                    </table>
                `;
            }

            async function getSystem() {
                let data = await fetchData('/system');
                if (!data) return;

                document.getElementById('output').innerHTML = `
                    
                    <table>
                        <tr><th>OS</th><td>${data.os_details}</td></tr>
                        <tr><th>Python</th><td>${data.python_version}</td></tr>
                        <tr><th>Arch</th><td>${data.machine}</td></tr>
                    </table>

                `;
            }

            function openDocs() {
                window.open('/docs');
            }
            function toggleTheme() {
                let body = document.body;
                let container = document.querySelector('.container');
                let button = document.getElementById("themeBtn");

                if (body.classList.contains("dark")) {
                    // ✅ Switch to light
                    body.classList.remove("dark");

                    body.style.background = "#f4f6f8";
                    body.style.color = "black";

                    container.style.background = "white";
                    container.style.color = "black";

                    button.innerText = "🌙";  // show moon

                } else {
                    // ✅ Switch to dark
                    body.classList.add("dark");

                    body.style.background = "black";
                    body.style.color = "white";

                    container.style.background = "#1e1e1e";
                    container.style.color = "white";

                    button.innerText = "☀️";  // show sun
                }
            }

            async function getMetrics() {
                let data = await fetchData('/metrics');
                if (!data) return;

                // ✅ Dynamic color logic
                let color = "green";
                if (data.cpu_load_percent > 70) {
                    color = "red";
                } else if (data.cpu_load_percent > 40) {
                    color = "orange";
                }

                document.getElementById('output').innerHTML = `
                    <table>
                        <tr><th>Uptime (sec)</th><td>${data.uptime_seconds}</td></tr>
                        <tr><th>CPU Cores</th><td>${data.cpu_cores}</td></tr>
                        <tr><th>CPU Load (1m)</th><td>${data.cpu_load_1min}</td></tr>

                        <tr>
                        <th>CPU Usage</th>
                        <td>
                            <div style="background:#ddd; width:100%; border-radius:5px;">
                            <div style="
                                    width:${data.cpu_load_percent}%;
                                    background:${color};
                                    color:white;
                                    padding:3px;
                                    text-align:center;
                                    border-radius:5px;">
                                ${data.cpu_load_percent}%
                            </div>
                            </div>
                        </td>
                        </tr>

                        <tr><th>Total Memory</th><td>${data.memory_total_kb} KB</td></tr>
                        <tr><th>Free Memory</th><td>${data.memory_free_kb} KB</td></tr>
                    </table>
                `;
            }


        </script>
    </body>
    </html>
    """
