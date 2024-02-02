

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

        sorted_data = {}
        ranking = 1

        for filename, entry in sorted(data.items(), key=lambda x: x[1]["score"], reverse=True):

            file_path = entry['filepath'] # Access filepath
            
            sorted_data[f"rank {ranking}"] = {
                    "filename": filename,
                    "Url": file_path, # Add to output
                    "score": entry["score"]
            }

            ranking += 1

        # Print output with filepath  
        for rank, entry in sorted_data.items():
            print(f"{rank} - {entry['filename']} - {entry['Url']} - {entry['score']}") 
        print(sorted_data)
        return sorted_data

            
