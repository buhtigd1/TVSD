from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
import random
import time
import json


user_agents = [
    #add your list of user agents here
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/126.0.6478.35 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.165 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14.5; rv:127.0) Gecko/20100101 Firefox/127.0',
    'Mozilla/5.0 (X11; Linux i686; rv:127.0) Gecko/20100101 Firefox/127.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/127.0 Mobile/15E148 Safari/605.1.15',
    'Mozilla/5.0 (Android 14; Mobile; rv:127.0) Gecko/126.0 Firefox/126.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0',

]


# Dictionary mapping channel IDs to channel names
channel_logos = {
    "A&E": "https://cdn.tvpassport.com/image/station/960x540/v2/s10036_h15_aa.png",
    "ACC Network": "https://cdn.tvpassport.com/image/station/240x135/v2/s111905_h15_ac.png",
    "AMC": "https://cdn.tvpassport.com/image/station/240x135/v2/s52247_h15_aa.png",
    "American Heroes Channel": "https://cdn.tvpassport.com/image/station/240x135/v2/s18284_h15_aa.png",
    "Animal Planet": "https://cdn.tvpassport.com/image/station/240x135/v2/s16331_h9_ad.png",
    "BBC America": "https://cdn.tvpassport.com/image/station/240x135/v2/s18332_h15_aa.png",
    "BBC World News HD": "https://cdn.tvpassport.com/image/station/240x135/v2/s89542_h15_ab.png",
    "BET": "https://cdn.tvpassport.com/image/station/240x135/v2/s10051_h15_ad.png",
    "BET Her": "https://cdn.tvpassport.com/image/station/240x135/v2/s14897_h15_ac.png",
    "Big Ten Network": "https://cdn.tvpassport.com/image/station/240x135/v2/s56783_h15_ab.png",
    "Bloomberg TV": "https://cdn.tvpassport.com/image/station/240x135/v2/s71799_h15_ab.png",
    "Boomerang": "https://cdn.tvpassport.com/image/station/240x135/v2/s21883_h15_ab.png",
    "Bravo": "https://cdn.tvpassport.com/image/station/240x135/v2/s10057_h15_ab.png",
    "Cartoon Network": "https://cdn.tvpassport.com/image/station/240x135/v2/s60048_h15_ac.png",
    "CBS Sports Network": "https://cdn.tvpassport.com/image/station/240x135/v2/s16365_h15_ae.png",
    "Cinemax": "https://cdn.tvpassport.com/image/station/240x135/v2/s10120_h15_ab.png",
    "CNBC": "https://cdn.tvpassport.com/image/station/240x135/v2/s10139_h15_ad.png",
    "CMT": "https://cdn.tvpassport.com/image/station/240x135/v2/s15072_h15_aa.png",
    "CNN": "https://cdn.tvpassport.com/image/station/240x135/v2/s10142_h15_aa.png",
    "Comedy Central": "https://cdn.tvpassport.com/image/station/240x135/v2/s10149_h15_ab.png",
    "Cooking Channel": "https://cdn.tvpassport.com/image/station/240x135/v2/s30156_h15_aa.png",
    "Crime & Investigation HD": "https://cdn.tvpassport.com/image/station/240x135/v2/s61469_h15_ab.png",
    "CSPAN": "https://cdn.tvpassport.com/image/station/240x135/v2/s10161_h15_ad.png",
    "CSPAN 2": "https://cdn.tvpassport.com/image/station/240x135/v2/s10162_h15_ac.png",
    "Destination America": "https://cdn.tvpassport.com/image/station/240x135/v2/s16617_h15_aa.png",
    "Discovery": "https://cdn.tvpassport.com/image/station/240x135/v2/s11150_h15_af.png",
    "Discovery Family Channel": "https://cdn.tvpassport.com/image/station/240x135/v2/s16618_h15_aa.png",
    "Discovery Life": "https://cdn.tvpassport.com/image/station/240x135/v2/s16125_h15_ac.png",
    "Disney Channel (East)": "https://cdn.tvpassport.com/image/station/240x135/v2/s10171_h15_ae.png",
    "Disney Junior": "https://cdn.tvpassport.com/image/station/240x135/v2/s74885_h15_ab.png",
    "Disney XD": "https://cdn.tvpassport.com/image/station/240x135/v2/s18279_h15_aa.png",
    "E!": "https://cdn.tvpassport.com/image/station/240x135/v2/s10989_h15_aa.png",
    "ESPN": "https://cdn.tvpassport.com/image/station/240x135/v2/s10179_h15_aa.png",
    "ESPN2": "https://cdn.tvpassport.com/image/station/240x135/v2/s12444_h15_ab.png",
    "ESPNews": "https://cdn.tvpassport.com/image/station/240x135/v2/s16485_h15_aa.png",
    "ESPNU": "https://cdn.tvpassport.com/image/station/240x135/v2/s45654_h15_aa.png",
    "Food Network": "https://cdn.tvpassport.com/image/station/240x135/v2/s12574_h15_ab.png",
    "Fox Business Network": "https://cdn.tvpassport.com/image/station/240x135/v2/s58649_h15_ac.png",
    "FOX News Channel": "https://cdn.tvpassport.com/image/station/240x135/v2/s16374_h15_ab.png",
    "FOX Sports 1": "https://cdn.tvpassport.com/image/station/240x135/v2/s82541_h15_ab.png",
    "FOX Sports 2": "https://cdn.tvpassport.com/image/station/240x135/v2/s33178_h15_ab.png",
    "Freeform": "https://cdn.tvpassport.com/image/station/240x135/v2/s10093_h15_ae.png",
    "Fuse HD": "https://cdn.tvpassport.com/image/station/240x135/v2/s59116_h15_ac.png",
    "FX": "https://cdn.tvpassport.com/image/station/240x135/v2/s58574_h15_aa.png",
    "FX Movie": "https://cdn.tvpassport.com/image/station/240x135/v2/s70253_h15_aa.png",
    "FXX": "https://cdn.tvpassport.com/image/station/240x135/v2/s17927_h15_aa.png",
    "FYI": "https://cdn.tvpassport.com/image/station/240x135/v2/s58988_h15_aa.png",
    "Golf Channel": "https://cdn.tvpassport.com/image/station/240x135/v2/s65384_h15_aa.png",
    "Hallmark": "https://cdn.tvpassport.com/image/station/240x135/v2/s66268_h15_ab.png",
    "Hallmark Drama HD": "https://cdn.tvpassport.com/image/station/240x135/v2/s105756_h15_ab.png",
    "Hallmark Movies & Mysteries HD": "https://cdn.tvpassport.com/image/station/240x135/v2/s61522_h15_ab.png",
    "HBO 2 East": "https://cdn.tvpassport.com/image/station/240x135/v2/s59368_h15_aa.png",
    "HBO Comedy HD": "https://cdn.tvpassport.com/image/station/240x135/v2/s18429_h15_aa.png",
    "HBO East": "https://cdn.tvpassport.com/image/station/240x135/v2/s10240_h15_aa.png",
    "HBO Family East": "https://cdn.tvpassport.com/image/station/240x135/v2/s16585_h15_aa.png",
    "HBO Signature": "https://cdn.tvpassport.com/image/station/240x135/v2/s59363_h15_aa.png",
    "HBO Zone HD": "https://cdn.tvpassport.com/image/station/240x135/v2/s59845_h15_aa.png",
    "HGTV": "https://cdn.tvpassport.com/image/station/240x135/v2/s14902_h15_ab.png",
    "History": "https://cdn.tvpassport.com/image/station/240x135/v2/s57708_h15_ad.png",
    "HLN": "https://cdn.tvpassport.com/image/station/240x135/v2/s10145_h15_ac.png",
    "IFC": "https://cdn.tvpassport.com/image/station/240x135/v2/s14873_h15_ac.png",
    "Investigation Discovery": "https://cdn.tvpassport.com/image/station/240x135/v2/s16615_h15_ad.png",
    "ION Television East HD": "https://cdn.tvpassport.com/image/station/240x135/v2/s18633_h15_ac.png",
    "Lifetime": "https://cdn.tvpassport.com/image/station/240x135/v2/s10918_h15_ac.png",
    "LMN": "https://cdn.tvpassport.com/image/station/240x135/v2/s55887_h15_ag.png",
    "Logo": "https://cdn.tvpassport.com/image/station/240x135/v2/s46762_h15_aa.png",
    "MeTV Toons": "https://cdn.tvpassport.com/image/station/240x135/v2/s159817_h15_aa.png",
    "MLB Network": "https://cdn.tvpassport.com/image/station/240x135/v2/s62079_h15_aa.png",
    "MoreMAX": "https://cdn.tvpassport.com/image/station/240x135/v2/s59373_h15_ad.png",
    "MotorTrend HD": "https://cdn.tvpassport.com/image/station/240x135/v2/s31046_h15_ab.png",
    "MovieMAX": "https://cdn.tvpassport.com/image/station/240x135/v2/s59963_h15_ab.png",
    "MSNBC": "https://cdn.tvpassport.com/image/station/240x135/v2/s16300_h15_ac.png",
    "MTV": "https://cdn.tvpassport.com/image/station/240x135/v2/s10986_h15_aa.png",
    "Nat Geo WILD": "https://cdn.tvpassport.com/image/station/240x135/v2/s66804_h15_ab.png",
    "National Geographic": "https://cdn.tvpassport.com/image/station/240x135/v2/s49438_h15_ab.png",
    "NBA TV": "https://cdn.tvpassport.com/image/station/240x135/v2/s32281_h15_ad.png",
    "Newsmax TV": "https://cdn.tvpassport.com/image/station/240x135/v2/s87925_h15_ac.png",
    "NFL Network": "https://cdn.tvpassport.com/image/station/240x135/v2/s34710_h15_aa.png",
    "NFL Red Zone": "https://cdn.tvpassport.com/image/station/240x135/v2/s65024_h9_aa.png",
    "NHL Network": "https://cdn.tvpassport.com/image/station/240x135/v2/s58570_h15_ab.png",
    "Nick Jr.": "https://cdn.tvpassport.com/image/station/240x135/v2/s82649_h15_ad.png",
    "Nickelodeon East": "https://cdn.tvpassport.com/image/station/240x135/v2/s11006_h15_ab.png",
    "Nicktoons": "https://cdn.tvpassport.com/image/station/240x135/v2/s82654_h15_ac.png",
    "Outdoor Channel": "https://cdn.tvpassport.com/image/station/240x135/v2/s14776_h15_ab.png",
    "OWN": "https://cdn.tvpassport.com/image/station/240x135/v2/s70387_h15_aa.png",
    "Oxygen True Crime": "https://cdn.tvpassport.com/image/station/240x135/v2/s21484_h15_ac.png",
    "PBS 13 (WNET) New York": "https://cdn.tvpassport.com/image/station/240x135/v2/s11039_h15_ab.png",
    "ReelzChannel": "https://cdn.tvpassport.com/image/station/240x135/v2/s52199_h9_ac.png",
    "Science": "https://cdn.tvpassport.com/image/station/240x135/v2/s57390_h15_ac.png",
    "SEC Network": "https://cdn.tvpassport.com/image/station/240x135/v2/s89535_h15_ab.png",
    "Showtime (E)": "https://cdn.tvpassport.com/image/station/240x135/v2/s11115_h15_aa.png",
    "SHOWTIME 2": "https://cdn.tvpassport.com/image/station/240x135/v2/s11116_h15_aa.png",
    "STARZ East": "https://cdn.tvpassport.com/image/station/240x135/v2/s12719_h15_ac.png",
    "SundanceTV HD": "https://cdn.tvpassport.com/image/station/240x135/v2/s71280_h15_aa.png",
    "SYFY": "https://cdn.tvpassport.com/image/station/240x135/v2/s11097_h15_ae.png",
    "TBS": "https://cdn.tvpassport.com/image/station/240x135/v2/s11867_h15_ac.png",
    "TCM": "https://cdn.tvpassport.com/image/station/240x135/v2/s48815_h15_ab.png",
    "TeenNick": "https://cdn.tvpassport.com/image/station/240x135/v2/s59036_h15_ac.png",
    "Telemundo East": "https://cdn.tvpassport.com/image/station/240x135/v2/s73245_h15_ac.png",
    "Tennis Channel": "https://cdn.tvpassport.com/image/station/240x135/v2/s33395_h15_ac.png",
    "The CW (WPIX New York)": "https://cdn.tvpassport.com/image/station/240x135/v2/s53098_h15_ac.png",
    "The Movie Channel East": "https://cdn.tvpassport.com/image/station/240x135/v2/s35329_h15_aa.png",
    "The Weather Channel": "https://cdn.tvpassport.com/image/station/240x135/v2/s11187_h15_aa.png",
    "TLC": "https://cdn.tvpassport.com/image/station/240x135/v2/s11158_h15_ad.png",
    "TNT": "https://cdn.tvpassport.com/image/station/240x135/v2/s11164_h15_ac.png",
    "Travel Channel": "https://cdn.tvpassport.com/image/station/240x135/v2/s11180_h15_ac.png",
    "truTV": "https://cdn.tvpassport.com/image/station/240x135/v2/s10153_h15_ad.png",
    "TV One HD": "https://cdn.tvpassport.com/image/station/240x135/v2/s61960_h15_ab.png",
    "Universal Kids": "https://cdn.tvpassport.com/image/station/240x135/v2/s70225_h15_ae.png",
    "Univision East": "https://cdn.tvpassport.com/image/station/240x135/v2/s11118_h15_ab.png",
    "USA Network": "https://cdn.tvpassport.com/image/station/240x135/v2/s11207_h15_af.png",
    "VH1": "https://cdn.tvpassport.com/image/station/240x135/v2/s11218_h15_ac.png",
    "VICE": "https://cdn.tvpassport.com/image/station/240x135/v2/s18822_h15_ac.png",
    "WABC (New York) ABC East": "https://cdn.tvpassport.com/image/station/240x135/v2/s10003_h15_ac.png",
    "WCBS (New York) CBS East": "https://cdn.tvpassport.com/image/station/240x135/v2/s10098_h15_ac.png",
    "WE tv": "https://cdn.tvpassport.com/image/station/240x135/v2/s59296_h15_aa.png",
    "WNBC (New York) NBC East": "https://cdn.tvpassport.com/image/station/240x135/v2/s10991_h15_ad.png",
    "WNYW (New York) FOX East": "https://cdn.tvpassport.com/image/station/240x135/v2/s10212_h15_ab.png"

    # Add more channel IDs and names as needed
}

