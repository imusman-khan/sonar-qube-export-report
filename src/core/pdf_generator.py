from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    PageBreak,
    Preformatted,
)
from reportlab.lib.units import inch
from datetime import datetime
import re
from typing import List, Dict, Any


class PDFGenerator:
    """
    A class to generate PDF reports for SonarQube analysis.

    This class handles the creation of PDF documents that include an overview of the project and detailed issue analysis.
    It uses ReportLab to generate the PDF and applies custom styles for better readability.

    Attributes:
        doc (SimpleDocTemplate): The document template for the PDF.
        styles (getSampleStyleSheet): The stylesheet for the PDF elements.
    """

    def __init__(self, output_file: str):
        """
        Initializes the PDFGenerator with the specified output file.

        Args:
            output_file (str): The path to the output PDF file.
        """
        self.doc = SimpleDocTemplate(
            output_file,
            pagesize=landscape(letter),
            rightMargin=36,
            leftMargin=36,
            topMargin=50,
            bottomMargin=50,
        )
        self.styles = getSampleStyleSheet()
        self._setup_styles()

    def _setup_styles(self):
        """
        Sets up the custom styles for the PDF document.

        This method adds custom paragraph styles for various elements in the PDF, such as issue titles, code blocks,
        issue descriptions, bullet points, section headers, report headers, and project info.
        """
        self.styles.add(
            ParagraphStyle(
                "IssueTitle",
                parent=self.styles["Heading3"],
                fontSize=14,
                textColor=colors.HexColor("#2B547E"),
                spaceAfter=15,
                spaceBefore=10,
                leading=20,
                borderColor=colors.HexColor("#E0E0E0"),
                borderWidth=1,
                borderPadding=10,
                borderRadius=5,
            )
        )
        self.styles.add(
            ParagraphStyle(
                "CodeBlock",
                parent=self.styles["Code"],
                fontSize=8.5,
                fontName="Courier",
                leftIndent=0,
                rightIndent=0,
                spaceAfter=15,
                spaceBefore=10,
                backColor=colors.HexColor("#F5F5F5"),
                borderColor=colors.HexColor("#DDDDDD"),
                borderWidth=1,
                borderPadding=12,
                leading=12,
            )
        )
        self.styles.add(
            ParagraphStyle(
                "IssueDescription",
                parent=self.styles["Normal"],
                fontSize=11,
                leftIndent=20,
                rightIndent=20,
                spaceAfter=8,
                spaceBefore=8,
                leading=16,
                textColor=colors.HexColor("#333333"),
                bulletIndent=40,
                firstLineIndent=0,
            )
        )
        self.styles.add(
            ParagraphStyle(
                "BulletPoint",
                parent=self.styles["IssueDescription"],
                leftIndent=40,
                firstLineIndent=-20,
                spaceBefore=4,
                spaceAfter=4,
            )
        )
        self.styles.add(
            ParagraphStyle(
                "SectionHeader",
                parent=self.styles["Heading4"],
                fontSize=12,
                textColor=colors.HexColor("#1A4B7C"),
                spaceBefore=20,
                spaceAfter=10,
                leading=18,
                borderColor=colors.HexColor("#1A4B7C"),
                borderWidth=0,
                borderPadding=5,
                borderRadius=3,
            )
        )
        self.styles.add(
            ParagraphStyle(
                "ReportHeader",
                parent=self.styles["Heading1"],
                fontSize=28,
                textColor=colors.HexColor("#1A4B7C"),
                spaceAfter=20,
                leading=32,
                alignment=1,
            )
        )
        self.styles.add(
            ParagraphStyle(
                "ProjectInfo",
                parent=self.styles["Normal"],
                fontSize=12,
                textColor=colors.HexColor("#666666"),
                spaceAfter=30,
                alignment=1,
            )
        )

    def generate_pdf(
        self,
        project_key: str,
        overview: Dict[str, Any],
        detailed_issues: List[Dict[str, Any]],
        get_rule_details_func,
    ):
        """
        Generates the PDF report for the given project.

        Args:
            project_key (str): The key of the project.
            overview (Dict[str, Any]): The overview data of the project.
            detailed_issues (List[Dict[str, Any]]): The list of detailed issues.
            get_rule_details_func (Callable): A function to get rule details.
        """
        elements = []
        elements.append(
            Paragraph(
                f'<font color="#1A4B7C" size="28"><b>SonarQube Analysis Report</b></font>',
                self.styles["ReportHeader"],
            )
        )
        project_info = f"""
            <font color="#333333" size="14"><b>{project_key}</b></font><br/>
            <font color="#666666">Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}</font>
        """
        elements.append(Paragraph(project_info, self.styles["ProjectInfo"]))
        self._add_overview(elements, overview)
        self._add_detailed_issues(elements, detailed_issues, get_rule_details_func)
        self.doc.build(
            elements,
            onFirstPage=self._add_header_footer,
            onLaterPages=self._add_header_footer,
        )

    def _add_overview(self, elements: List[Any], overview: Dict[str, Any]):
        """
        Adds the project overview to the PDF.

        Args:
            elements (List[Any]): The list of PDF elements.
            overview (Dict[str, Any]): The overview data of the project.
        """
        if overview and "component" in overview:
            measures_dict = {
                m["metric"]: m["value"] for m in overview["component"]["measures"]
            }
            overview_data = [
                ["Issue Type", "Count"],
                ["Critical Issues", measures_dict.get("issues_critical", "0")],
                ["Major Issues", measures_dict.get("issues_major", "0")],
                ["Minor Issues", measures_dict.get("issues_minor", "0")],
                ["Info Issues", measures_dict.get("issues_info", "0")],
                ["Code Smells", measures_dict.get("issues_code_smell", "0")],
                ["Bugs", measures_dict.get("issues_bug", "0")],
                ["Vulnerabilities", measures_dict.get("issues_vulnerability", "0")],
            ]
            overview_table = Table(
                overview_data,
                colWidths=[3 * inch, 1 * inch],
                style=[
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2B547E")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 12),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("PADDING", (0, 0), (-1, -1), 6),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ALIGN", (1, 0), (1, -1), "CENTER"),
                ],
            )
            elements.append(overview_table)
            elements.append(Spacer(1, 20))

    def _add_detailed_issues(
        self,
        elements: List[Any],
        detailed_issues: List[Dict[str, Any]],
        get_rule_details_func,
    ):
        """
        Adds the detailed issues to the PDF.

        Args:
            elements (List[Any]): The list of PDF elements.
            detailed_issues (List[Dict[str, Any]]): The list of detailed issues.
            get_rule_details_func (Callable): A function to get rule details.
        """
        elements.append(Spacer(1, 30))
        elements.append(
            Paragraph(
                '<font color="#1A4B7C" size="20"><b>Detailed Issue Analysis</b></font>',
                self.styles["ReportHeader"],
            )
        )
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("Issue Details", self.styles["Heading2"]))
        for issue in detailed_issues:
            elements.append(PageBreak())
            elements.append(
                Paragraph(
                    f'<font color="#999999" size="9">ISSUE #{detailed_issues.index(issue) + 1}</font>',
                    self.styles["Normal"],
                )
            )
            severity = issue.get("severity", "MAJOR")
            severity_colors = {
                "BLOCKER": ("#DC3545", "#FFF"),
                "CRITICAL": ("#E94F37", "#FFF"),
                "MAJOR": ("#FFA500", "#000"),
                "MINOR": ("#FFC107", "#000"),
                "INFO": ("#28A745", "#FFF"),
            }
            bg_color, text_color = severity_colors.get(severity, ("#666666", "#FFF"))
            issue_title = f"""
                <div style="background-color: #F8F9FA; padding: 15px; border-radius: 5px;">
                    <font color="{bg_color}">●</font>
                    <font color="{bg_color}"><b>{severity}</b></font>
                    <font color="#666666"> | {issue.get('type', 'Issue')}</font>
                    <br/><br/>
                    <font color="#333333" size="12">{issue.get('message', 'N/A')}</font>
                </div>
            """
            elements.append(Paragraph(issue_title, self.styles["IssueTitle"]))
            elements.append(
                Paragraph(
                    f'<font color="#CCCCCC">{"─" * 80}</font>', self.styles["Normal"]
                )
            )
            elements.append(
                Paragraph(
                    '<font color="#1A4B7C">📍 Where is this issue?</font>',
                    self.styles["SectionHeader"],
                )
            )
            file_path = issue.get("component", "").split(":")[-1]
            location = f"""
                <b>File:</b> {file_path}
                <br/>
                <b>Line:</b> {issue.get('line', 'N/A')}
            """
            elements.append(Paragraph(location, self.styles["IssueDescription"]))
            elements.append(
                Paragraph(
                    '<font color="#1A4B7C">❓ Why is this an issue?</font>',
                    self.styles["SectionHeader"],
                )
            )
            rule_details = get_rule_details_func(issue.get("rule"))
            if "rule" in rule_details:
                rule = rule_details["rule"]
                if "descriptionSections" in rule:
                    for section in rule["descriptionSections"]:
                        if section["key"] == "root_cause":
                            cleaned_content = self._clean_html(section["content"])
                            paragraphs = cleaned_content.split("\n\n")
                            for para in paragraphs:
                                if para.strip():
                                    if para.strip().startswith("•"):
                                        elements.append(
                                            Paragraph(
                                                para.strip(), self.styles["BulletPoint"]
                                            )
                                        )
                                    else:
                                        elements.append(
                                            Paragraph(
                                                para.strip(),
                                                self.styles["IssueDescription"],
                                            )
                                        )
                                    elements.append(Spacer(1, 4))
            elements.append(
                Paragraph(
                    '<font color="#1A4B7C">🔧 How can I fix it?</font>',
                    self.styles["SectionHeader"],
                )
            )
            for section in rule["descriptionSections"]:
                if section["key"] == "how_to_fix":
                    parts = section["content"].split("<pre")
                    if parts:
                        explanation = self._clean_html(parts[0])
                        paragraphs = explanation.split("\n\n")
                        for para in paragraphs:
                            if para.strip():
                                if para.strip().startswith("•"):
                                    elements.append(
                                        Paragraph(
                                            para.strip(), self.styles["BulletPoint"]
                                        )
                                    )
                                else:
                                    elements.append(
                                        Paragraph(
                                            para.strip(),
                                            self.styles["IssueDescription"],
                                        )
                                    )
                                elements.append(Spacer(1, 4))
                        for i in range(1, len(parts)):
                            part = parts[i]
                            if 'data-diff-type="noncompliant">' in part:
                                elements.append(
                                    Paragraph(
                                        '<font color="#DC3545">⚠ Noncompliant Code Example:</font>',
                                        self.styles["SectionHeader"],
                                    )
                                )
                                code = part.split('data-diff-type="noncompliant">')[
                                    1
                                ].split("</pre>")[0]
                                elements.append(
                                    self._format_code_block(
                                        [
                                            {"line": i + 1, "code": line}
                                            for i, line in enumerate(
                                                code.strip().split("\n")
                                            )
                                        ],
                                        1,
                                        self.styles["CodeBlock"],
                                    )
                                )
                            elif 'data-diff-type="compliant">' in part:
                                elements.append(
                                    Paragraph(
                                        '<font color="#28A745">✓ Compliant Solution:</font>',
                                        self.styles["SectionHeader"],
                                    )
                                )
                                code = part.split('data-diff-type="compliant">')[
                                    1
                                ].split("</pre>")[0]
                                elements.append(
                                    self._format_code_block(
                                        [
                                            {"line": i + 1, "code": line}
                                            for i, line in enumerate(
                                                code.strip().split("\n")
                                            )
                                        ],
                                        1,
                                        self.styles["CodeBlock"],
                                    )
                                )
                            elements.append(Spacer(1, 10))
            elements.append(Spacer(1, 20))
            elements.append(
                Paragraph(
                    f'<font color="#EEEEEE">{"═" * 100}</font>', self.styles["Normal"]
                )
            )
            elements.append(Spacer(1, 20))

    def _add_header_footer(self, canvas, doc):
        """
        Adds header and footer to each page of the PDF.

        Args:
            canvas (Canvas): The canvas object to draw on.
            doc (SimpleDocTemplate): The document template.
        """
        canvas.saveState()
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(colors.HexColor("#999999"))
        footer_text = f"Page {doc.page} | Generated by SonarQube"
        canvas.drawCentredString(doc.pagesize[0] / 2, 30, footer_text)
        canvas.restoreState()

    def _format_code_block(
        self,
        code_lines: List[Dict[str, Any]],
        highlight_line: int,
        style: ParagraphStyle,
    ) -> Preformatted:
        """
        Formats a block of code with line numbers and syntax highlighting.

        Args:
            code_lines (List[Dict[str, Any]]): The list of code lines with line numbers.
            highlight_line (int): The line number to highlight.
            style (ParagraphStyle): The style to apply to the code block.

        Returns:
            Preformatted: The formatted code block.
        """
        formatted_lines = []
        max_line_length = 120
        for line in code_lines:
            line_num = str(line["line"]).rjust(4)
            code = line["code"]
            code = re.sub(r'<span class="[^"]*">', "", code)
            code = code.replace("</span>", "")
            if len(code) > max_line_length:
                chunks = [
                    code[i : i + max_line_length]
                    for i in range(0, len(code), max_line_length)
                ]
                formatted_lines.append(f"{line_num} │ {chunks[0]} ↩")
                for chunk in chunks[1:]:
                    formatted_lines.append(f"     │ {chunk}")
                if line["line"] == highlight_line:
                    formatted_lines[-1] += " <<<"
            else:
                if line["line"] == highlight_line:
                    formatted_lines.append(f"{line_num} │ {code} <<<")
                else:
                    formatted_lines.append(f"{line_num} │ {code}")
        return Preformatted("\n".join(formatted_lines), style)

    def _clean_html(self, html_content: str) -> str:
        """
        Cleans HTML content for PDF rendering with better formatting.

        Args:
            html_content (str): The HTML content to clean.

        Returns:
            str: The cleaned HTML content.
        """
        code_blocks = []

        def _save_code(match):
            code_blocks.append(match.group(1))
            return f"CODE_BLOCK_{len(code_blocks)-1}"

        text = html_content
        text = re.sub(r"<code>(.*?)</code>", _save_code, text, flags=re.DOTALL)
        text = re.sub(r"<a\s+[^>]*>(.*?)</a>", r"\1", text, flags=re.DOTALL)
        text = re.sub(r"</?para[^>]*>", "", text)
        text = re.sub(r"</?div[^>]*>", "", text)
        text = re.sub(r"</?span[^>]*>", "", text)
        text = re.sub(r"</?a[^>]*>", "", text)
        text = text.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
        text = (
            text.replace("<ul>", "\n")
            .replace("</ul>", "\n")
            .replace("<li>", "  • ")
            .replace("</li>", "\n")
        )
        text = re.sub(r"<h3>(.*?)</h3>", r"\n\n<b>\1</b>\n", text)
        text = re.sub(r"<h[1-6]>(.*?)</h[1-6]>", r"\n\n<b>\1</b>\n", text)
        text = text.replace("<p>", "").replace("</p>", "\n\n")
        text = text.replace("<strong>", "<b>").replace("</strong>", "</b>")
        text = text.replace("<em>", "<i>").replace("</em>", "</i>")
        text = re.sub(r"<(?!/?({})).*?>".format("|".join(["b", "i", "font"])), "", text)
        text = re.sub(r"\n\s*\n\s*\n", "\n\n", text)
        text = re.sub(r" +", " ", text)
        text = re.sub(r"\n +", "\n", text)
        text = text.replace("• ", "\n• ")
        text = re.sub(
            r"•\s*([^•]*?)(?=(?:\n|$))",
            lambda m: f"• {m.group(1).strip()}",
            text,
            flags=re.DOTALL,
        )

        def _restore_code(match):
            index = int(match.group(1))
            code_content = code_blocks[index]
            formatted_code = f'<font face="Courier">{code_content}</font>'
            return formatted_code

        text = re.sub(r"CODE_BLOCK_(\d+)", _restore_code, text)
        for tag in ["b", "i", "font"]:
            count = text.count(f"<{tag}") - text.count(f"</{tag}>")
            if count > 0:
                text += f"</{tag}>" * count
        text = text.strip()
        return text
