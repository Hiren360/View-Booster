import time
import random
import multiprocessing
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException
import pyautogui
from urllib.parse import urlparse, parse_qs
from Common import *


class YouTubeAutomation:
    def __init__(self, driver):
        self.driver = driver
        self.actions = ActionChains(driver)

    def random_scroll(self):
        # Scroll randomly both up and down
        scroll_direction = random.choice(['down', 'up'])
        scroll_amount = random.randint(200, 800)

        if scroll_direction == 'down':
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
        else:
            self.driver.execute_script(f"window.scrollBy(0, -{scroll_amount});")

        print(f"Scrolled {scroll_direction} by {scroll_amount}px")
        time.sleep(random.uniform(2, 5))

    def hover_random_element(self):
        try:
            elements = WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a, button, img"))
            )

            if elements:
                element = random.choice(elements)
                if element.size['width'] > 0 and element.size['height'] > 0:
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", element)
                    time.sleep(1)
                    hover = ActionChains(self.driver).move_to_element(element)
                    hover.perform()
                    time.sleep(random.uniform(2, 4))
                    
                else:
                    print("The selected element has no size or location, skipping hover.")
            else:
                print("No elements found to hover over.")

        except Exception as e:
            print(f"An error occurred while performing hover_random_element: {e}")

    def random_pause_and_resume(self, video_player):
        if random.choice([True, False]):
            self.driver.execute_script("arguments[0].pause();", video_player)
            #print("Video paused for a few seconds.")
            time.sleep(random.uniform(5, 10))
            self.driver.execute_script("arguments[0].play();", video_player)
            #print("Video resumed.")

    def random_click(self):
        screen_width, screen_height = pyautogui.size()
        x = random.randint(0, screen_width - 1)
        y = random.randint(0, screen_height - 1)
        pyautogui.moveTo(x, y, duration=random.uniform(0.1, 0.3))
        pyautogui.click()
        #print(f"Clicked at ({x}, {y})")

    def change_video_quality(self, quality='360p'):
        try:
            settings_button = self.driver.find_element(By.XPATH, "//button[@title='Settings']")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", settings_button)
            settings_button.click()
            time.sleep(1)
            quality_button = self.driver.find_element(By.XPATH, "//div[contains(text(),'Quality')]")
            quality_button.click()
            time.sleep(1)
            desired_quality = self.driver.find_element(By.XPATH, f"//span[contains(text(),'{quality}')]")
            desired_quality.click()
            #print(f"Video quality set to {quality}")
            time.sleep(2)
        except Exception as e:
            print(f"Error changing video quality: {e}")

    def switch_tabs(self):
        if random.choice([True, False]):
            random_url = random.choice(URL_LIST)
            self.driver.execute_script(f"window.open('{random_url}', '_blank');")
            self.driver.switch_to.window(self.driver.window_handles[-1])
            time.sleep(random.uniform(3, 6))
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

    def scroll_comments(self, scroll_pause_time=2, max_scrolls=10):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        for _ in range(max_scrolls):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def select_and_play_video(self):
        try:
            video_elements = WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a#video-title"))
            )
            if video_elements:
                selected_video = random.choice(video_elements)
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", selected_video)
                selected_video.click()
                time.sleep(random.uniform(5, 10))
            else:
                #print("No videos found in search results.")
                return False
        except Exception as e:
            #print(f"Error selecting video: {e}")
            return False
        return True

    def interact_with_ads(self):
        try:
            skip_ad_button = self.driver.find_elements(By.CSS_SELECTOR, '.ytp-ad-skip-button')
            if skip_ad_button:
                #print("Ad detected: Skipping ad...")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", skip_ad_button[0])
                skip_ad_button[0].click()
                return True

            watch_ad_button = self.driver.find_elements(By.CSS_SELECTOR, '.ytp-ad-overlay-close-button')
            if watch_ad_button:
                if random.choice([True]):
                    #print("Ad detected: Skipping ad...")
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", watch_ad_button[0])
                    watch_ad_button[0].click()
                else:
                    #print("Ad detected: Watching ad...")
                    time.sleep(random.uniform(5, 20))
                return True

        except Exception as e:
            print(f"Error interacting with ads: {e}")
        return False

    def take_short_break(self):
        break_duration = random.uniform(5, 15)
        #print(f"Taking a short break for {break_duration:.2f} seconds...")
        time.sleep(break_duration)

    def mute_unmute_video(self):
        try:
            mute_button = self.driver.find_elements(By.CSS_SELECTOR, '.ytp-mute-button')
            if mute_button:
                is_muted = self.driver.execute_script(
                    "return document.querySelector('video.html5-main-video').muted;"
                )
                self.driver.execute_script("arguments[0].scrollIntoView(true);", mute_button[0])
                if is_muted:
                    #print("Unmuting the video...")
                    mute_button[0].click()
                else:
                    #print("Muting the video...")
                    mute_button[0].click()
        except Exception as e:
            print(f"Error muting/unmuting video: {e}")

    def perform_random_actions_on_youtube(self, duration):
        start_time = time.time()
        if not self.select_and_play_video():
            return 
        
        if not self.change_video_quality():
            return
        
        # Define the tasks to perform in random order
        tasks = [
            self.random_scroll,
            self.hover_random_element,
            self.switch_tabs,
            self.mute_unmute_video,
            self.take_short_break,
            self.interact_with_ads,
            self.scroll_comments,
            self.change_video_quality
        ]

        # Continue until the specified duration has passed
        while time.time() - start_time < duration:
            # Shuffle the task list to randomize the order
            random.shuffle(tasks)

            # Loop through the tasks in the random order and execute each one
            for task in tasks:
                try:
                    task()  # Call the task function
                    time.sleep(random.uniform(2, 5))  # Add some randomness between actions
                except Exception as e:
                    print(f"An error occurred while performing task {task.__name__}: {e}")

            # Randomize the amount of time to wait before starting the next round of tasks
            time.sleep(random.uniform(5, 10))  # Random wait time before starting the next round

        print(f"Stayed on YouTube for {duration / 60:.2f} minutes.")


