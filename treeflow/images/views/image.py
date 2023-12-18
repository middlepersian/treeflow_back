from ..models import Image
from ..forms import ImageForm
import logging
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Set up logging
logger = logging.getLogger(__name__)

# a django view function to create a new image, using the ImageForm
def create_image(request):
    ...

def edit_image(request, image_id):
    """
    API endpoint for updating a image's data
    """
    logger.debug(f"Request method: {request.method}")
    logger.debug(f"Source ID: {image_id}")
    try:
        image = get_object_or_404(Image, pk=image_id)

        if request.method == "POST":
            # Handling other fields
            #
            for field in ["identifier", "page", "number"]:
                if field in request.POST:
                    logger.info(f"Updating {field} for image with ID {image_id}")
                    setattr(image, field, request.POST[field])
                    image.save(update_fields=[field])
                    return JsonResponse(
                        {
                            "status": "success",
                            "message": f"{field} updated successfully",
                        }
                    )
                else:
                    logger.info(
                        f"Field {field} not provided in POST data for image ID {image_id}"
                    )

            # If no recognized fields are found
            logger.warning(
                f"No matching field found in POST data for image ID {image_id}"
            )
            return JsonResponse(
                {"status": "error", "message": "No matching field found"}
            )

        else:
            logger.warning(f"Received a non-POST request for image ID {image_id}")
            return JsonResponse({"status": "error", "message": "Invalid request"})

    except Exception as e:
        logger.error(f"Error in updating image: {e}", exc_info=True)
        return JsonResponse(
            {"status": "error", "message": "An error occurred during update"}
        )
