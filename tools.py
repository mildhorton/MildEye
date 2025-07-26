from crewai_tools import tool
# We can also add our Serper search tool definition here for organization
from crewai_tools import SerperDevTool

search_tool = SerperDevTool()

# Our new tool for generating affiliate links
@tool("Affiliate Link Generator Tool")
def AffiliateLinkTool(product_name: str) -> str:
    """
    Use this tool to generate an affiliate marketing link for a given product.
    The input should be the name of the product.
    """
    # In a real app, this would call an affiliate API.
    # For now, we'll simulate it with a simple Amazon search link.
    # Replace 'your-affiliate-tag-20' with your actual Amazon Associates tag.
    formatted_query = "+".join(product_name.split())
    affiliate_link = f"https://www.amazon.com/s?k={formatted_query}&tag=your-affiliate-tag-20"
    return affiliate_link