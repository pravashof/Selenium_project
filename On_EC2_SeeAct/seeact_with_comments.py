
# -*- coding: utf-8 -*-
# Copyright (c) 2024 OSU Natural Language Processing Group
#
# Licensed under the OpenRAIL-S License;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.licenses.ai/ai-pubs-open-rails-vz1
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This script leverages the GPT-4V API and Playwright to create a web agent capable of autonomously performing tasks on webpages.
It utilizes Playwright to create a browser instance and retrieve interactive elements, then applies the SeeAct Framework 
(https://osu-nlp-group.github.io/SeeAct/) to generate and ground the next operation.
The script is designed to automate complex web interactions, enhancing accessibility and efficiency in web navigation tasks.
"""

import argparse
import asyncio
import datetime
import json
import logging
import os
import warnings
from dataclasses import dataclass

import toml
import torch
from aioconsole import ainput, aprint
from playwright.async_api import async_playwright

# Import custom utilities for various tasks
from data_utils.format_prompt_utils import get_index_from_option_name
from data_utils.prompts import generate_prompt, format_options
from demo_utils.browser_helper import (
    normal_launch_async, 
    normal_new_context_async,
    get_interactive_elements_with_playwright, 
    select_option, 
    saveconfig
)
from demo_utils.format_prompt import format_choices, format_ranking_input, postprocess_action_lmm
from demo_utils.inference_engine import OpenaiEngine
from demo_utils.ranking_model import CrossEncoder, find_topk
from demo_utils.website_dict import website_dict

# Suppress HuggingFace and tokenizer warnings for cleaner output
os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore", category=UserWarning)

@dataclass
class SessionControl:
    """A class to manage session states and active components."""
    pages = []  # Tracks open browser pages
    cdp_sessions = []  # Tracks Chrome DevTools Protocol sessions for debugging
    active_page = None  # Currently active browser page
    active_cdp_session = None  # Active debugging session
    context = None  # The browser context
    browser = None  # Browser instance

# Initialize a global session control instance
session_control = SessionControl()

async def page_on_close_handler(page):
    """Handles the event when a browser page is closed."""
    try:
        await session_control.active_page.title()
    except Exception:
        if session_control.context and session_control.context.pages:
            # Switch to the last available page
            session_control.active_page = session_control.context.pages[-1]
            await session_control.active_page.bring_to_front()
        else:
            # If no pages are available, open a new default page
            await session_control.context.new_page()
            await session_control.active_page.goto("https://www.google.com/", wait_until="load")

async def page_on_navigation_handler(frame):
    """Updates the active page when a navigation event occurs."""
    session_control.active_page = frame.page

async def page_on_crash_handler(page):
    """Handles the event when a page crashes by attempting to reload it."""
    await aprint("Page crashed:", page.url)
    await page.reload()

async def page_on_open_handler(page):
    """Handles the event when a new page is opened."""
    page.on("framenavigated", page_on_navigation_handler)
    page.on("close", page_on_close_handler)
    page.on("crash", page_on_crash_handler)
    session_control.active_page = page

async def main(config, base_dir) -> None:
    """The main function to manage browser automation tasks."""

    # Load basic settings from the configuration file
    is_demo = config["basic"]["is_demo"]
    save_file_dir = os.path.abspath(config["basic"]["save_file_dir"])
    default_task = config["basic"]["default_task"]
    default_website = config["basic"]["default_website"]

    # Initialize the OpenAI engine for GPT-4V-based inference
    openai_config = config["openai"]
    if openai_config["api_key"] == "Your API Key Here":
        raise Exception("Please set your GPT API key in the configuration file.")
    generation_model = OpenaiEngine(**openai_config)

    # Launch Playwright and set up the browser context
    async with async_playwright() as playwright:
        session_control.browser = await normal_launch_async(playwright)
        session_control.context = await normal_new_context_async(
            session_control.browser,
            tracing=config["playwright"]["tracing"],
            storage_state=config.get("basic", {}).get("storage_state"),
            video_path=save_file_dir if config["playwright"]["save_video"] else None,
            viewport=config["playwright"]["viewport"],
        )
        session_control.context.on("page", page_on_open_handler)

        # Open a new browser tab and navigate to the default website
        await session_control.context.new_page()
        await session_control.active_page.goto(default_website, wait_until="load")

        # Example task loop for performing actions on a webpage
        elements = await get_interactive_elements_with_playwright(session_control.active_page)
        for element in elements:
            # Perform actions as determined by the GPT-4V engine
            pass  # Placeholder for interaction logic

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config_path", help="Path to the TOML configuration file.", type=str, default="config/demo_mode.toml")
    args = parser.parse_args()

    # Load configuration from the TOML file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, args.config_path), "r") as toml_file:
        config = toml.load(toml_file)

    # Run the main function
    asyncio.run(main(config, base_dir))
