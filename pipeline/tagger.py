from collections import Counter
from string import punctuation

from rake_nltk import Rake
import spacy

from pipeline.pipeline_stage import PipelineStage


class Tagger(PipelineStage):

    def __init__(self):
        super().__init__()
        self.nlp = spacy.load("en_core_web_md")
        self.pos_tag = ['PROPN', 'NOUN']

        self.r = Rake(max_length=1)

    def _process_one(self, to_process):
        text = (to_process.title + to_process.desc).lower()

        # rake
        self.r.extract_keywords_from_text(text)
        rakes = set(self.r.get_ranked_phrases())

        # spacy
        result = []
        doc = self.nlp(text)

        for token in doc:
            if token.text in self.nlp.Defaults.stop_words or token.text in punctuation:
                continue

            if token.pos_ in self.pos_tag:
                result.append(token.text)

        spacys = [x[0] for x in Counter(result).most_common()]

        # print(to_process.title, rakes, spacys)
        # print(to_process.title, list(rakes.intersection(spacys)))

    def start(self):
        pass
