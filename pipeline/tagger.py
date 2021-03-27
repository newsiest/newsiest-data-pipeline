from collections import Counter
from string import punctuation

import nltk
from rake_nltk import Rake
import spacy

from models.news_article import NewsArticle
from pipeline.pipeline_stage import PipelineStage


class Tagger(PipelineStage):
    nltk.download('stopwords')
    nltk.download('punkt')
    nlp = spacy.load("en_core_web_md")
    pos_tag = ['PROPN', 'NOUN']

    def __init__(self, rake_max_length: int = 1):
        """
        Initialize Rake algorithm
        """
        super().__init__()
        self.r = Rake(max_length=rake_max_length)

    def _process_one(self, to_process: NewsArticle) -> NewsArticle:
        """
        Generate tags using the Rake algorithm and spaCy's POS extraction
        """
        text = (to_process.title + to_process.desc_title + to_process.desc_para).lower()

        # rake
        self.r.extract_keywords_from_text(text)
        rakes = self.r.get_ranked_phrases()

        # spacy
        result = []
        doc = self.nlp(text)

        for token in doc:
            if token.text in self.nlp.Defaults.stop_words or token.text in punctuation:
                continue

            if token.pos_ in self.pos_tag:
                result.append(token.text)

        spacys = [x[0] for x in Counter(result).most_common()]

        to_process.tags = list(set(rakes + spacys))

        return to_process

    def start(self):
        raise NotImplementedError
