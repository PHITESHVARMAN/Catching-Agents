from governance import config
from governance.database_handler import DatabaseHandler
from governance.email_handler import EmailHandler


class ResponseHandler:
    def __init__(self, profile):
        self.profile = profile

        # DB connection from governance/config.py
        self.db_handler = DatabaseHandler(**config.DB_CONFIG)
        self.db_handler.ensure_table_exists()

        # SMTP setup from governance/config.py
        self.email_handler = EmailHandler(**config.EMAIL_CONFIG)

    def handle_violation(self, violation: dict) -> None:
        print("\n" + "=" * 65)
        print("GOVERNANCE VIOLATION DETECTED")
        print("=" * 65)
        print("Agent:", violation.get("agent_name"))
        print("Tool:", violation.get("tool_name"))
        print("Type:", violation.get("violation_type"))
        print("Severity:", violation.get("severity"))
        print("Description:", violation.get("description"))
        print("Blocked:", violation.get("blocked"))
        print("=" * 65)

        # 1. Save in MySQL first.
        violation_id = self.db_handler.save_violation(violation)

        if violation_id is None:
            print("[DB] ERROR: Violation was not saved.")
        else:
            print(f"[DB] Violation saved successfully. ID: {violation_id}")

        # 2. Send the email alert for block or alert_only mode.
        if self.profile.should_alert():
            email_sent = self.email_handler.send_violation_alert(violation)

            if email_sent:
                print("[EMAIL] Alert sent successfully.")
            else:
                print("[EMAIL] ERROR: Alert was not sent. Check SMTP details.")
        else:
            print("[EMAIL] Skipped because enforcement_mode is log_only.")