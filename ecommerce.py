
from langchain_openai import ChatOpenAI
from browser_use import Agent, Controller

import asyncio
from pydantic import BaseModel

from llm import get_agent

# Define the output format as a Pydantic model
class Output(BaseModel):
	is_ecommerce: bool
	reason: str



async def main(website_link) -> Output:
    agent = get_agent(
        task="Check if the website is a ecommerce website. Website link is " + website_link,
        output_model=Output
    )
    
    history = await agent.run()
    
    return Output.model_validate_json(history.final_result())

if __name__ == "__main__":
    print(asyncio.run(main("https://www.amazon.com")).is_ecommerce)
