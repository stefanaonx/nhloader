import os
import sys
import requests
import shutil
import json
import re
import time


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
    # if i don't have this sleep, i'll get a timeout from nginx
    time.sleep(1)
    data = rdata.text
    base_split = '<img src="https://i.nhentai.net/galleries/'
    # this might have errors, the reason for try except
    try:
        split_data = data.split(base_split)[1][:17]
    except Exception as e:
        print("Failed with: " + str(e))
        print("with the following data: " + str(data))
        print("link is: " + link + ", page nr is: " + page_nr)
    
    print("split_data is: ")
    print(split_data)
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
    list = []
    try:
        f = open(fpath, "r")
        basic_list = f.readlines()
        # removing \n endlines
        for element in basic_list:
            list.append(element.strip())
        print("Going to try and download the following: ")
        for x in list:
            print(x)
    except:
        print("No file was given, exiting")
        sys.exit(0)
    return list
    

def main(basic=None):
    nhlink = "https://nhentai.net/"
    # g comes from gallery, i just found out
    nhid = "g/"
    file_path = "numbahrs.txt"
    if basic is None:
        list = get_numbah_list(file_path)
    else:
        list = [basic]

    for x in list:
        get_doujin_from_id(nhlink + nhid, x)

    print("Done downloading, hopefully it worked")

            
if __name__ == "__main__":
    print("Started the nhscrapper")
    if len(sys.argv) > 1:
        print("Please do not give weird first argument")
        print("Using given argument to only get " \
            + str(sys.argv[1]))
        main(str(sys.argv[1]))
    else:
        print("Reading from file to get numbahrs")
        main()
