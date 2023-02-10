

@pytest.mark.django_db
def parse_preannotated(sentences, text_object=None):

    set_of_values = [None, '', '_', np.nan]

    token_number = 1
    current_newpart = None
    newparts = {}
    newpart_number = 0
    sentence_id = ""
    for sentence in sentences:

        # initialize sections
        # sentence section
        sentence_section_type = SectionTypeFactory(identifier="sentence")
        # line section
        line_section_type = SectionTypeFactory(identifier="line")
        # chapter section
        chapter_section_type = SectionTypeFactory(identifier="chapter")
        # section
        section_section_type = SectionTypeFactory(identifier="section")

        for i, row in sentence.iterrows():
            token_id = row["id"]

            #check if token_id starts with #
            if str(token_id).strip().startswith("#"):
                if str(token_id).startswith("#SENTENCE_ID"):
                    sentence_id = str(token_id).split(" = ")[1]
                    assert sentence_id != ""
                elif str(token_id).startswith("#SENTENCE_TEXT"):
                    sentence_text = str(token_id).split(" = ")[1]
                    assert sentence_text != ""
                continue

            # assert token_id not empty
            assert token_id != ""
            # transcription
            transcription = row["transcription"]
            # assert transcription not empty
            assert transcription != ""
            # transliteration
            transliteration = row["transliteration"]
            # assert transliteration not empty
            assert transliteration != ""

            # create token

            token = TokenFactory(text=text_object, token_number=token_number)
            # create token transcription
            token.transcription = transcription
            token.transliteration = transliteration

            token_number += 1

            # postag
            postag = row["postag"]
            if postag != '_':
                postag = postag
            else:
                postag = None

            # postfeatures
            postfeatures = str(row["postfeatures"]).strip()
            postfeatures_to_add = []
            if postfeatures != '_':
                # create postfeatures (MorphologicalAnnotation)
                morpho_syntax = PostFeatureFactory()
                if '|' in postfeatures:
                    # split postfeatures
                    postfeatures = postfeatures.split("|")
                    # sub split postfeatures
                    for postfeature in postfeatures:
                        postfeature = postfeature.split("=")
                        if len(postfeature) == 2:
                            feature = postfeature[0]
                            value = postfeature[1]
                            # create postfeature
                            postfeature = PostFeatureFactory(
                                feature=feature, value=value)
                            postfeatures_to_add.append(postfeature)
                    else:
                        postfeatures = None

            # add postfeatures to token
            if postfeatures_to_add:
                token.morphological_annotation.add(*postfeatures_to_add)
            print("transcription {} - postfeatures: {}".format(transcription, postfeatures))

            # if there is a newpart, add it to the newparts dictionary
            if row["newpart"] == row["newpart"]:
                # check if newpart is not a digit or a _
                if str(row["newpart"]).strip():
                    # check if not _ or digit
                    if str(row["newpart"]).strip() != "_":
                        if not str(row["newpart"]).strip().replace('.', '').isdigit():
                            print("newpart: {} - sentence #{}".format(row["newpart"], sentence_id))

                newpart = str(row["newpart"])
                if newpart.strip() not in ["_", ""]:
                    current_newpart = newpart
                    token_newpart = current_newpart
                    newpart_number += 1
                    newparts[newpart_number] = token_newpart
            assert current_newpart != ""

    print("Number of tokens: {}".format(token_number))
    print("Number of newparts: {}".format(newpart_number))
