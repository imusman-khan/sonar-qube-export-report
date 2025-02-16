# SonarQube Report Exporter 📊

A powerful tool to generate comprehensive PDF reports from SonarQube analysis, including key metrics, issues, and quality gates for easy sharing and insights. 🚀

## Features ✨

- Generate detailed PDF reports from SonarQube analysis
- Include project overview with key metrics
- Detailed issue analysis with severity levels
- Code snippets with compliant and non-compliant examples
- Beautiful and professional report formatting
- Easy to read and share with stakeholders

## Prerequisites 📋

Before you begin, ensure you have the following installed:

- Python 3.12 or higher
- Poetry (Python package manager)
- Access to a SonarQube instance with API access

## Installation 🛠️

1. Clone the repository:
   ```bash
   git clone https://github.com/imusman-khan/sonar-qube-export-report.git
   cd sonar-qube-export-report
   ```

2. Install dependencies using Poetry:
   ```bash
   make install
   ```

## Configuration ⚙️

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Configure your environment variables in `.env`:
   ```
   SONAR_QUBE_URL=<your-sonarqube-url>
   SONAR_QUBE_AUTH_TOKEN=<your-auth-token>
   SONAR_QUBE_PROJECT_KEY=<your-project-key>
   ```

   - `SONAR_QUBE_URL`: Your SonarQube instance URL
   - `SONAR_QUBE_AUTH_TOKEN`: Your SonarQube authentication token
   - `SONAR_QUBE_PROJECT_KEY`: The project key you want to analyze

## Usage 🚀

1. Run the report generator:
   ```bash
   make run
   ```

2. Format the code (if you're contributing):
   ```bash
   make format
   ```

## Report Structure 📑

The generated PDF report includes:

1. **Project Overview**
   - Project key and generation timestamp
   - Summary of issues by severity
   - Key metrics (bugs, vulnerabilities, code smells)

2. **Detailed Issue Analysis**
   - Issue severity and type
   - File location and line number
   - Root cause explanation
   - How to fix with code examples
   - Compliant and non-compliant code samples

## Project Architecture 🏗️

```
src/
├── core/
│   ├── config.py         # Configuration management
│   ├── logger.py         # Logging utilities
│   ├── pdf_generator.py  # PDF generation logic
│   └── sonarqube_client.py # SonarQube API client
├── sonarqube/
│   └── report_generator.py # Main report generation
└── main.py              # Entry point
```

## Contributing 🤝

1. Fork the repository
2. Create your feature branch
3. Install dependencies: `make install`
4. Format your code: `make format`
5. Commit your changes
6. Push to the branch
7. Create a Pull Request

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Support 💬

If you encounter any issues or have questions, please file an issue in the GitHub repository.

---

Built with ❤️ by Muhammad Usman Khan