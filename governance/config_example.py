# Copy this file to config.py and edit values.

# Database
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "your_mysql_password",
    "database": "agent_governance",
}

# Email (SMTP)
EMAIL_CONFIG = {
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 587,
    "smtp_user": "your-email@gmail.com",
    "smtp_password": "your-app-password",
    "from_email": "your-email@gmail.com",
    "to_emails": ["your-email@gmail.com", "security@example.com"],
}
