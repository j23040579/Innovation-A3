import sys
from pathlib import Path

# Add backend directory to path
BACKEND_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BACKEND_DIR))

from fastapi.testclient import TestClient
from app.main import app
from app.services.weather_query_service import WeatherQueryService
import pandas as pd

def test_map_overview_preserves_snow_data_availability():
    service = WeatherQueryService()
    service.df = pd.DataFrame([
        {"prefecture": "Niigata", "date": "2026-06-15", "snowfall_sum": 12.5},
        {"prefecture": "Tokyo", "date": "2026-06-15", "snowfall_sum": None},
    ])
    items = {item["prefecture"]: item for item in service.get_map_overview("2026-06-15")}
    assert items["Niigata"]["snowfall_sum"] == 12.5
    assert items["Tokyo"]["snowfall_sum"] is None

def run_tests():
    print("=" * 60)
    print("RUNNING AUTOMATED FASTAPI BACKEND VERIFICATION SUITE")
    print("=" * 60)
    test_map_overview_preserves_snow_data_availability()
    print("\n[0/7] Passed focused map snowfall availability check.")

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
        snow_coverage = client.get("/api/predict/snow-coverage")
        assert snow_coverage.status_code == 200, f"Snow model coverage failed: {snow_coverage.text}"
        assert {"Niigata", "Yamagata"} <= set(snow_coverage.json()), (
            f"Expected coverage to reflect both installed regional models: {snow_coverage.json()}"
        )

        # Test 3: Metadata Date Range
        print("\n[3/7] Testing GET /api/metadata/date-range ...")
        res = client.get("/api/metadata/date-range")
        assert res.status_code == 200, f"Expected 200, got {res.status_code}"
        dr = res.json()
        assert dr["min_date"] == "2026-02-01", f"Unexpected minimum date: {dr['min_date']}"
        assert dr["max_date"] == "2027-12-31", f"Unexpected maximum date: {dr['max_date']}"
        assert dr["total_days"] == 699, f"Unexpected total days: {dr['total_days']}"
        print(f"  Passed! Date bounds: {dr['min_date']} to {dr['max_date']} ({dr['total_days']} total days)")

        # Test 4: Single-day Weather Query
        print("\n[4/7] Testing GET /api/weather/daily ...")
        res = client.get("/api/weather/daily?prefecture=Tokyo&date=2026-06-15")
        assert res.status_code == 200, f"Expected 200, got {res.status_code}"
        w = res.json()
        print(f"  Passed! Tokyo 2026-06-15 max temp: {w['metrics'].get('temperature_2m_max')}°C, rain: {w['metrics'].get('rain_sum')}mm")

        hokkaido = client.get("/api/weather/daily?prefecture=Hokkaido&date=2026-02-01")
        assert hokkaido.status_code == 200, f"Hokkaido lookup failed: {hokkaido.status_code} {hokkaido.text}"
        mie = client.get("/api/weather/daily?prefecture=Mie&date=2026-02-01")
        assert mie.status_code == 200, f"Mie lookup failed: {mie.status_code} {mie.text}"

        niigata_daily = client.get("/api/weather/daily?prefecture=Niigata&date=2026-11-30")
        assert niigata_daily.status_code == 404, (
            "The consolidated forecast has no Niigata row for 2026-11-30; "
            f"unexpected response: {niigata_daily.status_code} {niigata_daily.text}"
        )
        assert "does not contain this prefecture/date" in niigata_daily.json()["detail"]

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

        for prefecture in ("Yamagata",):
            snow_res = client.post(
                "/api/predict",
                json={"prefecture": prefecture, "date": "2026-06-15", "hazards": ["snow"]},
            )
            assert snow_res.status_code == 200, (
                f"Snow prediction failed for {prefecture}: {snow_res.status_code} {snow_res.text}"
            )
            snow_prediction = snow_res.json()
            snow_risk = next(risk for risk in snow_prediction["risks"] if risk["hazard"] == "snow")
            assert snow_prediction["execution_mode"] == "inference", (
                f"Expected model-backed snow prediction for {prefecture}"
            )
            assert snow_risk["model_name"].endswith("(Snow: Yamagata)"), (
                f"Expected the prefecture-specific snow model, got {snow_risk['model_name']}"
            )
            assert snow_risk["risk_level"] in {"Low", "Medium", "High"}
        niigata_snow = client.post(
            "/api/predict",
            json={"prefecture": "Niigata", "date": "2026-11-30", "hazards": ["snow"]},
        )
        assert niigata_snow.status_code == 404, "Niigata has no daily forecast row for 2026-11-30"
        assert "does not contain this prefecture/date" in niigata_snow.json()["detail"]
        print("  Confirmed Niigata 2026-11-30 has no source weather row; requests return 404.")

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
        typhoon_risk = next(r for r in pred["risks"] if r["hazard"] == "typhoon")
        assert typhoon_risk["risk_level"] == "Unassessed", f"Unexpected typhoon risk level: {typhoon_risk['risk_level']}"
        assert typhoon_risk["threshold_exceeded"] is False, "Unvalidated profile match must not trigger a typhoon warning"
        assert typhoon_risk["probability"] is None, "Profile-match probability must not be exposed as occurrence risk"
        assert typhoon_risk["profile_match_class"] in {"Low", "Medium", "High"}
        assert "profile_match_probabilities" in typhoon_risk
        assert pred["overall_risk_level"] != "High", "Unassessed typhoon profile match must not inflate overall risk"
        for r in pred["risks"]:
            val = f" ({r['predicted_value']}{r['unit']})" if r.get('predicted_value') else f" (prob: {r.get('probability')})"
            print(f"    - {r['hazard'].capitalize()}: {r['risk_level']}{val} | Model: {r['model_name']}")

    print("\n" + "=" * 60)
    print("ALL 7 API VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
