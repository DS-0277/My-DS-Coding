"""Initial FastMCP server exposing the assignment tools."""

from mcp.server.fastmcp import FastMCP

from server.tools.math_tool import calculate_expression
from server.tools.sql_tool import query_database
from server.tools.weather_tool import get_current_weather


mcp = FastMCP("enterprise-operations-tools")


@mcp.tool()
def query_database_tool(sql_query: str) -> str:
    """Query enterprise operations data using one read-only SELECT statement.

    Database schema: customers(customer_id, name, city, state); products(product_id,
    sku, name, unit_price); orders(order_id, customer_id, order_date, status,
    total_value); order_items(order_id, product_id, quantity); and
    inventory(inventory_id, product_id, city, quantity, reorder_level).
    To search inventory by SKU, join inventory to products on product_id because
    inventory stores product_id, not sku.
    """
    return query_database(sql_query)


@mcp.tool()
async def get_current_weather_tool(city: str) -> str:
    """Get current weather conditions for a city."""
    return await get_current_weather(city)


@mcp.tool()
def calculate_expression_tool(expression: str) -> str:
    """Calculate a mathematical expression."""
    return calculate_expression(expression)


if __name__ == "__main__":
    mcp.run(transport="stdio")
