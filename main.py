import time
from RPA.Browser.Selenium import Selenium

from RPA.Robocorp.WorkItems import WorkItems

from setup import URL, SEARCH_PHRASE, NUMBER_OF_MONTHS, CATEGORY
from util import (
    set_month_range,
    write_csv_data,
    replace_date_with_hour,
    download_image_from_url,
    check_for_dolar_sign,
    check_phrases,
    create_image_folder,
    get_all_files_from_folder,
)


class SeleniumScraper:
    def __init__(self):
        self.browser_lib = Selenium()

    def close_browser(self) -> None:
        self.browser_lib.close_browser()
# Open Browser
    def open_website(self, url: str) -> None:
        self.browser_lib.open_available_browser(url)
        self.browser_lib.maximize_browser_window()
        terms_accept = "//button[@data-testid='GDPR-accept']"
        is_term_button = self.browser_lib.does_page_contain_button(terms_accept)
        if is_term_button:
            self.browser_lib.click_button(locator=terms_accept)
# Start search
    def begin_search(self, search_phrase: str) -> None:
        try:
            search_xpath = "//button[@data-test-id='search-button']"
            self.browser_lib.click_button_when_visible(locator=search_xpath)
            field_xpath = "//input[@placeholder='SEARCH']"
            self.browser_lib.input_text(locator=field_xpath, text=search_phrase)
            go_button_xpath = "//button[@type='submit']"
            self.browser_lib.click_button_when_visible(locator=go_button_xpath)

        except ValueError as e:
            raise f"Error on execution of begin_search -> {e}"
# Set category
    def select_category(self, categorys) -> None:
        if len(categorys) == 0:
            return
        for value in categorys:
            try:
                section_drop_btn = "//div[@data-testid='section']/button[@data-testid='search-multiselect-button']"
                self.browser_lib.click_button_when_visible(locator=section_drop_btn)
                sections_list = "//*[@data-testid='section']//li"
                self.browser_lib.wait_until_page_contains_element(locator=sections_list)
                section = f"//input[@data-testid='DropdownLabelCheckbox' and contains(@value, '{value}')]"
                self.browser_lib.click_element(section)

            except:
                print(f"Category not found")
# Sort Results
    def sort_newest_news(self, list_value="newest") -> None:
        try:
            sort_dropdow_btn = "//select[@data-testid='SearchForm-sortBy']"
            self.browser_lib.select_from_list_by_value(sort_dropdow_btn, list_value)

        except ValueError as e:
            raise f"Error on execution of sort_newest_news -> {e}"
# Set date range
    def set_date_range(self, number_of_months: int) -> None:
        try:
            date_button = "//button[@data-testid='search-date-dropdown-a']"
            self.browser_lib.click_button_when_visible(locator=date_button)
            specific_dates_button = "//button[@value='Specific Dates']"
            self.browser_lib.click_button_when_visible(locator=specific_dates_button)
            input_date_range_start = "//input[@id='startDate']"
            input_date_range_end = "//input[@id='endDate']"
            date_start, date_end = set_month_range(number_of_months)
            self.browser_lib.input_text(input_date_range_start, date_start)
            self.browser_lib.input_text(input_date_range_end, date_end)
            self.browser_lib.click_button_when_visible(locator=date_button)

        except ValueError as e:
            raise f"Error on execution of data range -> {e}"
# Display results
    def load_all_news(self):
        show_more_button = "//button[normalize-space()='Show More']"
        while self.browser_lib.does_page_contain_button(show_more_button):
            try:
                self.browser_lib.wait_until_page_contains_element(
                    locator=show_more_button
                )
                self.browser_lib.scroll_element_into_view(locator=show_more_button)
                self.browser_lib.click_button_when_visible(show_more_button)
            except:
                print("Page show more button done")

    def get_element_value(self, path: str) -> str:
        if self.browser_lib.does_page_contain_element(path):
            return self.browser_lib.get_text(path)
        return ""

    def get_image_value(self, path: str) -> str:
        if self.browser_lib.does_page_contain_element(path):
            return self.browser_lib.get_element_attribute(path, "src")
        return ""

    def load_all_news(self) -> None:
        show_more_button = "//button[@data-testid='search-show-more-button']"
        while self.browser_lib.does_page_contain_button(show_more_button):
            try:
                self.browser_lib.wait_until_page_contains_element(
                    locator=show_more_button
                )
                time.sleep(1)
                self.browser_lib.click_element(show_more_button)
            except:
                print("Page show more button done")

    def get_element_value(self, path: str) -> str:
        if self.browser_lib.does_page_contain_element(path):
            return self.browser_lib.get_text(path)
        return ""

    def get_image_value(self, path: str) -> str:
        if self.browser_lib.does_page_contain_element(path):
            return self.browser_lib.get_element_attribute(path, "src")
        return ""

# scrape data
    def extract_website_data(self, search_phrase: str) -> None:
        self.load_all_news()
        element_list = "//ol[@data-testid='search-results']/li[@data-testid='search-bodega-result']"
        news_list_elements = self.browser_lib.get_webelements(element_list)
        extracted_data = []
        for value in range(1, len(news_list_elements) + 1):
            date = replace_date_with_hour(
                self.get_element_value(f"{element_list}[{value}]//span[@data-testid]")
            )
            title = self.get_element_value(f"{element_list}[{value}]//h4")
            description = self.get_element_value(f"{element_list}[{value}]//a/p")
            image = download_image_from_url(
                self.get_image_value(f"{element_list}[{value}]//img")
            )

            is_title_dolar = check_for_dolar_sign(title)
            is_description_dolar = check_for_dolar_sign(description)
            phrases_count = check_phrases(text_pattern=search_phrase, text=title)

            extracted_data.append(
                [
                    date,
                    title,
                    description,
                    image,
                    is_title_dolar,
                    is_description_dolar,
                    check_phrases(
                        text_pattern=search_phrase,
                        text=description,
                        count=phrases_count,
                    ),
                ]
            )
        # create csv  file
        write_csv_data(extracted_data)

    def main(self) -> None:
        try:
            create_image_folder()
            wi = WorkItems()
            wi.get_input_work_item()
            url = wi.get_work_item_variable("url")
            search_phrase = wi.get_work_item_variable("search_phrase")
            category = wi.get_work_item_variable("category")
            number_of_months = wi.get_work_item_variable("number_of_months")
            self.open_website(url=url)
            self.begin_search(search_phrase=search_phrase)
            self.select_category(categorys=category)
            self.sort_newest_news()
            self.set_date_range(number_of_months)
            self.extract_website_data(search_phrase)
            wi.add_work_item_file("./result.xlsx", "RESULT_EXCEL.xlsx")
            files = get_all_files_from_folder()
            wi.create_output_work_item(files=files, save=True)
            wi.create_output_work_item(files="./result.xlsx", save=True)

        finally:
            # close browser
            self.close_browser()


if __name__ == "__main__":
    obj = SeleniumScraper()
    obj.main()
