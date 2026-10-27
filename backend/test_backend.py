import sys
from pathlib import Path

# Add backend directory to path
BACKEND_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BACKEND_DIR))

from fastapi.testclient import TestClient
from app.main import app

def run_tests():
    print("=" * 60)
    print("RUNNING AUTOMATED FASTAPI BACKEND VERIFICATION SUITE")
    print("=" * 60)

    # Use TestClient with lifespan context
    with TestClient(app) as client:
        # Test 1: Root Health Check
        print("\n[1/7] Testing GET / ...")
        res = client.get("/")
        assert res.status_code == 200, f"Expected 200, got {res.status_code}"
        print(f"  Passed! Service: {res.json()['service']}, Dataset ready: {res.json()['dataset_ready']}")

        # Test 2: Metadata Prefectures
        print("\n[2/7] Testing GET /api/metadata/prefectures ...")
        res = client.get("/api/metadata/prefectures")
        assert res.status_code == 200, f"Expected 200, got {res.status_code}"
        data = res.json()
        print(f"  Passed! Found {data['count']} prefectures. Sample: {data['prefectures'][0]['prefecture']}")

        # Test 3: Metadata Date Range
        print("\n[3/7] Testing GET /api/metadata/date-range ...")
        res = client.get("/api/metadata/date-range")
        assert res.status_code == 200, f"Expected 200, got {res.status_code}"
        dr = res.json()
        print(f"  Passed! Date bounds: {dr['min_date']} to {dr['max_date']} ({dr['total_days']} total days)")

        # Test 4: Single-day Weather Query
        print("\n[4/7] Testing GET /api/weather/daily ...")
        res = client.get("/api/weather/daily?prefecture=Tokyo&date=2026-06-15")
        assert res.status_code == 200, f"Expected 200, got {res.status_code}"
        w = res.json()
        print(f"  Passed! Tokyo 2026-06-15 max temp: {w['metrics'].get('temperature_2m_max')}°C, rain: {w['metrics'].get('rain_sum')}mm")

        # Test 5: Time Series Query for D3 Charts
        print("\n[5/7] Testing GET /api/weather/timeseries ...")
        res = client.get("/api/weather/timeseries?prefecture=Tokyo&start_date=2026-06-01&end_date=2026-06-10")
        assert res.status_code == 200, f"Expected 200, got {res.status_code}"
        ts = res.json()
        print(f"  Passed! Retrieved {ts['total_data_points']} time-series data points.")

        # Test 6: Map Overview for D3 Japan Choropleth
        print("\n[6/7] Testing GET /api/weather/map-overview ...")
        res = client.get("/api/weather/map-overview?date=2026-06-15")
        assert res.status_code == 200, f"Expected 200, got {res.status_code}"
        mo = res.json()
        print(f"  Passed! Map data loaded for {mo['count']} prefectures.")

        # Test 7: Multi-hazard Disaster Prediction
        print("\n[7/7] Testing POST /api/predict ...")
        payload = {
            "prefecture": "Tokyo",
            "date": "2026-06-15",
            "hazards": ["flood", "rain", "temperature", "typhoon", "wind", "snow"]
        }
        res = client.post("/api/predict", json=payload)
        assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
        pred = res.json()
        print(f"  Passed! Mode: '{pred['execution_mode']}', Overall Risk: '{pred['overall_risk_level']}'")
        for r in pred["risks"]:
            val = f" ({r['predicted_value']}{r['unit']})" if r.get('predicted_value') else f" (prob: {r.get('probability')})"
            print(f"    - {r['hazard'].capitalize()}: {r['risk_level']}{val} | Model: {r['model_name']}")

    print("\n" + "=" * 60)
    print("ALL 7 API VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
