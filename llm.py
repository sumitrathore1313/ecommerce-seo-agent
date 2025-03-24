from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserContextConfig, Controller
from browser_use.browser.context import BrowserContext

config = BrowserContextConfig(
    cookies_file="cookies.json",
    # wait_for_network_idle_page_load_time=3.0,
    # browser_window_size={'width': 1280, 'height': 1100},
    # locale='en-US',
    # user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    # highlight_elements=True,
    # viewport_expansion=500,
    # allowed_domains=['google.com', 'wikipedia.org'],
)

browser = Browser()
context = BrowserContext(browser=browser, config=config)
    
    
def get_agent(task, output_model, controller=None):
    llm = ChatOpenAI(model="gpt-4o-mini")
    
    if controller is None:
        controller = Controller(output_model=output_model)
    
    return Agent(
        task=task,
        llm=llm,
        controller=controller,
        browser=browser,
        browser_context=context
    )