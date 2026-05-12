# Olist ERP MCP

MCP server for interacting with a simulated ERP backend built from the Olist Brazilian E-Commerce dataset in Supabase.

This repo is the MCP/integration layer. It depends on a separate Supabase-backed setup repo:

- `olist-erp-demo` — data cleaning scripts, Supabase SQL views, and setup documentation
- `olist-erp-mcp` — MCP server exposing ERP business tools to agents and MCP clients

## Architecture

```text
Olist Kaggle CSVs
    ↓
Supabase Postgres tables and ERP views
    ↓
Olist ERP MCP server
    ↓
MCP clients / LangChain agents / ChatGPT-compatible MCP clients