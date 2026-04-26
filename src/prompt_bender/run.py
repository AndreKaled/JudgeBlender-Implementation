import json
from utils.injector import PromptInjector

class PromptBlender:
    def __init__(self, model_caller):
        # model_caller: função que recebe o prompt e retorna a string de saida do modelo
        self.injector = PromptInjector()
        self.model_caller = model_caller

    def run_inference(self, qid, docid):
        # Thomas, Farzi (4 critérios) e Sun (Binary)
        p1 = self.injector.format_phase1(qid, docid)
        
        # Thomas Direct (0-3)
        score_thomas = self._parse_score(self.model_caller(p1['thomas']))

        # Farzi Step 1 (4 Critérios)
        farzi_scores = {}
        for criterion, prompt in p1['farzi_s1'].items():
            res = self.model_caller(prompt)
            farzi_scores[criterion] = self._parse_score(res)
        
        # Farzi Step 2: Injeção dos scores da S1 na S2
        p_farzi_s2 = self.injector.format_farzi_s2(qid, docid, farzi_scores)
        score_farzi = self._parse_score(self.model_caller(p_farzi_s2))

        # 3. Sun Binary (Yes/No)
        is_relevant = self.model_caller(p1['sun_s1']).strip().lower()
        
        if "yes" in is_relevant:
            # Sun Step 2: Pontuação 1-3
            p_sun_s2 = self.injector.format_sun_s2(qid, docid)
            score_sun = self._parse_score(self.model_caller(p_sun_s2))
        else:
            score_sun = 0

        return {
            "qid": qid,
            "docid": docid,
            "judges": {
                "thomas": score_thomas,
                "farzi": score_farzi,
                "sun": score_sun
            }
        }

    def _parse_score(self, text):
        # pega apenas o primeiro número (0-3)
        import re
        match = re.search(r'\b[0-3]\b', text)
        return int(match.group()) if match else 0