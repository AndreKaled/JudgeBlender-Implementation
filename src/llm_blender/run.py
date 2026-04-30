import json
from utils.injector import PromptInjector

class LLMBlender:
    def __init__(self, model_callers):
        # model_callers: {'mistral': func, 'gemma': func, 'llama': func}
        self.injector = PromptInjector()
        self.callers = model_callers

    def run_inference(self, qid, docid):
        # Gemma-7B -> Thomas Direct (Direct Grading)
        p_thomas = self.injector.format_phase1(qid, docid)['thomas']
        score_thomas = self._parse_score(self.callers['gemma'](p_thomas))

        # Mistral-7B -> Farzi (MultiCriteria)
        p_farzi = self.injector.format_phase1(qid, docid)['farzi_s1']
        farzi_scores = {}
        for criterion, prompt in p_farzi.items():
            res = self.callers['mistral'](prompt)
            farzi_scores[criterion] = self._parse_score(res)
        
        p_farzi_s2 = self.injector.format_farzi_s2(qid, docid, farzi_scores)
        score_farzi = self._parse_score(self.callers['mistral'](p_farzi_s2))

        # Llama-3-8B -> Sun et al. (Two-step)
        p_sun_s1 = self.injector.format_phase1(qid, docid)['sun_s1']
        is_relevant = self.callers['llama'](p_sun_s1).strip().lower()
        
        if "yes" in is_relevant:
            p_sun_s2 = self.injector.format_sun_s2(qid, docid)
            score_sun = self._parse_score(self.callers['llama'](p_sun_s2))
        else:
            score_sun = 0

        return {
            "qid": qid,
            "docid": docid,
            "judges": {
                "gemma_thomas": score_thomas,
                "mistral_farzi": score_farzi,
                "llama_sun": score_sun
            }
        }

    def _parse_score(self, text):
        import re
        match = re.search(r'\b[0-3]\b', text)
        return int(match.group()) if match else 0