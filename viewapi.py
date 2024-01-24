class output:
    def display_shortlist(self, match_list):
        print(f"\nFirst shortlist: {match_list}")

    def display_final_list(self, resume_scores):
        print('\nFinal list:')
        results = []
        for filename, score in sorted(resume_scores.items(), key=lambda x: x[1], reverse=True):
                if score * 100 > 1:
                    result = {'filename': filename, 'match_percentage': score * 100}
                    results.append(result)
        print(results)
        return results
