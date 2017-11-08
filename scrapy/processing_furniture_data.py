#Processing csv files from Craigslist Furniture


import sys
import numpy as np
import pandas as pd
from collections import Counter



manufacturer_list = '''Knoll Herman Miller, Fritz Hansen, Selig, Modernica, Carl Hansen, Swedese, Artek, Moreddi, Cassina, Thayer Coggin, Bramin, Howard Miller, Drexel Declaration, Broyhill Brasilia, Lane Acclaim, Westnofa, USM Haller'''

designer_list = '''Nelson, Eames, Saarinen, Florence Knoll, Paulin, Risom, Ekstrom, Schultz, Wegner, Vodder, Jalk, Olsen'''

style_list = '''mid century, mid-century, century modern, teak, 1960s, 60s'''

blacklist = '''cubicle, aeron, bed, mattress, chest, ethan allen, ikea, baker, grandfather clock, industrial, farmhouse, pottery barn, furnishare'''


def generate_df(filename):

    df = pd.read_csv(filename)
    #Check format:
    for col in ('URL','Meta_HTML','Time','Title'):
        if col not in list(df.columns):
            print "\n Error: '{}' column not in csv file, file is either corrupted or not the correct format \n".format(col)
            sys.exit()
        else:
            continue

    #Convert title to lower case
    df['Title'] = df['Title'].str.lower()

    #Add Price, Location
    for ix , meta in zip(df.index,df['Meta_HTML']):
        df.at[ix, 'Price'] = extract_price(meta)
        df.at[ix, 'Location'] = extract_location(meta).lower()
        #pd.set_option('display.max_colwidth', -1)

    #Add image URL
    for ix, image in zip(df.index,df['Image']):
        df.at[ix, 'Image'] = "https://images.craigslist.org/" +  image[2:].split()[0] + "_600x450.jpg"

    #Describe Table
    print filename + " - date: ", df.at[0, 'Time']
    print df.info()
    return df

def extract_price(result_meta_html):
    if result_meta_html.find('<span class="result-price">') == -1:
        return np.nan
    else:
        start_price = result_meta_html.find('<span class="result-price">') + len('<span class="result-price">')
        end_price = start_price + result_meta_html[start_price:start_price+80].find('</span>')
        price = result_meta_html[start_price: end_price].replace('$', "")
        try:
            price = float(price)
        except:
            price = np.nan
    return price

def extract_location(result_meta_html):
    if result_meta_html.find('<span class="result-hood"> ') == -1:
        return ""
    else:
        start_loc = result_meta_html.find('<span class="result-hood"> ') + len('<span class="result-hood"> ')
        end_loc = start_loc + result_meta_html[start_loc:start_loc+80].find('</span>')
        loc = result_meta_html[start_loc: end_loc].replace('(', "").replace(')',"")
        return loc


def cleaned_search_list(raw_text):
    rep_char = [", "]
    rep_with = ["|"]
    for char, rep in zip(rep_char,rep_with):
        lst = raw_text.replace(char,rep)
    lst = lst.replace("| |", "|")
    return '"' + lst.lower() + '"'

def term_size(lst):
    # outputs two list given an original list of strings:
    # - first only contains single word terms
    # - second only contains two word terms (or more)
    terms_with_2_words = [term for term in lst if (' ' in term) == True if term not in [' \n', '']]
    terms_with_1_word = [term for term in lst if term not in terms_with_2_words if term not in [' \n', ''] ]
    return  terms_with_1_word, terms_with_2_words

def multi_manufacturer_designer(df,column):
    #Generate single word term lists
    manufacturer_ls_1, manufacturer_ls_2 = term_size(cleaned_search_list(manufacturer_list).split("|"))

    #Generate double word term lists
    designer_ls_1, designer_ls_2 = term_size(cleaned_search_list(designer_list).split("|"))

    #Remove Listings where multiple designers or multiple manufacturers are mentioned
    for n in df.index:
        count_m = 0
        count_d = 0
        text = df[column][df.index == n].values

        for phrase in text:
            for i, word in enumerate(phrase.split()):
                if word in manufacturer_ls_1:
                    count_m += 1
                if word in designer_ls_1:
                    count_d += 1
                try:
                    if phrase.split()[i-1] + ' ' + word in manufacturer_ls_2:
                        count_m += 1
                    if phrase.split()[i-1] + ' ' + word in designer_ls_2:
                        count_d += 1
                except:
                    continue

        df.at[n, 'Manufacturers Listed'] = count_m
        df.at[n, 'Designers Listed'] = count_d

    return df[(df['Manufacturers Listed'] <= 1) & (df['Designers Listed'] <= 1)]



