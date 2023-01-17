import re
import pandas as pd


def get_sentences(filepath):
    data = pd.read_excel(filepath)
    data = data.groupby(['sentence'])
    return sentences


def check_field(field):
    if pd.isna(field):
        return None
    else:
        return str(field).strip()


def process_new_part(new_part):
    if pd.isna(new_part):
        return None
    else:
        new_part_raw = new_part.strip()
        new_part = new_part_raw.split('_')
        new_part_dict = {}

        # first we do process the source
        source = new_part[0]
        new_part_dict['source'] = source

        # then we iterate through the rest of the parts
        for part in new_part[1:]:
            # the we do process the section_types
            parts = re.findall(r'[A-Za-z]+|\d+', part)
            if parts[0] == 'ch':
                new_part_dict['chapter_number'] = parts[1]
            if parts[0] == 'sec':
                new_part_dict['section_number'] = parts[1]

        new_part_dict['section_identifier'] = new_part_raw
        new_part_dict['chapter_identifier'] = '_'.join(
            new_part_raw.split('_')[:-1])

        print('new_part_dict: {} '.format(new_part_dict))

        return new_part_dict


def parse_sentences(sentences):
    all_sentences = []
    for i, e in enumerate(sentences):
        translations = []
        current_sentence = e[1]
        sentence = {}
        tokens = []
        mwe = []

        for index, row in current_sentence.iterrows():

            try:
                # add sentence number
                if str(row['sentence']):
                    sentence['number'] = str(float(row['sentence'])).strip()

                # add translations
                if str(row['transcription']).startswith('#TRANSLATION'):
                    translation = {}

                    # get translations language
                    translation_desc = str(row['transcription']).split('_')
                    translation_language = translation_desc[1]
                    if translation_language == 'en':
                        translation_language = 'eng'
                    if translation_language == 'de':
                        translation_language = 'deu'

                    # set gujarati as lang if not eng or deu
                    if translation_language not in ['eng', 'deu']:
                        translation_language = 'guj'

                    translation['translation_language'] = translation_language

                    # get translations content
                    translation_content = check_field(
                        str(row['transliteration']).strip())

                    translation['translation_content'] = translation_content
                    translations.append(translation)

                # add comment
                if str(row['transcription']).startswith('#COMMENT'):
                    if check_field(row['transliteration']):
                        sentence['comment'] = str(row['transliteration']).strip()

                # "normal" tokens have a 'transcription' and a 'lemma'
                if check_field(row['transcription']) and check_field(row['lemma']):
                    token = {}
                    if check_field(row['transcription']):
                        token['transcription'] = check_field(row['transcription'])
                    if check_field(row['transliteration']):
                        token['transliteration'] = check_field(
                            row['transliteration'])
                    if check_field(row['folioNew']):
                        token['folio'] = check_field(row['folioNew'])
                    if check_field(row['line']):
                        token['line'] = check_field(float(row['line']))
                    if check_field(row['lemma']):
                        token['lemma'] = check_field(row['lemma'])
                    if check_field(row['meaning']):
                        token['meaning'] = check_field(row['meaning'])
                    if check_field(row['POSTag']):
                        pos = check_field(row['POSTag'])
                    if check_field(row['POSTFeatures']):
                        if [check_field(x) for x in check_field(row['POSTFeatures']).split('|') if x != '_']:
                            token['morphological_annotation'] = [check_field(x) for x in check_field(
                                row['POSTFeatures']).split('|')]  # morphological_annotations
                    if check_field(row['uncertain']):
                        token['uncertain'] = [check_field(x) for x in check_field(
                            row['uncertain']).split(',')]
                    if check_field(row['new_suggestion']):
                        token['new_suggestion'] = [check_field(x) for x in check_field(
                            row['new_suggestion']).split(',')]
                    if check_field(row['discussion']):
                        token['to_discuss'] = [check_field(x) for x in check_field(
                            row['discussion']).split(',')]
                    if check_field(row['comment']):
                        token['comment'] = check_field(row['comment'])
                    if check_field(row['newPart']):
                        token['new_part'] = process_new_part(row['newPart'])
                    tokens.append(token)

                    # "multi-word" expressions have no tokens assigned, but do appear in the "lemma" field
                if row['transcription'] is np.nan and row['lemma'] is not np.nan:
                    #print(row['sentence'], row['lemma'])
                    local_mwe = {}
                    local_mwe['mwe_lemma'] = str(row['lemma']).strip()
                    local_mwe['mwe_meaning'] = str(row['meaning']).strip()
                    mwe.append(local_mwe)

            except Exception as e:
                print(e)
                print(row)

        sentence['tokens'] = tokens
        sentence['mwe'] = mwe
        sentence['translations'] = translations
        all_sentences.append(sentence)

    return all_sentences
