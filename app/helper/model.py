from pydantic import BaseModel, Field
from typing import Any, Dict, List
from skpy import SkypeMsg

class Labels(BaseModel):
    alertname: str
    team: str
    zone: str


class Annotations(BaseModel):
    description: str
    runbook_url: str
    summary: str


class Alert(BaseModel):
    status: str
    labels: Labels
    annotations: Annotations
    startsAt: str
    endsAt: str
    generatorURL: str
    fingerprint: str
    silenceURL: str
    dashboardURL: str
    panelURL: str
    valueString: str


class CommonLabels(BaseModel):
    team: str


class GrafanaAlert(BaseModel):
    receiver: str
    status: str
    orgId: int
    alerts: List[Alert]
    groupLabels: Dict[str, Any]
    commonLabels: CommonLabels
    commonAnnotations: Dict[str, Any]
    externalURL: str
    version: str
    groupKey: str
    truncatedAlerts: int
    title: str
    state: str
    message: str

    def __str__(self):
        return (
            f"{SkypeMsg.bold('GrafanaAlert')}:\n"
            f"{SkypeMsg.bold('receiver')}: {self.receiver}\n"
            f"{SkypeMsg.bold('status')}: {self.status}\n"
            f"{SkypeMsg.bold('orgId')}: {self.orgId}\n"
            f"{SkypeMsg.bold('alerts')}: {', '.join(str(alert) for alert in self.alerts)}\n"
            f"{SkypeMsg.bold('groupLabels')}: {', '.join(str(label) for label in self.groupLabels)}\n"
            f"{SkypeMsg.bold('commonLabels')}: {self.commonLabels}\n"
            f"{SkypeMsg.bold('commonAnnotations')}: {', '.join(str(annotation) for annotation in self.commonAnnotations)}\n"
            f"{SkypeMsg.bold('externalURL')}: {self.externalURL}\n"
            f"{SkypeMsg.bold('version')}: {self.version}\n"
            f"{SkypeMsg.bold('groupKey')}: {self.groupKey}\n"
            f"{SkypeMsg.bold('truncatedAlerts')}: {self.truncatedAlerts}\n"
            f"{SkypeMsg.bold('title')}: {self.title}\n"
            f"{SkypeMsg.bold('state')}: {self.state}\n"
            f"{SkypeMsg.bold('message')}: {self.message}\n"
        )

