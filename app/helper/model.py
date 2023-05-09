from pydantic import BaseModel
from typing import Dict, List, Optional
from skpy import SkypeMsg
import textwrap
import re


class Alert(BaseModel):
    status: str
    labels: Dict[str, str]
    annotations: Dict[str, str]
    startsAt: str
    endsAt: str
    generatorURL: str
    fingerprint: str
    silenceURL: str
    dashboardURL: Optional[str]
    panelURL: Optional[str]
    valueString: str
    values: Optional[Dict[str, float]]
    imageURL: Optional[str]

    def model_representer(self):
        return (
            f"{SkypeMsg.bold('Labels')}: {self.labels}\n"
            f"{SkypeMsg.bold('Values')}: {self.value_string_parser()}\n"
            f"{SkypeMsg.bold('Starts at')}: {self.startsAt}\n"
            f"{SkypeMsg.bold('Ends at')}: {self.endsAt}\n"
            f"{SkypeMsg.link(url=self.panelURL, display='Panel URL')}\n"
            f"{SkypeMsg.link(url=self.silenceURL, display='Silence URL')}\n"
        )

    def value_string_parser(self):
        # Define the pattern
        pattern = r"'([^']*)'\s*labels=\{([^}]*)\}\s*value=([^\]]*)"

        # Find matches
        matches = re.findall(pattern, self.valueString)

        result = ""
        # Extract the values from the matches
        for match in matches:
            metric = match[0]
            labels = match[1]
            value = match[2]
            result += "{} = {} \t ".format(metric, value)
        return result


class GrafanaAlert(BaseModel):
    receiver: str
    status: str
    orgId: int
    alerts: List[Alert]
    groupLabels: Dict[str, str]
    commonLabels: Dict[str, str]
    commonAnnotations: Dict[str, str]
    externalURL: str
    version: str
    groupKey: str
    truncatedAlerts: int
    title: Optional[str]
    state: Optional[str]
    message: Optional[str]

    def model_representer(self, verbose=False):
        if verbose:
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
        else:
            join_char = "\n\n"
            text_indent = "    "
            alert_name = self.commonLabels.get("alertname", "")
            status_emoticon_dict = {
                "firing": SkypeMsg.emote("bomb"),
                "resolved": SkypeMsg.emote("smile"),
            }

            emote = status_emoticon_dict.get(self.status, "")
            return (
                f"{SkypeMsg.bold(alert_name)}:\n"
                f"{SkypeMsg.bold('Status')}: {self.status.upper()} {emote}\n"
                f"{SkypeMsg.bold('Alerts')}\n"
                f"{join_char.join(textwrap.indent(alert.model_representer(), text_indent) for alert in self.alerts)}\n"
            )
