from selenium import webdriver

driver = webdriver.Edge(executable_path=r'C:\Users\latto\OneDrive\Software\Python\Edge WebDriver\edgedriver_win64\msedgedriver.exe')

driver.

def create_driver():
	try:
		web = webdriver.Firefox()
		print("[*] Opening Mozila FireFox...")
		return web
	except:
		try:
			web = webdriver.Chrome()
			print("[*] We got some errors running Firefox, Opening Google Chrome instead...")
			return web
		except:
			try:
				web = webdriver.Opera()
				print("[*] We got some errors running Chrome, Opening Opera instead...")
				return web
			except:
				try:
					web = webdriver.Edge()
					print("[*] We got some errors running Opera, Opening Edge instead...")
					return web
				except:
					try:
						web = webdriver.Ie()
						print("Bro")
						return web
					except:
						print("Error: \n  Can not call any WebBrowsers\n   Check your Installed Browsers!")
						exit()

def main():
    web_driver = create_driver()

    print("some data about webdriver: ")

if __name__ == '__main__':
    main()