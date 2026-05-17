from typing import Any

from .supabase_client import get_supabase_client

supabase = get_supabase_client()


def get_invoice(invoice_id: str) -> dict[str, Any]:
    response = (
        supabase
        .table("erp_invoices")
        .select("*")
        .eq("invoice_id", invoice_id)
        .single()
        .execute()
    )
    return response.data


def get_order(order_id: str) -> dict[str, Any]:
    response = (
        supabase
        .table("erp_orders")
        .select("*")
        .eq("order_id", order_id)
        .single()
        .execute()
    )
    return response.data


def get_customer_account_summary(customer_unique_id: str) -> dict[str, Any]:
    response = (
        supabase
        .table("erp_customer_account_summary")
        .select("*")
        .eq("customer_unique_id", customer_unique_id)
        .single()
        .execute()
    )
    return response.data


def list_late_shipments(min_delay_days: int = 3, limit: int = 20) -> list[dict[str, Any]]:
    response = (
        supabase
        .table("erp_shipments")
        .select("*")
        .eq("delivery_status", "late")
        .gte("delivery_delay_days", min_delay_days)
        .limit(limit)
        .execute()
    )
    return response.data


def list_high_priority_support_cases(limit: int = 20) -> list[dict[str, Any]]:
    response = (
        supabase
        .table("erp_support_cases")
        .select("*")
        .eq("priority", "high")
        .limit(limit)
        .execute()
    )
    return response.data


def get_seller_performance(seller_id: str) -> dict[str, Any]:
    response = (
        supabase
        .table("erp_seller_performance")
        .select("*")
        .eq("seller_id", seller_id)
        .single()
        .execute()
    )
    return response.data


def list_high_risk_sellers(limit: int = 20) -> list[dict[str, Any]]:
    response = (
        supabase
        .table("erp_seller_risk_summary")
        .select("*")
        .eq("seller_risk_level", "high")
        .order("late_line_rate", desc=True)
        .limit(limit)
        .execute()
    )
    return response.data


def list_invoice_exceptions(limit: int = 20) -> list[dict[str, Any]]:
    response = (
        supabase
        .table("erp_invoice_exceptions")
        .select("*")
        .eq("has_exception", True)
        .limit(limit)
        .execute()
    )
    return response.data


def add_agent_note(entity_type: str, entity_id: str, note: str) -> dict[str, Any]:
    response = (
        supabase
        .table("agent_notes")
        .insert({
            "entity_type": entity_type,
            "entity_id": entity_id,
            "note": note,
        })
        .execute()
    )
    return response.data[0]


def create_agent_task(
    task_type: str,
    entity_type: str,
    entity_id: str,
    description: str,
    priority: str = "medium",
) -> dict[str, Any]:
    response = (
        supabase
        .table("agent_tasks")
        .insert({
            "task_type": task_type,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "description": description,
            "priority": priority,
            "status": "open",
        })
        .execute()
    )
    return response.data[0]

def list_open_tasks_for_entity(
    entity_type: str,
    entity_id: str,
    limit: int = 20,
) -> list[dict[str, Any]]:
    """
    List open agent tasks for a specific business entity.

    This is used for duplicate prevention. Before the agent creates a
    new task for an order, invoice, support case, or seller, it can check
    whether an open task already exists.
    """
    response = (
        supabase
        .table("agent_tasks")
        .select("*")
        .eq("entity_type", entity_type)
        .eq("entity_id", entity_id)
        .eq("status", "open")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return response.data


def list_notes_for_entity(
    entity_type: str,
    entity_id: str,
    limit: int = 20,
) -> list[dict[str, Any]]:
    """
    List recent notes for a specific business entity.

    This gives the agent historical context about prior reviews,
    escalations, or actions taken on the same record.
    """
    response = (
        supabase
        .table("agent_notes")
        .select("*")
        .eq("entity_type", entity_type)
        .eq("entity_id", entity_id)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return response.data


def update_agent_task_status(
    task_id: int,
    status: str,
) -> dict[str, Any]:
    """
    Update the status of an existing agent task.

    Example statuses:
    - open
    - in_progress
    - closed
    - cancelled

    This lets future workflows manage task lifecycle instead of only
    creating new tasks.
    """
    response = (
        supabase
        .table("agent_tasks")
        .update({
            "status": status,
        })
        .eq("id", task_id)
        .execute()
    )

    if not response.data:
        return {
            "error": "No task found or updated",
            "task_id": task_id,
            "status": status,
        }

    return response.data[0]