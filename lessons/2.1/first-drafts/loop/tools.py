"""Harborline's backend as tools that Claude can ask to call."""

import json

from harborline import backend, policy
from harborline.errors import BackendError

GET_CUSTOMER = {
    "name": "get_customer",
    "description": "Find a Harborline customer by email address. "
                   "Use it to check who is writing.",
    "input_schema": {
        "type": "object",
        "properties": {
            "email": {"type": "string",
                      "description": "The customer's email address"},
            "name": {"type": "string",
                     "description": "The customer's full name"},
        },
    },
}
LOOKUP_ORDER = {
    "name": "lookup_order",
    "description": "Look up one Harborline order: its status, items, "
                   "total and tracking.",
    "input_schema": {
        "type": "object",
        "properties": {
            "order_id": {"type": "string",
                         "description": "The order ID, as the customer "
                                        "wrote it"},
        },
        "required": ["order_id"],
    },
}
LIST_ORDERS = {
    "name": "list_orders",
    "description": "List a customer's orders.",
    "input_schema": {
        "type": "object",
        "properties": {
            "customer_id": {"type": "string",
                            "description": "The customer ID"},
        },
        "required": ["customer_id"],
    },
}
PROCESS_REFUND = {
    "name": "process_refund",
    "description": "Refund an order.",
    "input_schema": {
        "type": "object",
        "properties": {
            "order_id": {"type": "string",
                         "description": "The order ID"},
            "reason": {"type": "string", "enum": list(policy.REASONS),
                       "description": "Why the customer wants it"},
            "amount": {"type": "number",
                       "description": "The amount in US dollars"},
            "sku": {"type": "string",
                    "description": "The item's SKU, for item refunds"},
        },
        "required": ["order_id", "reason", "amount"],
    },
}
ESCALATE_TO_HUMAN = {
    "name": "escalate_to_human",
    "description": "Escalate the case to a human.",
    "input_schema": {
        "type": "object",
        "properties": {
            "customer_id": {"type": "string",
                            "description": "The customer ID"},
            "reason": {"type": "string",
                       "description": "Why a person is needed"},
            "summary": {"type": "string",
                        "description": "The case so far"},
        },
        "required": ["customer_id", "reason", "summary"],
    },
}
TOOLS = [GET_CUSTOMER, LOOKUP_ORDER, LIST_ORDERS, PROCESS_REFUND,
         ESCALATE_TO_HUMAN]

HANDLERS = {
    "get_customer": backend.get_customer,
    "lookup_order": backend.lookup_order,
    "list_orders": backend.list_orders,
    "process_refund": backend.process_refund,
    "escalate_to_human": backend.escalate_to_human,
}


def run_tool(call):
    """Run one tool_use block; return the tool_result block for it."""
    result = {"type": "tool_result", "tool_use_id": call.id}
    handler = HANDLERS.get(call.name)
    if handler is None:
        return result | {"content": f"Unknown tool {call.name}.",
                         "is_error": True}
    try:
        output = handler(**call.input)
    except BackendError as error:  # not found, bad input, ...
        return result | {"content": str(error), "is_error": True}
    return result | {"content": json.dumps(output)}
