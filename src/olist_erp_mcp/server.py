from typing import Any

from mcp.server.fastmcp import FastMCP

from src.olist_erp_mcp.tools import (
    add_agent_note,
    create_agent_task,
    get_customer_account_summary,
    get_invoice,
    get_order,
    get_seller_performance,
    list_high_priority_support_cases,
    list_high_risk_sellers,
    list_invoice_exceptions,
    list_late_shipments,
)

mcp = FastMCP("olist-erp-mcp")


@mcp.tool()
def get_invoice_tool(invoice_id: str) -> dict[str, Any]:
    """
    Retrieve an ERP-style invoice by invoice ID.
    """
    return get_invoice(invoice_id)


@mcp.tool()
def get_order_tool(order_id: str) -> dict[str, Any]:
    """
    Retrieve an ERP-style order header by order ID.
    """
    return get_order(order_id)


@mcp.tool()
def get_customer_account_summary_tool(customer_unique_id: str) -> dict[str, Any]:
    """
    Retrieve customer account summary by customer_unique_id.
    """
    return get_customer_account_summary(customer_unique_id)


@mcp.tool()
def list_late_shipments_tool(
    min_delay_days: int = 3,
    limit: int = 20,
) -> list[dict[str, Any]]:
    """
    List late shipments with a minimum delivery delay.
    """
    return list_late_shipments(min_delay_days=min_delay_days, limit=limit)


@mcp.tool()
def list_high_priority_support_cases_tool(
    limit: int = 20,
) -> list[dict[str, Any]]:
    """
    List high-priority support cases based on low review scores.
    """
    return list_high_priority_support_cases(limit=limit)


@mcp.tool()
def get_seller_performance_tool(seller_id: str) -> dict[str, Any]:
    """
    Retrieve seller/vendor performance metrics by seller ID.
    """
    return get_seller_performance(seller_id)


@mcp.tool()
def list_high_risk_sellers_tool(limit: int = 20) -> list[dict[str, Any]]:
    """
    List high-risk sellers based on late delivery rate and review score.
    """
    return list_high_risk_sellers(limit=limit)


@mcp.tool()
def list_invoice_exceptions_tool(limit: int = 20) -> list[dict[str, Any]]:
    """
    List invoices with payment, delivery, or order-status exceptions.
    """
    return list_invoice_exceptions(limit=limit)


@mcp.tool()
def add_agent_note_tool(
    entity_type: str,
    entity_id: str,
    note: str,
) -> dict[str, Any]:
    """
    Add an operational note to a business record.

    entity_type examples: invoice, order, customer, seller, shipment, support_case.
    """
    return add_agent_note(
        entity_type=entity_type,
        entity_id=entity_id,
        note=note,
    )


@mcp.tool()
def create_agent_task_tool(
    task_type: str,
    entity_type: str,
    entity_id: str,
    description: str,
    priority: str = "medium",
) -> dict[str, Any]:
    """
    Create an operational follow-up task for a business record.

    task_type examples: finance_review, support_follow_up, seller_review,
    fulfillment_review, executive_escalation.

    priority examples: low, medium, high.
    """
    return create_agent_task(
        task_type=task_type,
        entity_type=entity_type,
        entity_id=entity_id,
        description=description,
        priority=priority,
    )


if __name__ == "__main__":
    mcp.run()