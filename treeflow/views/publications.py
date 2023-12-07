from django.shortcuts import render
from treeflow.corpus.utils.zotero import request_zotero_api_for_collection

def zotero_view(request):
    # Connect to Zotero API

    collectionKeys = {
    "Preliminary Publications": "4DBIWSQG",
    "Project Publications": "B3BHZEGW",
    "Related Publications": "8VFMBB74",
    "Presentations": "YZX3G3DF",
    "Related Presentations": "2DNQXANE",
    }

    publications = {
        'group_key': 2116388,
        'collections' : []
    }
    # Get Zotero data

    for key, value in collectionKeys.items():

        zotero_data,_ = request_zotero_api_for_collection(publications["group_key"],value)
        publications["collections"].append({"name":key,"data":zotero_data})

    # Render template with Zotero data
    return render(request, 'pages/publications.html', {'publications': publications['collections']})
