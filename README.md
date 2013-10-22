# eBay Collection Creator

### A dopeass utility for curating [eBay collections](http://www.ebay.com/cln) from locations across the web.

Usage
-----

The application requires eBay cookies, saved in the Mozilla `cookies.txt` file format. To obtain these cookies:

- Open Firefox
- Install the [Cookie Exporter](https://addons.mozilla.org/en-US/firefox/addon/cookie-exporter/) extension
- Log into [ebay.com](https://signin.ebay.com/ws/eBayISAPI.dll?SignIn)
- In the Tools menu, select "Export Cookies..."
- Save the file as cookies.txt

Next create a collection on eBay.com and obtain the COLLECTION_ID from the URL (e.g. "http://www.ebay.com/cln/mitgleitz/This-Is-Why-Im-Broke/58099917014" -> 58099917014).

Add items to your collection with the following command

    python collect.py -c COLLECTION_ID

Author
------

-  Benjamin Gleitzman ([@gleitz](http://github.com/gleitz))


Notes
-----

-  Edit the `fetch_broke_items` function to collect items from other locations on the web.
