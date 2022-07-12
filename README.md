# Web Scraping using Selenium in Python

## Milestone 1: Getting all the product links from - https://store.eu.square-enix-games.com/en_GB/

- Collected all the product link from Square-Enix Store website using Object-Oriented Programming using Selenium to automate the process.
- Object-Oriented Programming is used to avoid repeating codes and overall more cleaner.
- Sqaure Enix Website because there are different types of products and different methods required to write such as age restriction, making it more interesting.
- Selenium is used to automate program and collect useful data's from websites.

## Milestone 2: Scrape all the product links

- Collected all the data and stored it as a dictionary: title, price, status, images, SKU (Product ID), UUID (Randomly Generated ID). Use the dictionary and convert it into raw data using json file and store it into a folder. Download all the images from the product image and store it all into a image folder.
- Used dictionary to store all the data so that it can be imported into json file more easier.
- Used v4 UUID to generate a unique ID. Eventhough v4 UUID does not 100% generates a unique ID but with 32 bit of data being randomized you can assure that 99.99% of the time will be unique.
- Downloaded all the image and all the raw_data so that in case website URL changes, we will have a reference to the images and data.