# Function to search YouTube using a keyword
def search_youtube(driver, search_query):
    search_box = WebDriverWait(driver, 40).until(lambda d: d.find_element(By.NAME, 'search_query'))
    search_query = random.choice(search_query)
    search_box.clear()
    for char in search_query:
        search_box.send_keys(char)
        time.sleep(random.uniform(0.1, 0.4))  # Typing delay to simulate human input
    search_box.send_keys(Keys.RETURN)  
    time.sleep(3)  # Wait for the page to load
    return driver.page_source

# Extract video ID from a given YouTube URL
def extract_video_id(url):
    parsed_url = urlparse(url)
    
    # Check for standard YouTube URL (www.youtube.com)
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        query_params = parse_qs(parsed_url.query)
        return query_params.get('v', [None])[0]
    
    # Check for shortened YouTube URL (youtu.be)
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]  # Remove the leading "/"
    
    return None

# Function to find video URLs and their video IDs in search result page
def get_video_ids(driver):
    video_elements = driver.find_elements(By.XPATH, "//a[@id='video-title']")
    video_ids = []
    for video in video_elements:
        video_url = video.get_attribute("href")
        video_id = extract_video_id(video_url)
        video_ids.append((video_url, video_id))
    return video_ids

# Function to find video elements and their video IDs in search result page
def get_video_elements(driver):
    return driver.find_elements(By.XPATH, "//a[@id='video-title']")

def search_by_channel(driver, channel_name, target_video_id):
    search_box = driver.find_element(By.NAME, "search_query")
    search_box.clear()
    search_box.send_keys(channel_name)
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)  # Wait for the search results to load

    # Now we can locate the channel and click on it
    try:
        channel_element = driver.find_element(By.XPATH, f"//a[contains(@title, '{channel_name}')]")
        driver.execute_script("arguments[0].scrollIntoView(true);", channel_element)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable(channel_element)).click()
        time.sleep(5)  # Wait for channel page to load

        # Search for the target video within the channel
        video_elements = get_video_elements(driver)
        for video_element in video_elements:
            try:
                video_url = video_element.get_attribute("href")
                video_id = extract_video_id(video_url)
                
                if video_id == target_video_id:
                    #print("Video found on the channel page.")
                    driver.execute_script("arguments[0].scrollIntoView(true);", video_element)
                    WebDriverWait(driver, 30).until(EC.element_to_be_clickable(video_element)).click()
                    time.sleep(random.uniform(5, 10))  # Let the video load
                    return True  # Return True if video is found
            except Exception as e:
                print(f"Error finding video on channel: {e}")
                continue
    except Exception as e:
        print(f"Channel '{channel_name}' not found: {e}")

    return False  # Return False if video is not found on the channel page

