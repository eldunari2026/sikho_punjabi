-- Run this in the Supabase SQL Editor (Dashboard → SQL Editor → New query)
-- Creates the feedback table and enables Row Level Security

CREATE TABLE IF NOT EXISTS feedback (
  id            bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  reviewer_token text   NOT NULL,
  reviewer_name  text   NOT NULL,
  item_id        text   NOT NULL,
  action         text   NOT NULL DEFAULT '',
  comment        text   NOT NULL DEFAULT '',
  updated_at     timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT feedback_reviewer_item UNIQUE (reviewer_token, item_id)
);

-- Index for fast per-reviewer queries
CREATE INDEX IF NOT EXISTS feedback_reviewer_token_idx ON feedback (reviewer_token);

-- Enable Row Level Security
ALTER TABLE feedback ENABLE ROW LEVEL SECURITY;

-- Allow anyone with the anon key to read, insert, and update
-- (Blindness between reviewers is enforced in the frontend, not the DB)
CREATE POLICY "anon read"   ON feedback FOR SELECT USING (true);
CREATE POLICY "anon insert" ON feedback FOR INSERT WITH CHECK (true);
CREATE POLICY "anon update" ON feedback FOR UPDATE USING (true);
