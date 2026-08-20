from governance import config
from governance.database_handler import DatabaseHandler
from governance.email_handler import EmailHandler

print("DB config:", config.DB_CONFIG)
print("Email config:", config.EMAIL_CONFIG)

# Test DB
db = DatabaseHandler(**config.DB_CONFIG)
db.ensure_table_exists()

test_violation = {
    "agent_name": "test_agent",
    "session_id": "test_session",
    "tool_name": "test_tool",
    "violation_type": "test_breach",
    "severity": "high",
    "description": "Test violation from test script",
    "blocked": True,
    "tool_input": {"query": "test"},
}

vid = db.save_violation(test_violation)
print("Saved violation id:", vid)

rows = db.get_violations(limit=5)
print("Last violations from DB:", rows)

db.close()

# Test email
email = EmailHandler(**config.EMAIL_CONFIG)

ok = email.send_violation_alert(test_violation)
print("Email sent?", ok)