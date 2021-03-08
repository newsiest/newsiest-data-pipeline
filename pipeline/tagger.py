import nltk
from rake_nltk import Rake

from pipeline.pipeline_stage import PipelineStage


class Tagger(PipelineStage):

    def __init__(self):
        super().__init__()
        nltk.download('stopwords')
        nltk.download('punkt')
        self.r = Rake(min_length=1, max_length=2)

    def _process_one(self, to_process):
        self.r.extract_keywords_from_text(to_process.title)
        to_process.tags = self.r.get_ranked_phrases()

    def start(self):
        pass
