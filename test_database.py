from governance import config
from governance.database_handler import DatabaseHandler

db = DatabaseHandler(**config.DB_CONFIG)
#TEST: Ensure the table exists before inserting a test violation
db.ensure_table_exists()

test_violation = {
    "agent_name": "support_agent",
    "session_id": "manual_test_001",
    "tool_name": "access_customer_db",
    "violation_type": "policy_breach",
    "severity": "high",
    "rule_matched": "approved_tools",
    "description": "Manual DB test: unapproved customer DB tool.",
    "blocked": True,
    "tool_input": {
        "customer_id": "4521"
    },
    "raw_data": {
        "test": True
    }
}

violation_id = db.save_violation(test_violation)

print("Inserted violation ID:", violation_id)
print("Latest violations:")
print(db.get_violations(limit=5))

db.close()