-- 004 — read-only `analyst` role for Supabase MCP analysis sessions.
-- apply_migrations.py replaces __ANALYST_PASSWORD__ from .env at apply time.
-- Analysis connects with THIS role, never the service key: SELECT everywhere,
-- write nowhere (only ETL/tagging scripts write, via ANALYTICS_DB_URL).

do $$
begin
  if not exists (select from pg_roles where rolname = 'analyst') then
    create role analyst login password '__ANALYST_PASSWORD__';
  end if;
end $$;

grant usage on schema raw, tags, metrics, etl to analyst;
grant select on all tables in schema raw, tags, metrics, etl to analyst;

alter default privileges in schema raw     grant select on tables to analyst;
alter default privileges in schema tags    grant select on tables to analyst;
alter default privileges in schema metrics grant select on tables to analyst;
alter default privileges in schema etl     grant select on tables to analyst;

-- Belt and braces: no write path even if a grant slips in later.
alter role analyst set default_transaction_read_only = on;