# Function to scroll down and load more videos, returns the position of the target video if found
def scroll_and_load_more(driver, target_video_id, channel_name=None):
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    video_position = 0  # Track the position of videos
    max_scroll_attempts = 10  # Scroll up to 10 times (adjust based on preference)
    scroll_attempt = 0

    while scroll_attempt < max_scroll_attempts:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(10)  # Wait for new videos to load
        new_height = driver.execute_script("return document.documentElement.scrollHeight")

        # Check all video elements in the current viewport
        video_elements = get_video_elements(driver)
        for video_element in video_elements:
            try:
                video_url = video_element.get_attribute("href")
                video_id = extract_video_id(video_url)
                video_position += 1  # Increment the position counter

                if video_id == target_video_id:
                    print(f"Current Position:{video_position}")
                    # Ensure the video element is in view and clickable
                    driver.execute_script("arguments[0].scrollIntoView(true);", video_element)
                    WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, ".//a[@id='video-title']"))
                    )
                    # Try to click the video element
                    try:
                        video_element.click()
                    except Exception as e:
                        print(f"Normal click failed: {e}")
                        # Use JavaScript click as a fallback
                        driver.execute_script("arguments[0].click();", video_element)
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'button.ytp-large-play-button'))
                    )  # Wait for the play button to be clickable
                    time.sleep(random.uniform(5, 10))  # Let the video load
                    return video_position  # Return the position of the found video
            except Exception as e:
                print(f"Error processing video element: {e}")
                continue
        
        # If we've scrolled to the bottom, break the loop
        if new_height == last_height:
            break
        
        last_height = new_height
        scroll_attempt += 1

    #print(f"Target video not found in the top {video_position} videos.")
    
    # If video is not found, search by channel name (if provided)
    if channel_name:
        #print(f"Searching for channel: {channel_name}")
        search_by_channel(driver, channel_name, target_video_id)
    else:
        print("No channel name provided for fallback search.")
    
    return -1  # Return -1 if the video is not found

# Modified search and play video function to return the position
def search_and_play_video(driver, keywords, channel_name, video_link):
    # Extract the video ID from the provided link
    target_video_id = extract_video_id(video_link)
    if not target_video_id:
        #print("Invalid target video URL.")
        return False

    # Step 1: Search by keyword
    search_youtube(driver, keywords)
    position = scroll_and_load_more(driver, target_video_id)
    if position != -1:
        print(f"Current Position by Channel Name: {position}")
        return position  # Return the position if the video is found
    
    # If not found, check all videos on the current page
    video_elements = get_video_elements(driver)
    print([e.get_attribute("href") for e in video_elements])

    # Step 2: Check if target video ID is in search results
    video_position = 0  # Track position
    for video_element in video_elements:
        video_url = video_element.get_attribute("href")
        video_id = extract_video_id(video_url)
        video_position += 1  # Increment the position counter
        if video_id == target_video_id:
            print(f"Current Position by keyword: {video_position}")
            video_element.click()  # Click the video to play
            time.sleep(random.uniform(5, 10))  # Let the video load
            return video_position  # Return the position

    # Step 3: If not found, search by channel name
    #print(f"Video not found by keyword, searching by channel name: {channel_name}")

    search_youtube(driver, channel_name)
    position = scroll_and_load_more(driver, target_video_id)
    if position != -1:
        print(f"Current Position by Channel Name: {position}")
        return position  # Return the position if the video is found

    # Step 4: Check if target video ID is in search results
    video_position = 0  # Track position
    for video_element in video_elements:
        video_url = video_element.get_attribute("href")
        video_id = extract_video_id(video_url)
        video_position += 1  # Increment the position counter
        print(video_id)
        if video_id == target_video_id:
            print(f"Current Position by Channel Name: {video_position}")
            video_element.click()  # Click the video to play
            time.sleep(random.uniform(5, 10))  # Let the video load
            return video_position  # Return the position

    # Step 5: If video is not found
    print(f"Video with ID {target_video_id} not found in either search.")
    return -1  # Return -1 if the video is not found

