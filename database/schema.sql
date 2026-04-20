-- Student Performance Analyzer Database Schema (SQLite)
-- This schema creates all necessary tables for the application

-- Users table: stores authentication information
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Profiles table: stores student profile information
CREATE TABLE IF NOT EXISTS profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    age INTEGER,
    gender TEXT,
    course TEXT,
    semester TEXT,
    college TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Performance records table: stores subject marks and study data
CREATE TABLE IF NOT EXISTS performance_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    subject_marks TEXT NOT NULL,  -- JSON format: {"Math": 85, "Science": 90, ...}
    attendance REAL NOT NULL,
    study_hours REAL NOT NULL,
    backlogs INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Analysis history table: stores performance analysis results
CREATE TABLE IF NOT EXISTS analysis_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    performance_score REAL NOT NULL,
    category TEXT NOT NULL,
    explanation TEXT NOT NULL,
    suggestions TEXT NOT NULL,  -- JSON format: ["suggestion1", "suggestion2", ...]
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_profiles_user_id ON profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_performance_user_id ON performance_records(user_id);
CREATE INDEX IF NOT EXISTS idx_analysis_user_id ON analysis_history(user_id);
