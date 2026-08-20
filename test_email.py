from datetime import datetime

from governance import config
from governance.email_handler import EmailHandler


print("Testing SMTP email configuration...")
print("SMTP host:", config.EMAIL_CONFIG["smtp_host"])
print("SMTP port:", config.EMAIL_CONFIG["smtp_port"])
print("From email:", config.EMAIL_CONFIG["from_email"])
print("Recipient count:", len(config.EMAIL_CONFIG["to_emails"]))

test_violation = {
    "agent_name": "support_agent",
    "session_id": "manual_email_test",
    "tool_name": "access_customer_db",
    "violation_type": "policy_breach",
    "severity": "high",
    "rule_matched": "approved_tools",
    "description": "Manual SMTP test: unauthorized customer database access.",
    "blocked": True,
    "detected_at": datetime.now().isoformat(),
    "tool_input": {
        "customer_id": "4521"
    },
}

email_handler = EmailHandler(**config.EMAIL_CONFIG)

email_sent = email_handler.send_violation_alert(test_violation)

print("\nEmail sent?", email_sent)

if email_sent:
    print("Check the inbox and Spam/Junk folder for the governance alert.")
else:
    print("Email was not sent. Read the [EMAIL] error printed above.")