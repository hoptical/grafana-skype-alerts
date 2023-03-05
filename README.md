https://gitlab.p.ir/data-team/data-engineering/skype-notifier/badges/main/pipeline.svg


# Skype Notifier
The skype notifier is a web server based on Fast API providing a webhook for Grafana Alerts. 

## Docs
For endpoints documentation please visit `/docs` URI.

## Installation
You can install the app either by docker compose or helm chart. 

### Docker Compose
```bash
docker compose up --build

```
The app is accessible on `http://localhost:8000`

### Helm
```bash
helm upgrade --install skype-notifier helm

```

## Usage
1. Create a group chat in skype.
2. Add `Automated Grafana` to that group chat.
3. Fetch the chat id by `/api/skype/grafana_alert/{room_name}` endpoint with GET method.
4. Post your message using `/api/skype/grafana_alert/{chat_id}` and defined body message with POST method.   

## Test
```
pytest -v
```
## Coverage
```bash
coverage run -m pytest
coverage report
```

