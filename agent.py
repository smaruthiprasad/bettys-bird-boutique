import os
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.cloud.sql.connector import Connector
import pymysql
from .datastore import datastore_search_tool
from .search_agent import search_agent_tool

# Short-term session memory
session_service = InMemorySessionService()

# Read agent instructions
script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
    instruction = f.read()

# Cloud SQL connector (no proxy needed)
connector = Connector()


def get_product_price(product_name: str) -> str:
    """
    Get the price of a product from Betty's Bird Boutique store database.

    Args:
        product_name (str): The name of the product to look up the price for
    """
    try:
        conn = connector.connect(
            "a4990292-u4862290-1777133828:us-central1:free-trial-first-project",
            "pymysql",
            user="root",
            password="Betty2024!",
            db="betty",
        )
        cursor = conn.cursor()
        search_term = f"%{product_name.lower()}%"
        cursor.execute(
            "SELECT product_name, price FROM products WHERE LOWER(product_name) LIKE %s",
            (search_term,)
        )
        rows = cursor.fetchall()
        conn.close()
        if not rows:
            return f"No product found matching '{product_name}'."
        results = [f"{row[0]}: ${row[1]}" for row in rows]
        return "Products found:\n" + "\n".join(results)
    except Exception as e:
        return f"Error looking up product price: {e}"


# Set up all three tools
tools = [
    get_product_price,
    datastore_search_tool,
    search_agent_tool,
]

# Create the root agent
root_agent = Agent(
    name="bettys_bird_boutique_agent",
    description="A customer service agent for Betty's Bird Boutique pet store.",
    instruction=instruction,
    model="gemini-2.5-flash",
    tools=tools,
)
