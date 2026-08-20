import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailHandler:
    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        smtp_user: str,
        smtp_password: str,
        from_email: str,
        to_emails: list[str],
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.from_email = from_email
        self.to_emails = to_emails

    def send_violation_alert(self, violation: dict) -> bool:
        if not self.smtp_user:
            print("[EMAIL] SMTP user is missing in config.py")
            return False

        if not self.smtp_password:
            print("[EMAIL] SMTP password/App Password is missing in config.py")
            return False

        if not self.to_emails:
            print("[EMAIL] No recipients configured in config.py")
            return False

        subject = (
            f"[AI GOVERNANCE ALERT] "
            f"{violation.get('severity', 'high').upper()} - "
            f"{violation.get('tool_name', 'unknown')}"
        )

        body = f"""
AI AGENT GOVERNANCE VIOLATION

Agent Name: {violation.get("agent_name", "unknown")}
Tool Attempted: {violation.get("tool_name", "unknown")}
Violation Type: {violation.get("violation_type", "unknown")}
Severity: {violation.get("severity", "unknown")}
Blocked: {violation.get("blocked", True)}
Detected At: {violation.get("detected_at", "unknown")}

Description:
{violation.get("description", "No description")}
"""

        message = MIMEMultipart()
        message["From"] = self.from_email
        message["To"] = ", ".join(self.to_emails)
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        try:
            context = ssl.create_default_context()

            with smtplib.SMTP(
                self.smtp_host,
                self.smtp_port,
                timeout=20
            ) as server:
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(
                    self.from_email,
                    self.to_emails,
                    message.as_string(),
                )

            return True

        except smtplib.SMTPAuthenticationError as exc:
            print("[EMAIL] Authentication failed.")
            print("[EMAIL] Use a Gmail App Password, not your normal password.")
            print("[EMAIL] Details:", exc)
            return False

        except smtplib.SMTPException as exc:
            print("[EMAIL] SMTP error:", exc)
            return False

        except Exception as exc:
            print("[EMAIL] Unexpected error:", repr(exc))
            return False