from dataclasses import dataclass
from src.core.sonarqube_client import SonarQubeClient
from src.core.pdf_generator import PDFGenerator
from src.core.config import settings
from src.core.logger import logger
from typing import List, Dict, Any


@dataclass
class SonarQubeReportGenerator:
    """
    A class to generate SonarQube analysis reports.

    This class interacts with the SonarQube API to fetch project overview and detailed issue data, and generates a PDF report
    using the fetched data. It uses the SonarQubeClient to make API requests and the PDFGenerator to create the PDF report.

    Attributes:
        client (SonarQubeClient): The client to interact with the SonarQube API.
    """

    client: SonarQubeClient

    def __init__(self):
        """
        Initializes the SonarQubeReportGenerator with the SonarQube API client.
        """
        self.client = SonarQubeClient(
            settings.SONAR_QUBE_URL, settings.SONAR_QUBE_AUTH_TOKEN
        )

    def _get_project_overview(self, project_key: str) -> Dict[str, Any]:
        """
        Fetches the project overview data from the SonarQube API.

        Args:
            project_key (str): The key of the project.

        Returns:
            Dict[str, Any]: The overview data of the project, including measures for issues and metrics.
        """
        url = "api/issues/search"
        params = {
            "componentKeys": project_key,
            "facets": "severities,types,sonarsourceSecurity",
            "resolved": "false",
        }
        issues_data = self.client.get(url, params)
        if not issues_data:
            return {}

        metrics_url = "api/measures/component"
        metrics_params = {
            "component": project_key,
            "metricKeys": "bugs,vulnerabilities,code_smells,security_hotspots",
        }
        metrics_data = self.client.get(metrics_url, metrics_params)

        overview = {"component": {"measures": []}}

        if "facets" in issues_data:
            for facet in issues_data["facets"]:
                if facet["property"] == "severities":
                    severity_counts = {v["val"]: v["count"] for v in facet["values"]}
                    for severity, count in severity_counts.items():
                        overview["component"]["measures"].append(
                            {
                                "metric": f"issues_{severity.lower()}",
                                "value": str(count),
                            }
                        )
                elif facet["property"] == "types":
                    type_counts = {v["val"]: v["count"] for v in facet["values"]}
                    for issue_type, count in type_counts.items():
                        overview["component"]["measures"].append(
                            {
                                "metric": f"issues_{issue_type.lower()}",
                                "value": str(count),
                            }
                        )

        if metrics_data and "component" in metrics_data:
            overview["component"]["measures"].extend(
                metrics_data["component"].get("measures", [])
            )

        return overview

    def _get_detailed_issues(self, project_key: str) -> List[Dict[str, Any]]:
        """
        Fetches the detailed issues data from the SonarQube API.

        Args:
            project_key (str): The key of the project.

        Returns:
            List[Dict[str, Any]]: The list of detailed issues for the project.
        """
        url = "api/issues/search"
        params = {"componentKeys": project_key, "ps": 500, "p": 1}

        all_issues = []
        while True:
            data = self.client.get(url, params)
            if not data.get("issues"):
                break

            all_issues.extend(data["issues"])

            if len(all_issues) >= data["total"]:
                break

            params["p"] += 1

        return all_issues

    def _get_rule_details(self, rule_key: str) -> Dict[str, Any]:
        """
        Fetches the rule details from the SonarQube API.

        Args:
            rule_key (str): The key of the rule.

        Returns:
            Dict[str, Any]: The details of the rule.
        """
        url = "api/rules/show"
        params = {"key": rule_key}
        return self.client.get(url, params)

    def generate_report(self, project_key: str, output_file: str):
        """
        Generates the PDF report for the given project.

        Args:
            project_key (str): The key of the project.
            output_file (str): The path to the output PDF file.
        """
        overview = self._get_project_overview(project_key)
        detailed_issues = self._get_detailed_issues(project_key)
        pdf_generator = PDFGenerator(output_file)
        pdf_generator.generate_pdf(
            project_key, overview, detailed_issues, self._get_rule_details
        )
        logger.info(f"Report generated successfully for project: {project_key}")
