-- AutoLearn v15 Supabase schema
-- Run this in Supabase SQL Editor, then set Streamlit secrets.
create table if not exists users (
  id text primary key,
  email text unique not null,
  display_name text not null,
  password_hash text not null,
  created_at text not null
);

create table if not exists profiles (
  user_id text primary key references users(id) on delete cascade,
  data jsonb not null default '{}'::jsonb,
  updated_at text not null
);

create table if not exists medications (
  id text primary key,
  user_id text not null references users(id) on delete cascade,
  name text not null,
  dose text not null,
  times jsonb not null default '[]'::jsonb,
  days jsonb not null default '["Tất cả"]'::jsonb,
  instructions text,
  inventory numeric default 0,
  units_per_dose numeric default 1,
  refill_threshold numeric default 5,
  active boolean default true,
  created_at text not null
);

create table if not exists dose_logs (
  id text primary key,
  user_id text not null references users(id) on delete cascade,
  medication_id text,
  scheduled_at text not null,
  status text not null,
  note text,
  created_at text not null
);

create table if not exists health_logs (
  id text primary key,
  user_id text not null references users(id) on delete cascade,
  data jsonb not null default '{}'::jsonb,
  created_at text not null
);

create table if not exists reminder_sent (
  id text primary key,
  user_id text not null references users(id) on delete cascade,
  medication_id text not null,
  reminder_key text not null,
  channel text not null,
  sent_at text not null,
  unique(user_id, medication_id, reminder_key, channel)
);
