import asyncio
import aiohttp
import time
import uuid
import cloudscraper
from loguru import logger


def show_warning():
    confirm = input("By using this tool means you understand the risks. do it at your own risk! \nPress Enter to continue or Ctrl+C to cancel... ")

    if confirm.strip() == "":
        print("Continuing...")
    else:
        print("Exiting...")
        exit()


# Constants
PING_INTERVAL = 60
RETRIES = 3

DOMAIN_API = {
    "SESSION": "https://api.nodepay.org/api/auth/session",
    "PING": "https://nw.nodepay.org/api/network/ping"
}

CONNECTION_STATES = {
    "CONNECTED": 1,
    "DISCONNECTED": 2,
    "NONE_CONNECTION": 3
}

status_connect = CONNECTION_STATES["NONE_CONNECTION"]
browser_id = None
account_info = {}
last_ping_time = {}


def uuidv4():
    return str(uuid.uuid4())


def valid_resp(resp):
    if not resp or "code" not in resp or resp["code"] < 0:
        raise ValueError("Invalid response")
    return resp


async def render_profile_info(proxy, token):
    global browser_id, account_info

    try:
        np_session_info = load_session_info(proxy)

        if not np_session_info:
            browser_id = uuidv4()
            response = await call_api(DOMAIN_API["SESSION"], {}, proxy, token)
            valid_resp(response)
            account_info = response["data"]
            if account_info.get("uid"):
                save_session_info(proxy, account_info)
                await start_ping(proxy, token)
            else:
                handle_logout(proxy)
        else:
            account_info = np_session_info
            await start_ping(proxy, token)
    except Exception as e:
        logger.error(f"Error in render_profile_info for proxy {proxy}: {e}")
        handle_logout(proxy)


async def call_api(url, data, proxy, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User -Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://app.nodepay.ai",
    }

    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.post(url, json=data, headers=headers, proxies={
                                "http": proxy, "https": proxy}, timeout=30)

        response.raise_for_status()
        return valid_resp(response.json())
    except Exception as e:
        logger.error(f"Error during API call: {e}")
        raise ValueError(f"Failed API call to {url}")


async def start_ping(proxy, token):
    while True:
        await ping(proxy, token)
        await asyncio.sleep(PING_INTERVAL)


async def ping(proxy, token):
    global last_ping_time, RETRIES, status_connect

    current_time = time.time()

    if proxy in last_ping_time and (current_time - last_ping_time[proxy]) < PING_INTERVAL:
        logger.info(f"Skipping ping for proxy {proxy}, not enough time elapsed")
        return

    last_ping_time[proxy] = current_time

    try:
        data = {
            "id": account_info.get("uid"),
            "browser_id": browser_id,
            "timestamp": int(time.time())
        }

        response = await call_api(DOMAIN_API["PING"], data, proxy, token)
        if response["code"] == 0:
            logger.info(f"Ping successful via proxy {proxy}: {response}")
            global RETRIES
            RETRIES = 0
            status_connect = CONNECTION_STATES["CONNECTED"]
        else:
            handle_ping_fail(proxy, response)
    except Exception as e:
        logger.error(f"Ping failed via proxy {proxy}: {e}")
        handle_ping_fail(proxy, None)


def handle_ping_fail(proxy, response):
    global RETRIES, status_connect
    logger.warning(f"Ping failed for proxy {proxy}. Response: {response}")
    RETRIES += 1  # Increment the retry count
    if RETRIES >= 3:  # Example threshold for retries
        logger.error(f"Max retries exceeded for proxy {proxy}. Logging out.")
        handle_logout(proxy)


def handle_logout(proxy):
    logger.info(f"Logged out and cleared session info for proxy {proxy}")
    # Clear session info or perform necessary cleanup here


def load_session_info(proxy):
    # Placeholder for loading session info logic
    return None  # Implement your loading logic here


def save_session_info(proxy, account_info):
    # Placeholder for saving session info logic
    pass  # Implement your saving logic here


def load_proxies(proxy_file):
    try:
        with open(proxy_file, 'r') as file:
            proxies = [line.strip() for line in file if line.strip()]
        return proxies
    except Exception as e:
        logger.error(f"Error reading proxy file: {e}")
        return []


async def main():
    # Get user input for token
    token = input("Nodepay token: ")

    # Load proxies from the specified file
    proxy_file_path = r"proxies.txt"
    proxies = load_proxies(proxy_file_path)

    if not proxies:
        logger.warning("No proxies loaded from the file. Running without proxy.")
        await render_profile_info(None, token)
    else:
        for proxy in proxies:
            logger.info(f"Using proxy: {proxy}")
            await render_profile_info(proxy, token)


if __name__ == '__main__':
    show_warning()
    print("\nAlright, we here! Insert your nodepay token that you got from the tutorial.")
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Program terminated by user.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    finally:
        logger.info("Exiting the program. Please ensure all resources are cleaned up.")
