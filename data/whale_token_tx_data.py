from .whale_eth_tx_data import *
from .html_helper import get_html_by_url
import sys

def identify_investor_type_helper_token_helper(soup):
    no_matching_exist = soup.find("font",{"color":"black"})
    if no_matching_exist is not None:
        return None
    trs = soup.find("div",{"class":"table-responsive"}).findAll("tr")
    tx_arr = []
    for tr_index,tr in enumerate(trs):
        if tr_index != 0:
            tds = tr.findAll("td")
            for td_index,td in enumerate(tds):
                if td_index == 3:
                    # type
                    tx_type = td.find("span").text
                    if "IN" in tx_type:
                        tx_type = "IN"
                    else:
                        tx_type = 'OUT'
                elif td_index == 4:
                    #to
                    m_a = td.find("a")
                    if m_a is None:
                        m_a = td.find("span")
                    to_address = m_a.text
            to_address = to_address.lower()
            tx_arr.append([tx_type,to_address])
    for tx in tx_arr:
        [tx_type,to_address] = tx
        if tx_type == "OUT" and (("auction" in to_address) or ("sale" in to_address) or ("etherdelta" in to_address)):
            return personal_type
        if tx_type == "OUT" and (("binance" in to_address) or ("liqui" in to_address) or ("bittrex" in to_address) or ("poloniex" in to_address) or ("bitfinex" in to_address)):
            return exchange_type
    return affliate_type

def identify_investor_type_token(account):
    url = "https://etherscan.io/tokentxns?a={}".format(account)
    soup = get_html_by_url(url)
    total_number_of_page = get_total_number_of_page(soup)
    print("\t\t[identify_investor_type] Token:{} for {}".format(total_number_of_page,account))

    investor_type = identify_investor_type_helper_token_helper(soup)
    if investor_type != affliate_type: return investor_type

    for i in range(2,min(bfs_max_depth+1,total_number_of_page+1)):
        print("\t\t{}".format(i))
        soup = get_html_by_url("{}&p={}".format(url,i))
        investor_type = identify_investor_type_helper_token_helper(soup)
        if investor_type != affliate_type: return investor_type
    return affliate_type
