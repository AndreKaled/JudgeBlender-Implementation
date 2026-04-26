import json
import os

class PromptInjector:
    def __init__(self, data_dir="data", prompts_dir="prompts"):
        self.data_dir = data_dir
        self.prompts_dir = prompts_dir
        self.queries = self._load_queries()
        self.docstore = self._load_docs()
        self.templates = self._load_templates()

    def _load_queries(self):
        path = os.path.join(self.data_dir, "llm4eval_query_2024.txt")
        return {line.split('\t')[0]: line.split('\t')[1].strip() for line in open(path, 'r')}

    def _load_docs(self):
        path = os.path.join(self.data_dir, "llm4eval_document_2024.jsonl")
        docs = {}
        for line in open(path, 'r'):
            data = json.loads(line)
            did, txt = data.get('docid'), data.get('doc')
            if did and txt:
                docs[did] = txt
        return docs

    def _load_templates(self):
        names = [
            'thomas_direct', 'farzi_criteria_step1', 'farzi_criteria_step2',
            'sun_binary_step1', 'sun_permutation_step2'
        ]
        return {name: open(f"{self.prompts_dir}/{name}.txt").read() for name in names}

    def get_texts(self, qid, docid):
        return self.queries.get(qid), self.docstore.get(docid)

    def format_phase1(self, qid, docid):
        q_text, p_text = self.get_texts(qid, docid)
        if not q_text or not p_text: return None

        criteria = {
            "Exactness": "How precisely does the passage answer the query.",
            "Coverage": "How much of the passage is dedicated to discussing the query.",
            "Topicality": "Is the passage about the same subject as the whole query.",
            "Contextual Fit": "Does the passage provide relevant background or context."
        }

        return {
            'thomas': self.templates['thomas_direct'].format(
                query=q_text, description=q_text, narrative=q_text, page_text=p_text
            ),
            'farzi_s1': {name: self.templates['farzi_criteria_step1'].format(
                criterion=name, criterion_description=desc, query=q_text, passage=p_text
            ) for name, desc in criteria.items()},
            'sun_s1': self.templates['sun_binary_step1'].format(query=q_text, passage=p_text)
        }

    def format_farzi_s2(self, qid, docid, scores):
        # scores deve ser um dict: {'Exactness': 2, 'Topicality': 3, ...}
        q_text, p_text = self.get_texts(qid, docid)
        return self.templates['farzi_criteria_step2'].format(
            query=q_text,
            passage=p_text,
            exactness_score=scores.get('Exactness'),
            topicality_score=scores.get('Topicality'),
            coverage_score=scores.get('Coverage'),
            contextual_fit_score=scores.get('Contextual Fit')
        )

    def format_sun_s2(self, qid, docid):
        q_text, p_text = self.get_texts(qid, docid)
        return self.templates['sun_permutation_step2'].format(query=q_text, passage=p_text)