# Main function to perform YouTube tasks
def perform_youtube_task(video_link, video_time, keywords,channel_name, min_watch_time=20, max_watch_time=90):
    driver = setup_driver_with_proxy()
    automation = YouTubeAutomation(driver)  # Assuming you have a function to setup driver
    CHECK_INTERVAL = 5
    MAX_RETRIES = 5
    
    try:
    
        # Search for a video based on keywords
        driver.get("https://www.youtube.com")
        search_box = WebDriverWait(driver, 40).until(lambda d: d.find_element(By.NAME, 'search_query'))
        search_query = random.choice(CONTENTS_LIST)
        for char in search_query:
            search_box.send_keys(char)
            time.sleep(random.uniform(0.1, 0.4))  # Typing delay to simulate human input
        search_box.send_keys(Keys.RETURN)
        time.sleep(random.randint(3,6))
        search_box.clear()

        # Mimic some random scrolling or hovering before selecting a video
        if random.choice([False]):
            automation.random_scroll()
            automation.hover_random_element()
        time.sleep(random.uniform(5, 10))

        # Perform random actions on YouTube before playing the video to stay for at least 10 minutes
        if random.choice([False]):
            #print("Performing random actions on YouTube for 10 minutes...")
            automation.perform_random_actions_on_youtube(random.uniform(600, 900)) 

        search_and_play_video(driver,keywords,channel_name,video_link)
        time.sleep(random.uniform(5, 10))  # Let the video load
               
        for attempt in range(MAX_RETRIES):
            try:
                video_player = WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, 'video.html5-main-video'))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", video_player)
                time.sleep(2)  # Allow time for scrolling to complete

                # Check if the video is playing, and play if it's paused
                is_playing = driver.execute_script(
                    "return !document.querySelector('video.html5-main-video').paused;"
                )
                if not is_playing:
                    play_button = WebDriverWait(driver, 60).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "ytp-large-play-button"))
                    )
                    driver.execute_script("arguments[0].click();", play_button)
                    #print("Video is now playing.")
                    break
                else:
                    #print("Video is already playing.")
                    break

            except (TimeoutException, WebDriverException) as e:
                if attempt < MAX_RETRIES - 1:
                    #print(f"Retrying due to connection error: {e}")
                    time.sleep(random.randint(5, 9))
                else:
                    #print(f"Failed after {MAX_RETRIES} attempts: {e}")
                    return False

        # Periodically check if the video is playing and mimic human behavior
        start_time = time.time()
        while time.time() - start_time < video_time:
            try:

                # Determine random watch time for this segment
                watch_time = random.uniform(min_watch_time, max_watch_time)
                end_time = time.time() + watch_time
                
                while time.time() < end_time:
                    is_playing = driver.execute_script("return !document.querySelector('video.html5-main-video').paused;")
                    if not is_playing:
                        driver.execute_script("arguments[0].click();", video_player)
                        #print("Video was paused. Playing again...")

                    # Interact with ads if they appear
                    if random.choice([True,False]):
                        automation.interact_with_ads()

                    # Simulate a short break occasionally
                    if random.choice([True, False]):
                        automation.take_short_break()

                    # Randomly mute or unmute the video
                    if random.choice([True, False]):
                        automation.mute_unmute_video()
                        
                    # Mimic some random human-like behavior during video playback
                    if random.choice([True, False]):
                        automation.random_scroll()
                        automation.hover_random_element()
                        automation.random_pause_and_resume(video_player)

                    time.sleep(CHECK_INTERVAL)  # Wait before checking again

            except Exception as e:
                print(f"Error during playback check: {e}")

        print("Finished watching video")

    except TimeoutException as e:
        print(f"Timeout occurred: {e}")
    except WebDriverException as e:
        print(f"WebDriver encountered an issue: {e}")
    except Exception as e:
        print(f"Unexpected error during YouTube task: {e}")

    finally:
        driver.quit()

def start_processes(num_processes, video_link, video_time, keywords, channel_name, batch_size=6):
    total_batches = (num_processes + batch_size - 1) // batch_size  # Calculate total batches

    for batch in range(total_batches):
        start_index = batch * batch_size
        end_index = min(start_index + batch_size, num_processes)
        current_batch_size = end_index - start_index

        print(f"Starting batch {batch + 1} with {current_batch_size} browsers...")

        pool = None  # Initialize pool to None
        try:
            pool = multiprocessing.Pool(processes=current_batch_size)
            pool.starmap(perform_youtube_task, [(video_link, video_time, keywords, channel_name)] * current_batch_size)
            pool.close()
            pool.join()  # Ensure this batch is fully done before moving to the next

        except Exception as e:
            print(f"An error occurred during batch {batch + 1}: {e}")
        finally:
            if pool is not None:
                pool.terminate()  # Terminate pool if it's been initialized

        # Ensure that after one batch finishes, we wait before starting the next one
        time.sleep(random.uniform(3, 6))  # Randomize sleep between batches to prevent IP bans

    return num_processes

if __name__ == '__main__':
    # Entry point for the script
    youtube_url = "https://youtu.be/bTauFnlF-oQ"
    video_time = 5000  # Set the exact video length in seconds
    num_processes = 334
    Keywords = ["Pubg Multiple Matches","Multiple Pubg Matches"]
    channel_name = ["business work"]
    #perform_youtube_task(youtube_url, video_time, ["AWS Healthscribe","healthscribe video"],["Fahd Mirza"])
    start_processes(num_processes,youtube_url,video_time,Keywords,channel_name,50)



