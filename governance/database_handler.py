import json
import logging
from typing import Any, Dict, List, Optional

import mysql.connector
from mysql.connector import Error

logger = logging.getLogger(__name__)


class DatabaseHandler:
    """
    Handles MySQL database connection, table creation,
    violation insertion, and violation retrieval.
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 3306,
        user: str = "root",
        password: str = "",
        database: str = "agent_governance",
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

        self.connection: Optional[Any] = None

        self._create_database_if_needed()
        self._connect()

    def _server_config(self) -> Dict[str, Any]:
        """Configuration used to connect to MySQL server without selecting a DB."""
        return {
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "password": self.password,
        }

    def _database_config(self) -> Dict[str, Any]:
        """Configuration used to connect to the governance database."""
        return {
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "password": self.password,
            "database": self.database,
            "autocommit": False,
        }

    def _create_database_if_needed(self) -> None:
        """
        Create the configured database if it does not exist.

        This makes the project easier to run on a new local MySQL setup.
        """
        connection = None
        cursor = None

        try:
            connection = mysql.connector.connect(**self._server_config())
            cursor = connection.cursor()

            safe_database_name = self.database.replace("`", "")

            cursor.execute(
                f"""
                CREATE DATABASE IF NOT EXISTS `{safe_database_name}`
                CHARACTER SET utf8mb4
                COLLATE utf8mb4_unicode_ci
                """
            )

            connection.commit()
            print(f"[DB] Database checked/created: {self.database}")

        except Error as exc:
            print(f"[DB] Could not create/check database: {exc}")

        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()

    def _connect(self) -> bool:
        """
        Connect to the configured MySQL database.

        Returns:
            True when connection succeeds; False otherwise.
        """
        try:
            self.connection = mysql.connector.connect(**self._database_config())

            if self.connection.is_connected():
                print(
                    f"[DB] Connected successfully: "
                    f"{self.user}@{self.host}:{self.port}/{self.database}"
                )
                return True

        except Error as exc:
            print(f"[DB] Connection error: {exc}")
            self.connection = None

        return False

    def _ensure_connection(self) -> bool:
        """
        Ensure there is an active database connection.
        Reconnect when necessary.
        """
        if self.connection is None:
            return self._connect()

        try:
            self.connection.ping(reconnect=True, attempts=3, delay=1)
            return True

        except Error as exc:
            print(f"[DB] Connection lost; reconnecting. Details: {exc}")
            self.connection = None
            return self._connect()

    def ensure_table_exists(self) -> bool:
        """
        Create the violations table if it does not already exist.

        Returns:
            True when successful; False otherwise.
        """
        if not self._ensure_connection():
            print("[DB] Cannot create table because no DB connection is available.")
            return False

        cursor = None

        try:
            cursor = self.connection.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS violations (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    agent_name VARCHAR(100) NOT NULL,
                    session_id VARCHAR(100) NULL,
                    tool_name VARCHAR(100) NOT NULL,
                    violation_type VARCHAR(50) NOT NULL,
                    severity VARCHAR(20) NOT NULL,
                    rule_matched VARCHAR(255) NULL,
                    description TEXT NULL,
                    blocked BOOLEAN NOT NULL DEFAULT TRUE,
                    tool_input JSON NULL,
                    raw_data JSON NULL,
                    detected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

                    INDEX idx_violations_agent_name (agent_name),
                    INDEX idx_violations_tool_name (tool_name),
                    INDEX idx_violations_severity (severity),
                    INDEX idx_violations_detected_at (detected_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )

            self.connection.commit()
            print("[DB] Table checked/created successfully: violations")
            return True

        except Error as exc:
            print(f"[DB] Table creation error: {exc}")
            self.connection.rollback()
            return False

        finally:
            if cursor:
                cursor.close()

    def save_violation(self, violation: Dict[str, Any]) -> Optional[int]:
        """
        Save one governance violation to the MySQL violations table.

        Args:
            violation: Dictionary containing violation details.

        Returns:
            Inserted database ID, or None when insert fails.
        """
        if not self._ensure_connection():
            print("[DB] Cannot save violation because no DB connection is available.")
            return None

        cursor = None

        try:
            cursor = self.connection.cursor()

            query = """
                INSERT INTO violations (
                    agent_name,
                    session_id,
                    tool_name,
                    violation_type,
                    severity,
                    rule_matched,
                    description,
                    blocked,
                    tool_input,
                    raw_data
                )
                VALUES (
                    %(agent_name)s,
                    %(session_id)s,
                    %(tool_name)s,
                    %(violation_type)s,
                    %(severity)s,
                    %(rule_matched)s,
                    %(description)s,
                    %(blocked)s,
                    %(tool_input)s,
                    %(raw_data)s
                )
            """

            tool_input = violation.get("tool_input")
            raw_data = violation.get("raw_data")

            values = {
                "agent_name": violation.get("agent_name", "unknown"),
                "session_id": violation.get("session_id"),
                "tool_name": violation.get("tool_name", "unknown"),
                "violation_type": violation.get("violation_type", "policy_breach"),
                "severity": violation.get("severity", "high"),
                "rule_matched": violation.get("rule_matched"),
                "description": violation.get("description"),
                "blocked": bool(violation.get("blocked", True)),
                "tool_input": json.dumps(tool_input) if tool_input is not None else None,
                "raw_data": json.dumps(raw_data) if raw_data is not None else None,
            }

            cursor.execute(query, values)
            self.connection.commit()

            violation_id = cursor.lastrowid

            print(f"[DB] Violation saved successfully. ID: {violation_id}")
            return violation_id

        except (Error, TypeError, ValueError) as exc:
            print(f"[DB] Save error: {exc}")

            if self.connection:
                self.connection.rollback()

            return None

        finally:
            if cursor:
                cursor.close()

    def get_violations(
        self,
        limit: int = 100,
        agent_name: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Fetch latest violations from the database.

        Args:
            limit: Maximum number of rows to return.
            agent_name: Optional filter by agent name.

        Returns:
            List of violations.
        """
        if not self._ensure_connection():
            print("[DB] Cannot retrieve violations because no DB connection is available.")
            return []

        cursor = None

        try:
            cursor = self.connection.cursor(dictionary=True)

            safe_limit = max(1, min(int(limit), 1000))

            if agent_name:
                query = """
                    SELECT *
                    FROM violations
                    WHERE agent_name = %s
                    ORDER BY detected_at DESC, id DESC
                    LIMIT %s
                """
                cursor.execute(query, (agent_name, safe_limit))
            else:
                query = """
                    SELECT *
                    FROM violations
                    ORDER BY detected_at DESC, id DESC
                    LIMIT %s
                """
                cursor.execute(query, (safe_limit,))

            rows = cursor.fetchall()

            for row in rows:
                if row.get("detected_at") is not None:
                    row["detected_at"] = row["detected_at"].isoformat()

            return rows

        except Error as exc:
            print(f"[DB] Retrieval error: {exc}")
            return []

        finally:
            if cursor:
                cursor.close()

    def close(self) -> None:
        """Close the MySQL database connection."""
        if self.connection:
            try:
                self.connection.close()
                print("[DB] Connection closed.")
            except Error as exc:
                print(f"[DB] Error while closing connection: {exc}")
            finally:
                self.connection = None