# Define specific group-title overrides
group_overrides = {
    "A&E": "Entertainment",
    "ACC Network": "Sports",
    "AMC": "Movies",
    "American Heroes Channel": "Entertainment",
    "Animal Planet": "Documentary",
    "BBC America": "Entertainment",
    "BBC World News HD": "News",
    "BET": "Entertainment",
    "BET Her": "Entertainment",
    "Big Ten Network": "Sports",
    "Bloomberg TV": "News",
    "Boomerang": "Kids",
    "Bravo": "Entertainment",
    "Cartoon Network": "Kids",
    "CBS Sports Network": "Sports",
    "Cinemax": "Movies",
    "CNBC": "News",
    "CMT": "Entertainment",
    "CNN": "News",
    "Comedy Central": "Entertainment",
    "Cooking Channel": "Entertainment",
    "Crime & Investigation HD": "Documentary",
    "CSPAN": "News",
    "CSPAN 2": "News",
    "Destination America": "Documentary",
    "Discovery": "Documentary",
    "Discovery Family Channel": "Kids",
    "Discovery Life": "Documentary",
    "Disney Channel (East)": "Kids",
    "Disney Junior": "Kids",
    "Disney XD": "Kids",
    "E!": "Entertainment",
    "ESPN": "Sports",
    "ESPN2": "Sports",
    "ESPNews": "Sports",
    "ESPNU": "Sports",
    "Food Network": "Entertainment",
    "Fox Business Network": "News",
    "FOX News Channel": "News",
    "FOX Sports 1": "Sports",
    "FOX Sports 2": "Sports",
    "Freeform": "Entertainment",
    "Fuse HD": "Entertainment",
    "FX": "Entertainment",
    "FX Movie": "Movies",
    "FXX": "Movies",
    "FYI": "Entertainment",
    "Golf Channel": "Sports",
    "Hallmark": "Movies",
    "Hallmark Drama HD": "Movies",
    "Hallmark Movies & Mysteries HD": "Movies",
    "HBO 2 East": "Movies",
    "HBO Comedy HD": "Movies",
    "HBO East": "Movies",
    "HBO Family East": "Movies",
    "HBO Signature": "Movies",
    "HBO Zone HD": "Movies",
    "HGTV": "Entertainment",
    "History": "Documentary",
    "HLN": "News",
    "IFC": "Movies",
    "Investigation Discovery": "Documentary",
    "ION Television East HD": "Entertainment",
    "Lifetime": "Movies",
    "LMN": "Movies",
    "Logo": "Entertainment",
    "MeTV Toons": "Kids",
    "MLB Network": "Sports",
    "MoreMAX": "Movies",
    "MotorTrend HD": "Sports",
    "MovieMAX": "Movies",
    "MSNBC": "News",
    "MTV": "Music",
    "Nat Geo WILD": "Documentary",
    "National Geographic": "Documentary",
    "NBA TV": "Sports",
    "Newsmax TV": "News",
    "NFL Network": "Sports",
    "NFL Red Zone": "Sports",
    "NHL Network": "Sports",
    "Nick Jr.": "Kids",
    "Nickelodeon East": "Kids",
    "Nicktoons": "Kids",
    "Outdoor Channel": "Documentary",
    "OWN": "Entertainment",
    "Oxygen True Crime": "Entertainment",
    "PBS 13 (WNET) New York": "Entertainment",
    "ReelzChannel": "Entertainment",
    "Science": "Documentary",
    "SEC Network": "Sports",
    "Showtime (E)": "Movies",
    "SHOWTIME 2": "Movies",
    "STARZ East": "Movies",
    "SundanceTV HD": "Movies",
    "SYFY": "Entertainment",
    "TBS": "Entertainment",
    "TCM": "Movies",
    "TeenNick": "Kids",
    "Telemundo East": "Spanish",
    "Tennis Channel": "Sports",
    "The CW (WPIX New York)": "News",
    "The Movie Channel East": "Entertainment",
    "The Weather Channel": "News",
    "TLC": "Entertainment",
    "TNT": "Entertainment",
    "Travel Channel": "Documentary",
    "truTV": "Entertainment",
    "TV One HD": "Entertainment",
    "Universal Kids": "Kids",
    "Univision East": "Spanish",
    "USA Network": "Entertainment",
    "VH1": "Entertainment",
    "VICE": "Entertainment",
    "WABC (New York) ABC East": "News",
    "WCBS (New York) CBS East": "News",
    "WE tv": "Entertainment",
    "WNBC (New York) NBC East": "News",
    "WNYW (New York) FOX East": "News"
}

