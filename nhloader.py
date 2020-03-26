import os
import requests
import shutil
import json
import re


def get_request(link):
    try:
        x = requests.get(link)
        return x
    except Exception as e:
        print("Encountered exception: " + str(x))
        return False


# copied some of this part from somewhere
def download_picture(folder, link):
    print("downloading picture from: " + str(link))
    try:
        #parse the image link to get the name / type // jpg, gif etc
        new_name = link.split("/")[-1]
        # Open the url image, set stream to True, this will return the stream content.
        resp = requests.get(link, stream=True)
        # Open a local file with wb ( write binary ) permission.
        # \\ for windows, gonna make it work on debian at some point
        local_file = open(folder + "\\" + new_name, 'wb')
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        resp.raw.decode_content = True
        # Copy the response stream raw data to local image file.
        shutil.copyfileobj(resp.raw, local_file)
        # Remove the image url response object.
        del resp
        return True
    except Exception as e:
        print("Was unable to download: " + link)
        print("error received: " + str(e))
        return False
    

# this function gets the picture link from the page link + page nr
def get_picture_link(link, page_nr):
    print("Getting picture link")
    rdata = get_request(link + "/" + page_nr + "/")
    data = rdata.text
    base_split = '<img src="https://i.nhentai.net/galleries/'
    # this might have errors, the reason for try except
    try:
        split_data = data.split(base_split)[1][:17]
    except Exception as e:
        print("Failed with: " + str(e))
        print("with the following data: " + str(data))
        print("link is: " + link + ", page nr is: " + page_nr)
    
    media_id = split_data.split("/")[0]
    
    # taking default jpg
    pic_type = ".jpg"
    if ".png" in split_data:
        pic_type = ".png"
    
    full_link = "https://i.nhentai.net/galleries/" + \
            media_id + "/" + page_nr + pic_type
    return full_link


# will use the numbah as folder name until i make this
def get_doujin_name(link):
    print("TODO")
    
    
# this function gets the page number in a list
def get_page_numbers(link, id):
    # link here is full link 
    print("Getting page number")
    page_list = []
    rdata = get_request(link + id)
    data = rdata.text
    split_data = data.split(id)
    for x in split_data:
        if x == None:
            continue
        # this part needs more testing
        splited_numbers = (x[:6])
        new_list = re.findall('\d+', splited_numbers)
        for y in new_list:
            if y != []:
                page_list.append(y)
    return page_list
    

# this function does most of the jobs directly with a link
def get_doujin_from_id(link, id):
    print("Getting doujin from number: " + str(id))
    # getting page numbers
    page_list = get_page_numbers(link, id)
    
    # getting links from all the pics
    links_list = []
    for x in page_list:
        picture_link = get_picture_link(link + id, x)
        links_list.append(picture_link)
        
    # creating folder paths
    base_folder = "mangas"
    new_directory = os.path.join(base_folder, id)
    if not os.path.exists(new_directory):
        os.makedirs(new_directory)
    
    # downloading each page from the links_list
    for y in links_list:
        download_picture(new_directory, y)


# this function will get the list from the file
def get_numbah_list(fpath):
    print("getting the list number") # will read from file at some point
    # not sure to use them as int or string
    # but going for string right now
    list = ["306493", "306495", "306496", "306502"]
    return list
    

def main():
    nhlink = "https://nhentai.net/"
    # g comes from gallery, i just found out
    nhid = "g/"
    file_path = "numbahrs.txt"
    list = get_numbah_list(file_path)
    for x in list:
        get_doujin_from_id(nhlink + nhid, x)
    
    print("Done Main")

            
if __name__ == "__main__":
    print("Started the nhscrapper")
    main()
