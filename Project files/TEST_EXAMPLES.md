# Sample Test Cases for Startup Prediction Model

## Test Case 1: Well-Funded Tech Startup (Likely Acquired)
```bash
curl -s -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 37.7749,
    "longitude": -122.4194,
    "age_first_funding": 2,
    "age_last_funding": 5,
    "age_first_milestone": 1,
    "age_last_milestone": 4,
    "relationships": 25,
    "funding_rounds": 5,
    "total_funding": 15000000,
    "milestones": 8,
    "avg_participants": 12.5,
    "state": "CA",
    "category": "software",
    "has_vc": 1,
    "has_angel": 1,
    "has_roundA": 1,
    "has_roundB": 1,
    "has_roundC": 1,
    "has_roundD": 0,
    "is_top500": 1
  }'
```

## Test Case 2: Early Stage Startup (May Close)
```bash
curl -s -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 40.7128,
    "longitude": -74.0060,
    "age_first_funding": 1,
    "age_last_funding": 2,
    "age_first_milestone": 0.5,
    "age_last_milestone": 1.5,
    "relationships": 5,
    "funding_rounds": 1,
    "total_funding": 500000,
    "milestones": 2,
    "avg_participants": 3.2,
    "state": "NY",
    "category": "web",
    "has_vc": 0,
    "has_angel": 1,
    "has_roundA": 0,
    "has_roundB": 0,
    "has_roundC": 0,
    "has_roundD": 0,
    "is_top500": 0
  }'
```

## Test Case 3: Mature Biotech Startup
```bash
curl -s -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 42.3601,
    "longitude": -71.0589,
    "age_first_funding": 3,
    "age_last_funding": 6,
    "age_first_milestone": 2,
    "age_last_milestone": 5,
    "relationships": 18,
    "funding_rounds": 4,
    "total_funding": 25000000,
    "milestones": 6,
    "avg_participants": 8.7,
    "state": "MA",
    "category": "biotech",
    "has_vc": 1,
    "has_angel": 1,
    "has_roundA": 1,
    "has_roundB": 1,
    "has_roundC": 1,
    "has_roundD": 1,
    "is_top500": 1
  }'
```

## Test Case 4: Mobile Gaming Startup (May Close)
```bash
curl -s -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 37.3382,
    "longitude": -121.8863,
    "age_first_funding": 0.5,
    "age_last_funding": 1.5,
    "age_first_milestone": 0.2,
    "age_last_milestone": 1,
    "relationships": 8,
    "funding_rounds": 2,
    "total_funding": 2000000,
    "milestones": 3,
    "avg_participants": 5.1,
    "state": "CA",
    "category": "games_video",
    "has_vc": 0,
    "has_angel": 1,
    "has_roundA": 1,
    "has_roundB": 0,
    "has_roundC": 0,
    "has_roundD": 0,
    "is_top500": 0
  }'
```

## Field Explanations

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| latitude | float | 37.7749 | Geographic latitude (default 0 if not provided) |
| longitude | float | -122.4194 | Geographic longitude (default 0 if not provided) |
| age_first_funding | float | 2 | Years old when first funded |
| age_last_funding | float | 5 | Years old at last funding round |
| age_first_milestone | float | 1 | Years old at first milestone |
| age_last_milestone | float | 4 | Years old at last milestone |
| relationships | int | 25 | Number of relationships/partnerships |
| funding_rounds | int | 5 | Total number of funding rounds |
| total_funding | float | 15000000 | Total funding received in USD |
| milestones | int | 8 | Number of milestones achieved |
| avg_participants | float | 12.5 | Average participants per round |
| state | string | "CA" | State code (CA, NY, MA, TX, other) |
| category | string | "software" | Business category |
| has_vc | 0 or 1 | 1 | Has VC funding |
| has_angel | 0 or 1 | 1 | Has angel investor |
| has_roundA | 0 or 1 | 1 | Has Series A |
| has_roundB | 0 or 1 | 1 | Has Series B |
| has_roundC | 0 or 1 | 1 | Has Series C |
| has_roundD | 0 or 1 | 0 | Has Series D |
| is_top500 | 0 or 1 | 1 | Is in top 500 list |

## Expected Output Format

**Success Response (HTTP 200):**
```json
{
  "prediction": "Acquired",
  "success": true
}
```

or

```json
{
  "prediction": "Closed",
  "success": true
}
```

**Error Response (HTTP 400):**
```json
{
  "error": "Missing required field: age_first_funding",
  "success": false
}
```

## How to Test

1. **Make sure the Flask server is running:**
   ```bash
   python3 app.py
   ```
   (or on port 5001 if 5000 is busy)

2. **Copy-paste one of the test cases above** and run it in a terminal

3. **Check the response:**
   - If you see `"prediction": "Acquired"` or `"Closed"`, the model is working!
   - If you see an error message, check the field names and data types

## What Each Case Tests

- **Case 1**: Well-funded, mature software startup in Silicon Valley → Should predict **Acquired**
- **Case 2**: Early-stage web startup with minimal funding → Should predict **Closed**
- **Case 3**: Mature biotech with heavy funding rounds → Should predict **Acquired**
- **Case 4**: Mobile gaming startup with moderate funding → Should predict **Closed**

Try each case and let me know the results!
