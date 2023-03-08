import pandas as pd
from treeflow.images.models import Image

def map_folio_to_page(csv_file, source_id):

    """Map folio to page.

    Args:

        csv_file (str): Path to csv file.

        folio (str): Folio.

        page (str): Page.

    Returns:

        None

    """
    df = pd.read_csv(csv_file, sep='\t', encoding='utf-8')
    for index, row in df.iterrows():
        if row['folio_id']:
            print(row['folio_id'], row['page_number'])

            #call the image in db
            #update the page_number
            img_obj = Image.objects.get(identifier=str(source_id + '_' + str(row['folio_id'])))
 

                

 