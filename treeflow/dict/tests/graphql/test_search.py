import json
import pytest
from treeflow.users.models import User
from treeflow.dict.models import Lemma, Meaning 
from treeflow.dict.types import Lemma as LemmaType
from treeflow.dict.types import Meaning as MeaningType
from strawberry_django.test.client import TestClient
from strawberry import relay
