from config import AppConfig
from src.crawler.CrawlerType01 import CrawlerType01
import pandas as pd

if __name__ == '__main__':

    # package_info_df = pd.read_csv(AppConfig.PACKAGE_INFO_FILE_PATH)

    package_info = {
        'package_name': 'org.apache.commons.lang3',
        'api_doc_full_url': 'https://javadoc.io/static/org.apache.commons/commons-lang3/3.12.0/org/apache/commons/lang3/package-summary.html',
        'doc_base_url': 'https://javadoc.io',
        'java_class_doc_base_url': 'https://javadoc.io/static/org.apache.commons/commons-lang3/3.12.0/org/apache/commons/lang3/'
    }

    obj_crawler = CrawlerType01(package_info)
    obj_crawler.crawl_save_api_details()


    # write_header_to_csv = True
    # for index, row in package_info_df.iterrows():
    #     package_info = {
    #         'package_name': row['package_name'],
    #         'api_doc_full_url': row['api_doc_full_url'],
    #         'doc_base_url': row['doc_base_url'],
    #         'java_class_doc_base_url': row['java_class_doc_base_url'],
    #         'type': row['type']
    #     }
    #
    #     if package_info['type'] == 'type01':
    #         obj_crawler = CrawlerType01(package_info)
    #         obj_crawler.crawl_save_api_details()
    #
    #     if package_info['type'] == 'type02':
    #         pass
