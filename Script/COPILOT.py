from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as Exc
from selenium.webdriver.edge.service import Service
import time

class LLM:

    def __init__(self):
         
            options = Options()
            service = Service(executable_path=r"C:\El_3ariff\Edge_Driver\msedgedriver.exe")
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--force-device-scale-factor=1")
            options.add_experimental_option("detach", True)
            self.driver = webdriver.Edge(options=options, service=service)
            self.driver.get("https://m365.cloud.microsoft/chat")

    def start_chat(self):

        try:
            Chat_Instance = WebDriverWait(self.driver, 60).until(EC.visibility_of_element_located((By.XPATH, "//a[@aria-label='virtual assistant']")))
            Chat_Instance.click()
            
        except Exc.TimeoutException:
                    print("exception..")
                    Message_Box = WebDriverWait(self.driver , 10).until(EC.element_to_be_clickable((By.XPATH,"//p[@dir= 'auto']")))
                    Default_Message = "virtual assistant"
                    Message_Box.send_keys(Default_Message)
                    time.sleep(5)
                    Button = WebDriverWait(self.driver , 10).until(EC.element_to_be_clickable((By.XPATH,"//button[@type= 'submit']")))
                    Button.click()
                

    def get_answer(self, retrieved_context, user_query):
      prompt = f"""You are a helpful assistant. Use ONLY the provided context to answer the user's question. If the context does not contain the answer, say "I don't have enough information." if the user asks you about info. Context: {" ".join(retrieved_context)} User Question: {user_query}"""
      WebDriverWait(self.driver, 200).until(lambda d: d.find_element(By.XPATH,"//div[@data-testid='lastChatMessage']").text.strip() != "")

      try:
        
        Message_Box = WebDriverWait(self.driver , 10).until(EC.element_to_be_clickable((By.XPATH,"//p[@dir= 'auto']")))      
        Message_Box.send_keys(prompt)
        time.sleep(5)
        Button = WebDriverWait(self.driver , 10).until(EC.element_to_be_clickable((By.XPATH,"//button[@type= 'submit']")))
        Button.click()

      except Exc.StaleElementReferenceException:

        Message_Box = WebDriverWait(self.driver , 10).until(EC.element_to_be_clickable((By.XPATH,"//p[@dir= 'auto']")))      
        Message_Box.send_keys(prompt)
        time.sleep(5)
        Button = WebDriverWait(self.driver , 10).until(EC.element_to_be_clickable((By.XPATH,"//button[@type= 'submit']")))
        Button.click()

      WebDriverWait(self.driver, 200).until(lambda d: d.find_element(By.XPATH,"//div[@data-testid='lastChatMessage']").text.strip() != "")
      answer = self.driver.find_element(By.XPATH,"//div[@data-testid='lastChatMessage']").text
      return answer

    def quit_Copilot(self):
         self.driver.quit()