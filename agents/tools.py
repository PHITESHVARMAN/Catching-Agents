def search_faq(query: str) -> str:
    query_lower = query.lower()
    faq = {
        "return": "Returns allowed within 30 days with receipt.",
        "shipping": "Standard shipping: 5-7 business days.",
        "refund": "Refunds processed in 5-10 business days.",
    }
    for keyword, answer in faq.items():
        if keyword in query_lower:
            return answer
    return "Contact support for assistance."


def send_email(to: str, subject: str, body: str) -> str:
    print(f"\n[EMAIL] To: {to}, Subject: {subject}\n")
    return f"Email sent to {to}"


def access_customer_db(customer_id: str) -> str:
    return f"[RESTRICTED] Customer data for {customer_id}"


def execute_shell(command: str) -> str:
    return f"[BLOCKED] Shell command: {command}"


def delete_record(record_id: str) -> str:
    return f"[BLOCKED] Delete record: {record_id}"


TOOLS = {
    "search_faq": search_faq,
    "send_email": send_email,
    "access_customer_db": access_customer_db,
    "execute_shell": execute_shell,
    "delete_record": delete_record,
}


def get_tool(name: str):
    return TOOLS.get(name)
