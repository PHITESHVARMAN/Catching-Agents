-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 20, 2026 at 05:57 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `agent_governance`
--

-- --------------------------------------------------------

--
-- Table structure for table `violations`
--

CREATE TABLE `violations` (
  `id` int(11) NOT NULL,
  `agent_name` varchar(100) NOT NULL,
  `session_id` varchar(100) DEFAULT NULL,
  `tool_name` varchar(100) NOT NULL,
  `violation_type` varchar(50) NOT NULL,
  `severity` varchar(20) NOT NULL,
  `rule_matched` varchar(255) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `blocked` tinyint(1) NOT NULL DEFAULT 1,
  `tool_input` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`tool_input`)),
  `raw_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`raw_data`)),
  `detected_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `violations`
--

INSERT INTO `violations` (`id`, `agent_name`, `session_id`, `tool_name`, `violation_type`, `severity`, `rule_matched`, `description`, `blocked`, `tool_input`, `raw_data`, `detected_at`) VALUES
(1, 'support_agent', 'manual_test_001', 'access_customer_db', 'policy_breach', 'high', 'approved_tools', 'Manual DB test: unapproved customer DB tool.', 1, '{\"customer_id\": \"4521\"}', '{\"test\": true}', '2026-08-20 12:08:27'),
(2, 'support_agent', 'manual_test_001', 'access_customer_db', 'policy_breach', 'high', 'approved_tools', 'Manual DB test: unapproved customer DB tool.', 1, '{\"customer_id\": \"4521\"}', '{\"test\": true}', '2026-08-20 12:40:04'),
(3, 'support_agent', 'manual_test_001', 'access_customer_db', 'policy_breach', 'high', 'approved_tools', 'Manual DB test: unapproved customer DB tool.', 1, '{\"customer_id\": \"4521\"}', '{\"test\": true}', '2026-08-20 12:40:14'),
(4, 'support_agent', '20260820181246', 'access_customer_db', 'policy_breach', 'high', NULL, 'Tool \'access_customer_db\' is not approved', 1, '{\"customer_id\": \"4521\"}', NULL, '2026-08-20 12:42:46');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `violations`
--
ALTER TABLE `violations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_violations_agent_name` (`agent_name`),
  ADD KEY `idx_violations_tool_name` (`tool_name`),
  ADD KEY `idx_violations_severity` (`severity`),
  ADD KEY `idx_violations_detected_at` (`detected_at`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `violations`
--
ALTER TABLE `violations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
