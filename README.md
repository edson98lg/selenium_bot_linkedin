# selenium_bot_linkedin
This code is not intended for webscrapping, but for supervised low-scale information extraction.

## How to start
First you must install the requirements
```
pip install -r requirements.txt
```

To use the program, you need to provide your credentials in `config.json`. Additionally, you should know that in the `"LINKEDIN_TARGET_COMPANY"` variable, you should enter the target company. 
The target company is the company from which you want to extract information about its current or former employees.
> In this example the target company is Microsoft
```
"LINKEDIN_TARGET_COMPANY": "https://www.linkedin.com/company/157240/"
```
### how to get the link to the target company?
1. Go to a profile of someone who has worked at the target company.
2. Right click on the company logo and then inspect the element.
3. Find the anchor element <a> in the html, and copy the link.

## Considerations
