import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_whatsapp_hover():

    async with async_playwright() as p:

        browser = await p.chromium.launch_persistent_context("whatsapp-profile",headless=False)

        page = await browser.new_page()
        await page.goto("https://web.whatsapp.com/")


        deep_chat = page.get_by_text("Deep",exact=True).first
        await expect(deep_chat).to_be_visible(timeout=30000)
        print("Deep chat found")

        # Open Deep chat
        await deep_chat.click()
        print("Deep chat opened")

   
        # Calls
        calls = page.get_by_role("button",name="Calls")
        await expect(calls).to_be_visible()
        await calls.hover()
        print("Calls hovered")

    
        # Communities
        communities = page.get_by_role("button",name="Communities")
        await expect(communities).to_be_visible()
        await communities.hover()
        print("Communities hovered")


        # Meta AI
        meta_ai = page.get_by_role("button",name="Meta AI")
        await expect(meta_ai).to_be_visible()
        await meta_ai.hover()
        print("Meta AI hovered")

    
        # Menu inside Deep chat
        menu = page.get_by_test_id("conversation-header").get_by_role("button",name="Menu")
        await expect(menu).to_be_visible()
        await menu.hover()
        print("Chat Menu hovered")

    
        # Sticker
        sticker = page.get_by_role("button",name="Emojis, GIFs, Stickers")
        await expect(sticker).to_be_visible(timeout=10000)
        await sticker.hover()
        print("Sticker hovered")

   
        # Attach
        attach = page.get_by_role("button",name="Attach")
        await expect(attach).to_be_visible()
        await attach.hover()
        print("Attach hovered")

        # New Chat (+)
        new_chat = page.get_by_role("button",name="New chat")
        await expect(new_chat).to_be_visible()
        await new_chat.hover()
        print("New Chat (+) hovered")

        # Message box
        message_box = page.get_by_role("textbox",name="Type a message")
        await expect(message_box).to_be_visible()
        await message_box.hover()
        print("Message box hovered")
        await browser.close()