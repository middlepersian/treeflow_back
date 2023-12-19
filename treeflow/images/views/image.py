from ..models import Image
from ..forms import ImageForm
from treeflow.corpus.models import Source
import logging
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

# Set up logging
logger = logging.getLogger(__name__)

def delete_image(request, image_id):
    logger.debug(f"Request method: {request.method}")
    logger.debug(f"Image ID: {image_id}")

    try:
        image = get_object_or_404(Image, pk=image_id)
        if request.method == "POST":
            image.delete()
            return redirect("treeflow.corpus:manuscripts")
    except Exception as e:
        logger.error(f"Error in updating image: {e}", exc_info=True)
        return JsonResponse(
            {"status": "error", "message": "An error occurred during update"}
        )
    

# a django view function to create a new image, using the ImageForm
def create_image(request):
    # using the ImageForm to create a new image
    # check if request is post
    if request.POST:
        form = ImageForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("treeflow.corpus:manuscripts")
        else:
            return JsonResponse({"status": "error", "message": "Invalid form"})
    # return render(request,"")
    # if request is not post, return the form
    else:
        form = ImageForm()
        return render(request, "image_form.html", {"form": form})


def edit_image(request, image_id):
    """
    API endpoint for updating a image's data
    """
    logger.debug(f"Request method: {request.method}")
    logger.debug(f"Image ID: {image_id}")
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

def change_source_for_image(request,image_id):
    image = get_object_or_404(Image, pk=image_id)
    if request.method == "POST":
        # get the source id from the request
        try:
            source_id = request.POST.get("source_id")
            logger.debug(f"Source ID: {source_id}")
            # get the source object
            source = Source.objects.get(pk=source_id)
            # update the image object
            image.source = source
            image.save()
            return redirect("treeflow.corpus:manuscripts")
        except Exception as e:
            logger.error(f"Error in updating image: {e}", exc_info=True)
            return JsonResponse(
                {"status": "error", "message": "An error occurred during update"}
            )
    else:
        # get all sources
        sources = Source.objects.all()
        # render the template
        return render(request, "image_source.html", {"sources": sources, "image": image})
