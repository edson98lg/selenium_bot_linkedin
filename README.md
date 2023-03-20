# selenium_bot_linkedin
This code is not intended for webscrapping, but for supervised low-scale information extraction.
  
## How to start
**First you must install the requirements.**
```
pip install -r requirements.txt
```
**Second you must provide your credentials in `config.json`.**  
Additionally, you should know that in the `"LINKEDIN_TARGET_COMPANY"` variable, you should enter the target company. 
The target company is the company from which you want to extract information about its current or former employees.
> In this example the target company is Microsoft
```
"LINKEDIN_TARGET_COMPANY": "https://www.linkedin.com/company/157240/"
```
### How to get the link to the target company?
1. Go to a profile of someone who has worked at the target company.
2. Right click on the company logo and then inspect the element.
3. Find the anchor element <a> in the HTML, and copy the link.
  
## How to use the code properly?
1. Run the code and wait for login
> The console will display this message:(don't press Enter yet)  
`Press Enter when you are in the list of people who work or used to work in the target company.`
2. Type in the search box the company target
3. Active "People"
4. Select "All Filters"
5. Activate the checkboxes of your preferences. (Locations, Current Company, Past Company)
6. Select "Show Results"
7. Press Enter
> If this message is displayed, please click the next page, and then click enter in the console  
`I could't find the 'next' bottom, please click 'next' and then enter :( `
 
**
## ingresar al filtro
## Considerations
 
