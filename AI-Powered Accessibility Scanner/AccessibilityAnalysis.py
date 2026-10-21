import threading
import subprocess
from Utils.PageScanner import ScanPage
from Utils.ApiEndpointCreation import CreateApiEndpoint

# =============== Step 1 ==================== #
# Start the API endpoint in a separate thread
# =========================================== #
api_thread = threading.Thread(
    target=CreateApiEndpoint,
    daemon=True
)
api_thread.start()

# =============== Step 2 ==================== #
# Start the page scanning
# =========================================== #
ScanPage()

# =============== Step 3 ==================== #
# Start the Streamlit dashboard
# =========================================== #
subprocess.Popen(
    [
        "python",
        "-m",
        "streamlit",
        "run",
        "Utils/DashboardCreation.py",
        "--server.address=0.0.0.0"
    ]
)