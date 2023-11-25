from selenium import webdriver


class edge_automation:
    driver = webdriver.Edge(executable_path=r'C:\Users\latto\OneDrive\Software\Python\Edge WebDriver\edgedriver_win64\msedgedriver.exe')
    driver.get("https://www.cnn.com/")
    driver.execute_script("window.open('');")
def main():
    cls = edge_automation()

if __name__ == '__main__':
    main()