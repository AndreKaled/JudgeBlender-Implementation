import json
import statistics
import random

class JudgeAggregator:
    def __init__(self, results_path):
        with open(results_path, 'r') as f:
            self.data = json.load(f)

    def average_voting(self, scores):
        return sum(scores) / len(scores)

    def majority_voting(self, scores, tie_break="avg"):
        try:
            return statistics.mode(scores)
        except statistics.StatisticsError:
            # desempate do JudgeBlender
            if tie_break == "max": return max(scores)
            if tie_break == "min": return min(scores)
            if tie_break == "avg": return sum(scores) / len(scores)
            return random.choice(scores)

    def process_all(self, method="av", tie_break="avg"):
        final_judgments = []
        for entry in self.data:
            scores = list(entry['judges'].values())
            
            if method == "av":
                final_score = self.average_voting(scores)
            else:
                final_score = self.majority_voting(scores, tie_break)
                
            final_judgments.append({
                "qid": entry['qid'],
                "docid": entry['docid'],
                "final_score": final_score
            })
        return final_judgments