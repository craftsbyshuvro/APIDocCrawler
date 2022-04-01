import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

from config import AppConfig


class Crawler:
    def __init__(self, package_info):
        self.package_info = package_info

    def crawl_save_api_details(self):
        class_list = self.extract_classes()

        for single_class in class_list:
            api_methods_info = self.extract_method_docs(single_class)

            api_method_info_df = pd.DataFrame(api_methods_info)

            api_method_info_df.to_csv(AppConfig.API_METHOD_INFO_OUTPUT_FILE_PATH, mode='a', index=False,
                                      header=False)

    def extract_classes(self):
        web_req_response = requests.get(self.package_info['api_doc_full_url'])
        parent_page_content = bs(web_req_response.content, 'lxml')

        # Getting Links of iframe as we need to call it separately as browser does
        iframe_url = parent_page_content.select("iframe ")[0]['src']
        full_iframe_url = self.package_info['doc_base_url'] + iframe_url

        # Requesting to get content of the iframe
        iframe_req_response = requests.get(full_iframe_url)
        iframe_content = bs(iframe_req_response.text, 'lxml')

        # Getting index of table which contains class inforamtion
        all_types_text = [i.text for i in iframe_content.select('ul li table caption span:first-child')]
        class_summary_index = all_types_text.index('Class Summary')

        # Getting content of the class information table
        class_information = iframe_content.select("li.blockList")[class_summary_index].select("th.colFirst>a")
        class_information_links = [i['href'] for i in class_information]

        class_information_full_links = [self.package_info['java_class_doc_base_url'] + i for i in
                                        class_information_links]

        return class_information_full_links

    def extract_method_docs(self, li):
        methods_info_description = []

        api_doc_response = requests.get(li)
        api_doc_content = bs(api_doc_response.text, 'lxml')

        class_name = api_doc_content.select("body > main > div.header > h2.title")[0].get_text()
        class_name = str(class_name).replace('Class', '').strip()

        for i in api_doc_content.select("section[role='region']"):
            if 'Method Summary' in i.get_text():
                tr = api_doc_content.select(".memberSummary tr")

                # We are excluding table header
                for td in tr[3:]:
                    try:
                        modifier_type = td.select(".colFirst")[0].get_text()
                        method = td.select(".colSecond")[0].get_text()
                        description = td.select(".colLast")[0].get_text()

                        methods_info_description.append({'PackageName': self.package_info['package_name'],
                                                         'Class': class_name,
                                                         'ModifierType': modifier_type,
                                                         'Method': method,
                                                         'Description': description
                                                         })
                    except Exception as e:
                        # This exception is not handled
                        pass
                break

        return methods_info_description