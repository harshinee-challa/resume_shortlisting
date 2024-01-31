

class output:
    def display_shortlist(self, match_list):
        print(f"\nFirst shortlist")
        print(match_list)
        # return {"message":match_list}

    def secondlist(self,resume_scores):
        print(f"\nsecond shortlist")
        print(resume_scores)
        # return {"message":resume_scores.keys()}
    
    def display_final_list(self, data):
        print('\nFinal Shortlist:')
        
        sorted_data = {filename: {"filename": filename, "score": entry["score"]} for filename, entry in sorted(data.items(), key=lambda x: x[1]["score"], reverse=True)}
        print(sorted_data)
        return sorted_data

            
