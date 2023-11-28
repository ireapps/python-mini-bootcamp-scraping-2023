import csv

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


filename_latest = 'charleston-wv-court-docket-latest.csv'
filename_combined = 'charleston-wv-court-docket-combined.csv'


def download_latest():
    ''' A function to scrape the latest data from the docket '''

    # tracking list for the data to write
    data_out = []

    # https://playwright.dev/python/docs/library#usage
    with sync_playwright() as p:

        # launch a chromium browser
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # visit the page
        page.goto('https://charlestonwvpayments.com/court-docket')

        # https://playwright.dev/python/docs/locators#locate-by-text
        page.get_by_text('Search By Last Names').click()

        # wait for the entire page to load
        page.wait_for_load_state('networkidle')

        # grab the HTML for the page
        html = page.inner_html('body')

    # turn it into soup!
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc
    soup = BeautifulSoup(html, 'html.parser')

    # target the divs with the class 'well'
    # and use list indexing [1:] to exclude the first one,
    # which isn't actually a result
    divs = soup.find_all('div', {'class': 'well'})[1:]

    # using this to keep track of unique headers
    # as a precaution
    headers = set()

    # loop over the `well` divs
    for div in divs:

        # start an empty dict to hold data about this citation
        citation_data = {}

        # get a list of all the `strong` tags in this div
        # -- but skip the first bolded number
        strong_tags = div.find_all('strong')[1:]

        # loop over the strong tags and parse the text
        # in the containing paragraph
        for st in strong_tags:
            attr_list = st.parent.text.split(':', 1)

            if 'Docket No' in attr_list[1]:
                court_date, docket_no = attr_list[1].split('Docket No:')

                citation_data['Court Date'] = court_date.strip()
                citation_data['Docket No'] = docket_no.strip()
            else:
                key, val = attr_list
                val = ' '.join(val.split())
                citation_data[key] = val

        # update our running set of headers
        headers.update(citation_data.keys())

        # and add this record to the tracking list
        data_out.append(citation_data)

    # open the `latest` file and write the results
    with open(filename_latest, 'w') as outfile:
        writer = csv.DictWriter(
            outfile,
            fieldnames=sorted(list(headers))
        )
        writer.writeheader()
        writer.writerows(data_out)

        print(f'Wrote file: {filename_latest}')


def add_to_combined_file():
    ''' A function that adds any new records from the `latest` file into the `combined` file '''

    with open(filename_combined, 'r') as infile:
        data_combined = csv.DictReader(infile)
        headers = data_combined.fieldnames
        data_combined = list(data_combined)
        citation_nos = [x['Citation No'] for x in data_combined]

    with open(filename_latest, 'r') as infile:
        data_latest = list(csv.DictReader(infile))

    data_new = [x for x in data_latest if x['Citation No'] not in citation_nos]

    if data_new:
        data_combined.extend(data_new)

        with open(filename_combined, 'w') as outfile:
            writer = csv.DictWriter(
                outfile,
                fieldnames=headers
            )

            writer.writeheader()
            writer.writerows(data_combined)
            print(f'Wrote file: {filename_combined}')
    else:
        print('No new records to write to combined file')


if __name__ == '__main__':
    download_latest()
    add_to_combined_file()
