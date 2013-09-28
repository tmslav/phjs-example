import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time

class stock:

    username = ""
    password = ""
    #Here You can write down how much money You want to spend for option trading
    money=5000
    def __init__(self):
        nl=1
        print "Starting browser"
        while(nl):

             try:
                self.br=webdriver.PhantomJS()
                br=self.br
                br.get("https://www.optionsxpress.com/login.asp?r=1")
                br.find_element_by_id("txtUserID").send_keys(self.username)
                br.find_element_by_xpath("//input[@name='txtPassword']").send_keys(self.password)
                br.find_element_by_id("subButton").click()
                while(nl):
                    try:
                        br.switch_to_frame(0)
                        nl=0
                    except:
                        time.sleep(0.2)
                        nl=1
                br.find_element_by_id("toolbox").click()
                br.find_element_by_partial_link_text("Virtual Trading").click()
                nl=1
                while(nl):
                    try:
                        br.find_element_by_class_name("launchBtnTop").click()
                        nl=0
                    except:
                        time.sleep(0.2)
                        nl=1
                br.switch_to_window(br.window_handles[1])
                nl=1
                while(nl):
                        rs=br.execute_script("return document.readyState")
                        if rs!='complete':
                            nl=1
                        else:
                            time.sleep(0.5)
                            nl=0

                br.switch_to_frame(0)
                nl=0

             except:
                nl=1
                self.br.quit()



    def stockinput(self,ticker,buysell,amount):
        print "stockinput(%s,%s,%s)"%(ticker,buysell,amount)
        br=self.br
        nl=1
        while(nl):
            try:
                br.find_element_by_xpath("//li[@id='trade']").click()
                nl=0
            except:
                time.sleep(1)
        hover=ActionChains(br).move_to_element(br.find_element_by_id("trade"))
        hover.perform()
        nl=1
        while(nl):
            try:
                br.find_element_by_partial_link_text("Stock").click()
                nl=0
            except:
                time.sleep(1)
        nl=1
        while(nl):
            try:
                br.find_element_by_id("txtSymbol").send_keys(ticker)
                nl=0
            except:
                time.sleep(1)
        br.find_element_by_id("txtQuantity").send_keys(amount)
        query="//select[@id='lstOrderAction']/option[contains(text(),'"+buysell+"')]"
        br.find_element_by_xpath(query).click()
        br.find_element_by_id("submit1").click()
        nl=1
        while(nl):
            try:
                br.find_element_by_xpath("//input[@class='submit']").click()
                nl=0
            except:
                time.sleep(1)

    def optioninput(self,ticker,callput,bsoc,amount):
        print "optioninput(%s,%s,%s,%s)"%(ticker,callput,bsoc,amount)
        br=self.br
        nl=1
        hover=ActionChains(br).move_to_element(br.find_element_by_xpath("//li[@id='trade']"))
        hover.perform()
        while(nl):
            try:
                br.find_element_by_partial_link_text("Options").click()
                nl=0
            except:
                time.sleep(1)
        nl=1
        while(nl):
            try:
                br.find_element_by_id("txtSymbol00").send_keys(ticker)
                nl=0
            except:
                time.sleep(1)
        from selenium.webdriver.common.keys import Keys
        br.find_element_by_id("txtSymbol00").send_keys(Keys.ENTER)
        nl=1
        while(nl):
            try:
                ask_price =float( br.find_element_by_xpath("//a[contains(@href,'PopulateAsk')]").text)
                nl=0
            except:
                time.sleep(1)
        
        nl=1
        while(nl):
            try:
                br.find_element_by_xpath("//a[contains(@href,'PopulateAsk')]").send_keys(Keys.ENTER)
                nl=0
            except:
                time.sleep(1)
        numberofcalls=int(self.money/(ask_price*100))
        if numberofcalls>10:
            amount=10
        else:
            amount=numberofcalls
        
        br.find_element_by_id("txtQuantity").send_keys(amount)
        query="//select[@id='lstOrderAction']/option[contains(text(),'"+bsoc+"')]"
        br.find_element_by_xpath(query).click()
        query="//select[@id='lstCallPut0_0']/option[contains(text(),'"+callput+"')]"
        nl=1
        time.sleep(1)
        while(nl):
            try:
                br.find_element_by_xpath(query).click()
                nl=0
            except:
                print "3"
                time.sleep(1)
        nl=1
        while(nl):
            try:
                br.find_element_by_id("submit1").click()
                nl=0
            except:
                time.sleep(1)
        nl=1
        while(nl):
            try:
                br.find_element_by_class_name("submit").click()
                nl=0
            except:
                time.sleep(1)
        if "Need to get approved for buying calls/puts." in br.page_source:
            print "\nAccount is not approved for buying calls/puts"
            return
        br.find_element_by_xpath("//input[@name='btnTrade']").click()


    def __del__(self):
        print "Quit"
        self.br.quit()

if __name__=="__main__":
    trader=stock()
    t0=time.time()
    trader.optioninput("AAPL","Call","Buy To Open","1")
    t1=time.time()
    print "Time difference:"+str(t1-t0)
    t0=time.time()
    trader.optioninput("AAPL","Call","Buy To Open","2")
    t1=time.time()
    print "Time difference:"+str(t1-t0)
    t0=time.time()
    trader.stockinput("AAPL","Buy","1")
    t1=time.time()
    print "Time difference:"+str(t1-t0)

