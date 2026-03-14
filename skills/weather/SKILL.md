# Weather Forecast Skill

## Metadata
- **Name**: weather
- **Version**: 1.0.0
- **Author**: OpenClaw
- **Description**: Weather forecast and alerts

## Requirements
- OpenWeatherMap API key (optional, can work without)

## Configuration
```yaml
# ~/.openclaw/skills/weather/config.yaml
api_key: your_openweathermap_api_key  # Optional
location: "Beijing"
units: metric  # or imperial
default_days: 3
```

## Usage
```python
# Get current weather
get_current(city="Shanghai")

# Get forecast
get_forecast(city="Dali", days=7)

# Compare cities
compare_cities(["Beijing", "Shanghai", "Guangzhou"])
```

## Tools
- get_current: Get current weather conditions
- get_forecast: Get weather forecast
- compare_cities: Compare weather across cities
- get_alerts: Get weather alerts