# --- Setup WebDriver ---
def setup_driver():
    chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--crash-dumps-dir=/tmp")
    chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")

    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    return driver

# --- Scrape Channel Links ---
def get_channel_links(driver, url):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "row")))
    live_tv_row = driver.find_element(By.XPATH, "//h3[contains(text(), 'Live TV Channels')]/..")
    links = live_tv_row.find_elements(By.TAG_NAME, "a")
    return [(link.text.strip(), link.get_attribute("href")) for link in links]

# --- Extract M3U8 URL ---
def extract_m3u8(driver, link):
    try:
        driver.get(link)
        wait = WebDriverWait(driver, 5)
        try:
            video_button = wait.until(EC.element_to_be_clickable((By.ID, 'loadVideoBtn')))
        except:
            video_button = wait.until(EC.element_to_be_clickable((By.ID, 'loadVideoBtnTwo')))
        video_button.click()
        time.sleep(5)

        network_data = driver.execute_script("return JSON.stringify(performance.getEntries());")
        requests = json.loads(network_data)
        m3u8_urls = [r["name"] for r in requests if ".m3u8" in r["name"]]
        return m3u8_urls[0] if m3u8_urls else None
    except Exception:
        return None

# --- Main Execution ---
def main():
    driver = setup_driver()
    print('#EXTM3U url-tvg="https://raw.githubusercontent.com/buhtigd1/TVSD/main/en/tvsd.xml.gz"')

    for name, link in get_channel_links(driver, "https://thetvapp.to/"):
        m3u8_url = extract_m3u8(driver, link)
        if not m3u8_url:
            m3u8_url = "https://raw.githubusercontent.com/buhtigd1/TVSD/main/off/offline.mp4"

        logo_url = channel_logos.get(name, "")
        group_title = group_overrides.get(name, "Others")

        print(f'#EXTINF:-1 tvg-ID="{name}" tvg-name="{name}" tvg-logo="{logo_url}" group-title="{group_title}", {name}')
        print(m3u8_url)

    driver.quit()

if __name__ == "__main__":
    main()
