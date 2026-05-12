from src.olist_erp_mcp.tools import (
    add_agent_note,
    list_high_priority_support_cases,
    list_late_shipments,
)

print("Late shipments:")
print(list_late_shipments(min_delay_days=5, limit=3))

print("\nHigh-priority support cases:")
print(list_high_priority_support_cases(limit=3))

print("\nWriting test note:")
print(
    add_agent_note(
        entity_type="system",
        entity_id="mcp-test",
        note="Test note written from olist-erp-mcp tool layer.",
    )
)