from src.sonarqube.report_generator import SonarQubeReportGenerator
from src.core.config import settings


def main():
    # Configure these values
    PROJECT_KEY = settings.SONAR_QUBE_PROJECT_KEY
    OUTPUT_FILE = "output/report.pdf"

    try:
        report_generator = SonarQubeReportGenerator()
        report_generator.generate_report(PROJECT_KEY, OUTPUT_FILE)
        print(f"Report generated successfully: {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error generating report: {str(e)}")


if __name__ == "__main__":
    main()