def generate_filtered_dfs(filename, max_value=1200):
    pd.set_option('display.max_colwidth', -1)
    df = generate_df(filename)

    #Generate search Terms:
    search_terms = cleaned_search_list(manufacturer_list + '|' + designer_list + '|' + style_list)
    xlist = cleaned_search_list(blacklist)

    #Remove rows withe Title containing terms from blacklist (xlist)
    df = df[df['Title'].str.contains(xlist) == False]
    #Remove duplicates (don't keep any posts which appear more than once)
    df = df.drop_duplicates(subset = 'Title', keep = False)
    #Remove listings with multiple designers/manufacturers listed
    df = multi_manufacturer_designer(df,'Title')

    if 'Description' in list(df.columns):
        #Remove rows where description contains terms from blacklist
        df = df[df['Description'].str.contains(xlist) == False]
        #Remove listings with multiple designers/manufacturers listed in description
        df = multi_manufacturer_designer(df,'Description')

    # Filter out listings with price higher than $1200
    df = df[df['Price'] <= 1200]
    #Return useful rows only
    df = df[['Image', 'Price', 'Title', 'Time', 'Section', 'URL']]

    #Create first df: df1
    # Keep only rows containing key search term
    df1 = df[df['Title'].str.contains(search_terms) == True]
    #Create second df: df2
    # Keep only rows with value $400 and under, remove antique listings
    df2 = df[df['Price'] <= 400]
    df2 = df2[df2['Section'] != "new york - antiques"]

    print "Filtered df1 shape: {}".format(df1.shape)
    print "Filtered df2 shape: {}".format(df2.shape)
    return df1, df2


def export_df_to_html(df, title, htmlid, directory):
    #Add Header with Title
    header = '<h1 style="font-family:Verdana"> {} </h1>'.format(title)
    html = header + "\n" + df.to_html()

    #Update Table Format
    html = html.replace('<table border="1" class="dataframe">',
                        '<table border="1" class="greyGridTable", style="font-family:Verdana"> ')

    #Replace hyperlink text with working links
    html = html.replace('<td>https://','<td><a href="https://' ).replace('.html</td>','.html"> link </a></td>')

    #Replace image hyperlink text with thumbnail
    updated_html = ""
    for line in html.split("\n"):
        if line.find(".jpg</td>") != -1:
            h_image_url = line[line.find('="https://')+2:line.find('.jpg<')+4]
            updated_html += line.replace('.jpg</td>','.jpg"><IMG HEIGHT=75 WIDTH=75 SRC="{}"></a></td>'.format(h_image_url)) + "\n"
        else:
            updated_html += line + "\n"

    #Save HTML in current directory
    time = str(pd.to_datetime('now')).replace(" ", "_")[:13]
    htmlname = "{}-{}.html".format(htmlid,time)

    with open(htmlname, 'w') as f:
        write_html = f.write(updated_html.encode('utf-8'))
    print htmlname + " created in current directory: {}".format(directory)


def update_seen_list(df1,df2):
    pass


if __name__ == '__main__':
    # open the 'alice.txt' file, in the data directory
    filename = str(raw_input("please type in csv filename: "))
    #filename = "all_results-10-232-17-11PM.csv"
    df1, df2 = generate_filtered_dfs(filename)

    export_df_to_html(df1,
                      "List 1: Manufacturer, Designer, Style Filtered List",
                      "List_1",
                      "pages/")
    export_df_to_html(df2,"List 2: Generic Filtered List Under $400 Dollar Amount","List_2")
    print "html files ready"
