import os
from langchain_openai import ChatOpenAI
from browser_use import ActionResult, Agent, Browser, BrowserContextConfig, Controller
from browser_use.browser.context import BrowserContext
from urllib.parse import urlparse, parse_qs
import asyncio
from pydantic import BaseModel, Field

from llm import get_agent

# Define the output format as a Pydantic model
class Output(BaseModel):
    has_traffic_loss: bool = Field(description="Whether the website has lost traffic in the last 2 years")
    traffic_last_2_year: str = Field(description="Traffic of the website 2 years ago")
    traffic_last_year: str = Field(description="Traffic of the website 1 year ago")
    traffic_now: str = Field(description="Traffic of the website now")

controller = Controller(output_model=Output)

@controller.action('Scoll to MONTHLY ORGANIC TRAFFIC')
async def scroll_page_to_traffic(url: str, browser: Browser):
    page = await browser.get_current_page()
    await page.evaluate("document.querySelector('div.scrollarea').scrollBy(0,600)")
    return ActionResult(extracted_content='Website opened')

@controller.action('Take screenshot of the chart')
async def take_screenshot(url: str, browser: Browser):
    page = await browser.get_current_page()
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    website = query_params.get('domain', [None])[0]
    domain = website.split("//")[1]
    await page.screenshot(path=f"./screenshots/{domain}.png")  
    return ActionResult(extracted_content='Screenshot taken')

async def main(website_link) -> Output:
    task = f"""
    You will follow the steps to know the real traffic of the website. You need to use uber suggest website to get the real traffic of the website.

    Steps:
    1. go to https://app.neilpatel.com/en/login, If redirected to dashboard, then go to https://app.neilpatel.com/en/traffic_analyzer/overview
    2. Otherwise Sign in using the following credentials: In Username and EMail use {os.getenv("UBER_SUGGEST_USERNAME")} and in Password use {os.getenv("UBER_SUGGEST_PASSWORD")}
    4. After Sign in Go to Neil Patel uber suggest website - https://app.neilpatel.com/en/traffic_analyzer/overview
    5. Enter the website link - {website_link} in the Domain field
    6. Click on the search button and wait for 2 seconds to load result.
    7. Scroll to MONTHLY ORGANIC TRAFFIC.
    8. Take screenshot of the chart and save to ./screenshots/<website_link>.png
    8. Analyze the chart and find out how much website has lost traffic in the 3 months, 6 months, and last year in MONTHLY ORGANIC TRAFFIC Chart
    """

    agent = get_agent(task, Output, controller)
    
    history = await agent.run()
    
    return Output.model_validate_json(history.final_result())

if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()
    print(asyncio.run(main("https://www.amazon.com")))
