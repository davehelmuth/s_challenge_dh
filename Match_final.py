# This time, I am going to use a scoring algorithm
import re
import json

def remove_ambiguity(strtext):
    # Make everything lowercase
    strtext = strtext.lower()

    # come up with a standard separator (use dash - as the standard separator)
    strtext = str(strtext).replace(" ", "-")
    strtext = strtext.replace("_", "-")
    strtext = strtext.lower()

    return strtext

def main():
    fileHandlerProducts = open("/Users/david/Desktop/Sortable Software Challenge/products.txt", 'r')
    fileHandlerListings = open("/Users/david/Desktop/Sortable Software Challenge/listings.txt", 'r')

    # read file line by line, since it's jason format seems to be broken according to online jason checker
    lstProducts = fileHandlerProducts.readlines()

    # read file line by line, since it's jason format seems to be broken according to online jason checker
    lstListings = fileHandlerListings.readlines()

    fileHandlerProducts.close()
    fileHandlerListings.close()

    # Each Product must be placed into a dictionary
    dicProducts = {}

    # Loop through each Product and then place field into it's appropriate location in the dictionary.
    intRowCounter = 0
    for strProduct in lstProducts:

        # Only take products where all fields are present (this line checks for labels)
        if strProduct.find("product_name") > -1 and strProduct.find("manufacturer") > -1 and strProduct.find("model") > -1 \
                and strProduct.find("family") > -1:

            # Split each product line into it's separate fields (each field holds the label and the data)
            lstProduct_fields = re.split(r'","', strProduct)

            for strField in lstProduct_fields:

                # Parse the field, so that the label and data are stored into their own separate variables
                lstLabel_and_Field = re.split(r'":"', strField)

                # Determine what label we are looking at, and then place the appropriate data into it's home in dictionary
                if lstLabel_and_Field[0].find("product_name") > -1:
                    strProduct_name = lstLabel_and_Field[1]
                elif lstLabel_and_Field[0].find("manufacturer") > -1:
                    strManufacturer = lstLabel_and_Field[1]
                elif lstLabel_and_Field[0].find("model") > -1:
                    strModel = lstLabel_and_Field[1]
                elif lstLabel_and_Field[0].find("family") > -1:
                    strFamily = lstLabel_and_Field[1]
                elif lstLabel_and_Field[0].find("announced-date") > -1:
                    strAnnounced_Date = lstLabel_and_Field[1].translate(None, '"}\n')
                elif lstLabel_and_Field[0].find("announced-date") == -1:
                    strAnnounced_Date = "N/A"

                # Clear for the next time
                lstLabel_and_Field = []

            # Add to dictionary
            dicProducts[intRowCounter] = {'product_name': strProduct_name, 'manufacturer': strManufacturer,
                                          'model': strModel, 'family': strFamily,
                                          'announced-date': strAnnounced_Date}

            intRowCounter += 1

            lstProduct_fields = []

    # Each listing must be placed into a dictionary
    dicListings = {}

    intRowCounter = 0
    # Loop through each Listing and then place into it's appropriate location in the dictionary
    for strListing in lstListings:

        # Only take listings where all fields are present (this line checks for labels)
        if strListing.find("title") > -1 and strListing.find("manufacturer") > -1 and strListing.find("currency") > -1 and \
                        strListing.find("price") > -1:

            # Split each listing into its separate fields (each field holds the label and the data)
            lstListing_fields = re.split(r'","', strListing)

            for strField in lstListing_fields:

                # Parse the field, so that the label and data are stored into their own separate variables
                lstLabel_and_Field = re.split(r'":"', strField)

                # Determine what label we are looking at, and then place the appropriate data into it's home in dictionary
                if lstLabel_and_Field[0].find("title") > -1:
                    strTitle = lstLabel_and_Field[1]
                elif lstLabel_and_Field[0].find("manufacturer") > -1:
                    strManufacturer = lstLabel_and_Field[1]
                elif lstLabel_and_Field[0].find("currency") > -1:
                    strCurrency = lstLabel_and_Field[1]
                elif lstLabel_and_Field[0].find("price") > -1:
                    strPrice = lstLabel_and_Field[1].translate(None, '"}\n')

                # Clear for the next time
                lstLabel_and_Field = []

            # Add to dictionary
            dicListings[intRowCounter] = {'title': strTitle, 'manufacturer': strManufacturer,
                                          'currency': strCurrency, 'price': strPrice}
            intRowCounter += 1

            lstProduct_fields = []


    '''
    Two things really matter to determine if there is a match
    1) The manufacturer in both the product and listing match
    2) The model # provided in the product can be found in the title of the listing as a substring 
    
    Problems:
    Some listings have two model numbers in the title description. For example, a battery pack has it's model number and the
    model number of what it fits too.
    
    Possible Solution:
    Doesn't seem that a 2nd model number is ever found in the beginning of the text. Therefore, only check 1st half of the
    text for the model number
    '''

    '''
    for intRowCounter in dicProducts:
        print dicProducts[intRowCounter]['product_name']
    '''

    dicResult = {}
    dicResults = {}
    lstList_of_matches= []
    # Component B of flowchart
    for product_number in dicProducts:

        # Component C of flowchart
        dicResult['product'] = dicProducts[product_number]

        # Component D of the flowchart
        for listings_number in dicListings:

            # Component E of the flowchart
            if str(dicListings[listings_number]['manufacturer']).find(str(dicProducts[product_number]['manufacturer'])) > -1:

                # Component F of the flowchart...
                # Some listings have 2 model numbers, where the 1st model number should be the correct one

                # Step 1) Grab the 1st half of the text, hopefully will leave out the second model number
                strTitle_1st_half = str(dicListings[listings_number]['title'])
                strTitle_1st_half = strTitle_1st_half[: len(strTitle_1st_half) / 2]

                #Remove ambiguity
                strTitle_1st_half = remove_ambiguity(strTitle_1st_half)
                strProducts_model = remove_ambiguity(dicProducts[product_number]['model'])
                strListings_title = remove_ambiguity(dicListings[listings_number]['title'])
                strProducts_family = remove_ambiguity(dicProducts[product_number]['family'])


                # Step 2) Search strTitle_1st_half for our model number (With ambiguity removed)
                if strTitle_1st_half.find(strProducts_model) > -1 & strListings_title.find(strProducts_family) > -1:

                    # Component G of flowchart
                    lstList_of_matches.append(dicListings[listings_number])

        # Component H of flowchart
        dicResult['listing'] = lstList_of_matches

        # Copy Result into final storage dictionary
        dicResults[product_number] = dicResult.copy()

        # Clean house
        dicResult.clear()
        lstList_of_matches = []

    # Convert to json format
    output_for_file = json.dumps(dicResults)

    # print dicResults[3]

    with open("/Users/david/Desktop/Sortable Software Challenge/output.txt", "w") as f:
        f.write(output_for_file)

if __name__ == "__main__":
    main()


# Test output here
# http://jsonlint.com