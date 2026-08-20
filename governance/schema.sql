CREATE DATABASE IF NOT EXISTS agent_governance
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE agent_governance;

CREATE TABLE IF NOT EXISTS violations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    agent_name VARCHAR(100) NOT NULL,
    session_id VARCHAR(100),
    tool_name VARCHAR(100) NOT NULL,
    violation_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    description TEXT,
    blocked BOOLEAN DEFAULT TRUE,
    tool_input JSON,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
