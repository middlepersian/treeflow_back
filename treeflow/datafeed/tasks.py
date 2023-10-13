from django.core.cache import cache 
from celery import shared_task
import asyncio
import logging
from treeflow.schema import schema
from strawberry import relay
from treeflow.corpus.models.text import Text as TextModel
from treeflow.corpus.types.text import Text as TextType

logger = logging.getLogger(__name__)

#execute the query
async def execute_query(query):
    return await schema.execute(query)

#clear the cache
@shared_task
def clear_cache():
    logger.info("Starting to clear the cache.")
    cache.clear()
    logger.info("Cache cleared.")
    return "Cache cleared."

def get_texts_query():
    query = """
    query TextsQuery {
        texts {
            edges {
                node {
                    id
                    label
                    title
                    stage
                    version
                    identifier
                    sources {
                        id
                        identifier
                    }
                    series
                }
            }
            totalCount
        }
    }
    """
    return query

def get_sections_list_query(text_id):
    query = f"""
    query SectionsListQuery {{
        sectionsList(filters: {{ type: "sentence", text: {{ id: "{text_id}" }} }}) {{
            id
            identifier
            title
            type
            number
            resolveTokens {{
                id
                transcription
                number
            }}
        }}
    }}
    """
    return query

def get_all_sections_lists():
    # Fetch all text IDs from the database
    text_ids = TextModel.objects.values_list('id', flat=True)

    # Iterate over each text ID and execute the GraphQL query
    for text_id in text_ids:
        #convert id into relay global id
        text_id = relay.to_base64(TextType, text_id)
        query = get_sections_list_query(text_id)
        #execute the query
        try:
            result = asyncio.run(execute_query(query))
        except Exception as e:
            logger.error(f"An error occurred while executing the query: {e}")
            raise Exception("get_all_sections_lists failed") from e

@shared_task
def clear_and_warm_up_cache():
    logger.info("Starting to clear and warm up the cache.")
    
    # Clear the cache
    cache.clear()
    logger.info("Cache cleared.")

    # get all texts
    query = get_texts_query()
    # Execute the query
    try:
        result = asyncio.run(execute_query(query))
    except Exception as e:
        logger.error(f"An error occurred while executing the query: {e}")
        raise Exception("clear_and_warm_up_cache failed") from e

    # get all sections lists
    query = get_all_sections_lists()    
    # Execute the query
    try:
        result = asyncio.run(execute_query(query))
    except Exception as e:
        logger.error(f"An error occurred while executing the query: {e}")
        raise Exception("clear_and_warm_up_cache failed") from e

    logger.info("Cache cleared and warmed up.")    