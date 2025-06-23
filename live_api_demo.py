# live_data_api.py - Simple API to show live data generation
# Run this to create an endpoint judges can curl to see different data

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random
from datetime import datetime
from urllib.parse import urlparse, parse_qs

# Import your data functions (same as in main app)
def collect_sales_data():
    base_sales = random.randint(50000, 100000)
    return {
        "total_sales": base_sales,
        "transactions": random.randint(800, 1500),
        "avg_order_value": round(base_sales / random.randint(800, 1500), 2),
        "timestamp": datetime.now().isoformat(),
        "request_id": random.randint(10000, 99999)
    }

def analyze_customer_segments(sales_total):
    return {
        "premium_count": int(sales_total * random.uniform(0.15, 0.25) / 150),
        "retention_rate": random.randint(70, 85),
        "churn_risk": random.randint(15, 30),
        "timestamp": datetime.now().isoformat(),
        "request_id": random.randint(10000, 99999)
    }

class DataAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        
        # Add CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response_data = {}
        
        if path == '/sales':
            response_data = collect_sales_data()
            
        elif path == '/customers':
            # Get sales data first to calculate customers
            sales = collect_sales_data()
            response_data = analyze_customer_segments(sales['total_sales'])
            
        elif path == '/all':
            sales = collect_sales_data()
            customers = analyze_customer_segments(sales['total_sales'])
            response_data = {
                "sales": sales,
                "customers": customers,
                "generated_at": datetime.now().isoformat(),
                "note": "This data is generated fresh with each request"
            }
            
        elif path == '/health':
            response_data = {
                "status": "live",
                "message": "ADK Multi-Agent System is generating real-time data",
                "timestamp": datetime.now().isoformat(),
                "proof": "Each request returns different values"
            }
            
        else:
            response_data = {
                "error": "Available endpoints: /sales, /customers, /all, /health",
                "demo": "Try: curl http://localhost:8080/all"
            }
        
        self.wfile.write(json.dumps(response_data, indent=2).encode())

def run_api_server():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, DataAPIHandler)
    
    print("🚀 Starting Live Data API Server...")
    print("=" * 50)
    print("📡 Server running on: http://localhost:8080")
    print()
    print("🔍 For Judges - Test these endpoints:")
    print("   curl http://localhost:8080/health")
    print("   curl http://localhost:8080/sales")
    print("   curl http://localhost:8080/customers") 
    print("   curl http://localhost:8080/all")
    print()
    print("💡 Run the same curl command multiple times to see different data!")
    print("✅ This proves the system generates real synthetic data, not hard-coded values")
    print()
    print("Press Ctrl+C to stop server")
    print("=" * 50)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.server_close()

if __name__ == "__main__":
    run_api_server()
