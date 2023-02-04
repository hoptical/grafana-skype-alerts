# Skype Notifier



## Getting started

To test skype web hook, build the project like:
`make skype`

Then call the api to post a message in your Skype channel:
```shell
curl --location --request POST 'http://localhost:7654/SkypeNotifier/Your Skype channel' \
--header 'Content-Type: application/json' \
--data-raw '{ "title":  "[Alerting] Test notification",
"ruleId": 7008839925862512012,  "ruleName":  "Test notification",  "state ":  "alerting",
"evalMatches": [{ "value": 100,  "metric":  "High value",  "tags": null}, { "value": 200,  "metric":  "Higher Value",  "tags": null}],
"orgId": 0,  "dashboardId": 1,  "panelId": 1,  "tags": {},  "ruleUrl":  "http://localhost:3000/",
"imageUrl":  "https://grafana.com/assets/img/blog/mixed_styles.png",
"message":  "Someone is testing the alert notification within Grafana."}'
```

Also remember the `Automated Grafana` user should be
added first to your Skype channel
