import os
from bs4 import BeautifulSoup
from django.conf import settings
from django.shortcuts import render
import logging
logger = logging.getLogger(__name__)


def kosh_view(request):

    return render(request, 'pages/kosh.html')
