import logging
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from treeflow.corpus.models import Source

# Set up logging
logger = logging.getLogger(__name__)


def update_source(request, source_id):
    """
    API endpoint for updating a source's data
    """
    logger.debug(f"Request method: {request.method}")
    logger.debug(f"Source ID: {source_id}")
    try:
        token = get_object_or_404(Source, pk=source_id)

        if request.method == "POST":
            # TODO : Sources
            # TODO : BibEntry
            # Handling other fields
            for field in ["identifier", "description", "type"]:
                if field in request.POST:
                    logger.info(f"Updating {field} for token with ID {source_id}")
                    setattr(token, field, request.POST[field])
                    token.save(update_fields=[field])
                    return JsonResponse(
                        {
                            "status": "success",
                            "message": f"{field} updated successfully",
                        }
                    )
                else:
                    logger.info(
                        f"Field {field} not provided in POST data for source ID {source_id}"
                    )

            # If no recognized fields are found
            logger.warning(
                f"No matching field found in POST data for source ID {source_id}"
            )
            return JsonResponse(
                {"status": "error", "message": "No matching field found"}
            )

        else:
            logger.warning(f"Received a non-POST request for source ID {source_id}")
            return JsonResponse({"status": "error", "message": "Invalid request"})

    except Exception as e:
        logger.error(f"Error in updating source: {e}", exc_info=True)
        return JsonResponse(
            {"status": "error", "message": "An error occurred during update"}
        )
