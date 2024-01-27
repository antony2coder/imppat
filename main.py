import requests
from bs4 import BeautifulSoup
import os

# Step 1: Scrape the website for plant names and save to a file
def scrape_website(url, class_name):
    """the function is used to the extract the all plant name in the imppat database, it will pass the two arrgument one is home url for the imppat and the particular class name of the html code , because the hoem website contain the many option tag so we can get only a plant name"""
    try:
        # the code for the request the url
        response = requests.get(url)

        if response.status_code == 200:
            # the connection will be get first get the all html code
            soup = BeautifulSoup(response.text, 'html.parser')
            #the line will be for the find the particular class name
            select_tag = soup.find('select', class_=class_name)

            if select_tag:
                # we get the that class find the option tag contain the plant name , the plant name was return by thr function
                option_texts = [option.get_text(strip=True) for option in select_tag.find_all('option')]
                return option_texts
            else:
                #no class in the html
                print(f"No <select> tag with class '{class_name}' found on the website.")
                return None
        else:
            #any problem in website
            print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
            return None

    except Exception as e:
        #given url will be mistake
        print(f"An error occurred while processing {url}: {str(e)}")
        return None

#define the base url and the class name
website_url = "https://cb.imsc.res.in/imppat/"
select_class_name = "homeselect"

#to call the function and the plant name was save into the variable
option_texts = scrape_website(website_url, select_class_name)

if option_texts:
    # to store the plant name into the list
    combined_options = []

    # to print the plant name in the console
    for text in option_texts:
        print(text)
        combined_options.append(text + "\n")

   # the output file name , don't change the name it will take the next program input
    output_file_path = "plant_name.txt"
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.writelines(combined_options)

    print(f"Options saved to {output_file_path}")
else:
    print("No option texts found within the specified <select> class on the website.")

# Step 2: Replace spaces with '%20' in the generated plant names file
#to declare the input and output file into the variable name
input_file_path = "plant_name.txt"
output_file_path = "after_plant.txt"

#open the input file and read the content
with open(input_file_path, "r", encoding="utf-8") as input_file:
    content = input_file.read()

#the imppat will replace the space to the %20
modified_content = content.replace(" ", "%20")

#the modified data will be save into the  output file
with open(output_file_path, "w", encoding="utf-8") as output_file:
    output_file.write(modified_content)

print(f"Spaces replaced with '%20'. Output saved to {output_file_path}")

# Step 3: Generate URLs from plant names and save to a file
#define the input and output file into the variable name
input_file_path = 'after_plant.txt'
output_file_path = 'plant_name_link.txt'

with open(input_file_path, 'r') as file:
    lines = file.readlines()

#the base url for the all plant and the empty list
base_url = "https://cb.imsc.res.in/imppat/phytochemical/"
urls = []

for line in lines:
    plant_name = line.strip()
    if plant_name:
        url = base_url + plant_name
        urls.append(url)

with open(output_file_path, 'w') as output_file:
    for url in urls:
        output_file.write(url + '\n')

print(f"Generated URLs saved to '{output_file_path}'")

#Step 4: Scrape the compound information from the generated URLs
#Define a function to scrape and extract data from a website
def scrape_website(url):
    """the function for the extract the imppat id for the all plant"""
    try:
        # Send an HTTP GET request to the website
        response = requests.get(url)

        # Check if the response was successful
        if response.status_code == 200:
            # Parse the HTML content of the website
            soup = BeautifulSoup(response.text, 'html.parser')

            # to find the IMPHY word its unique for the all compound in database
            specific_word = 'IMPHY'
            specific_a_tags = soup.find_all('a', string=lambda s: specific_word.lower() in s.lower() if s else False)

            return specific_a_tags
        else:
            print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
            return None

    except Exception as e:
        print(f"An error occurred while processing {url}: {str(e)}")
        return None

# to declare the input file
input_file_path = 'plant_name_link.txt'

# Read the content from the input file
with open(input_file_path, 'r') as file:
    links = file.readlines()


for link in links:

    single_link = link.strip()


    specific_a_tags = scrape_website(single_link)

    if specific_a_tags:

        output_file_path = "compound.txt"
        with open(output_file_path, "a", encoding="utf-8") as output_file:
            for tag in specific_a_tags:
                output_file.write(tag.get_text(strip=True) + "\n")
        print(f"Output appended to {output_file_path}")
    else:
        print(f"No specific <a> tags found for {single_link}.")

# Step 5: Generate URLs from compound names and save to a file
input_file_path = 'compound.txt'
output_file_path = 'compound_link.txt'

with open(input_file_path, 'r') as file:
    compound_names = file.readlines()

base_url = "https://cb.imsc.res.in/imppat/images/2D/SDF/"
urls = []

for compound_name in compound_names:
    compound_id = compound_name.strip()
    if compound_id:
        url = base_url + compound_id + ".sdf"
        urls.append(url)

with open(output_file_path, 'w') as output_file:
    for url in urls:
        output_file.write(url + '\n')

print(f"Generated URLs saved to '{output_file_path}'")

# Step 6: Download compounds and save to a folder
input_file_path = "compound_link.txt"
output_folder = "compounds"
os.makedirs(output_folder, exist_ok=True)

with open(input_file_path) as file:
    for line in file:
        url = line.strip()
        if url:
            filename = os.path.join(output_folder, os.path.basename(url))
            response = requests.get(url)

            if response.status_code == 200:
                with open(filename, "wb") as output_file:
                    output_file.write(response.content)
                print(f"Downloaded: {url}")
            else:
                print(f"Failed to download: {url} (Status code: {response.status_code})")
