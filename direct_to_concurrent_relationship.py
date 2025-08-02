def direct_to_concurrent_relationship_function(df,from_activity,to_activity):
    # Change relationship from '→' to '||'
    if from_activity in df.columns and to_activity in df.index:
        if to_activity != from_activity:
            if df.at[from_activity, to_activity] == '→':

                # Find predecessors of from_activity and successors of to_activity
                predecessorsOfFromActivity=[col for col in df.columns if df.at[col,from_activity] == '→' or df.at[col,from_activity] == '≺' or df.at[col,from_activity] == '||']
                successorsOfToActivity=[col for col in df.columns if df.at[to_activity,col] == '→' or df.at[to_activity,col] == '≺' or df.at[to_activity,col] == '||']
                print(f"Predecessors of '{from_activity}': {predecessorsOfFromActivity}")
                print(f"Successors of '{to_activity}': {successorsOfToActivity}")
                if len(predecessorsOfFromActivity) > 0:     
                    for predecessor in predecessorsOfFromActivity:
                        df.at[predecessor, to_activity] = '→'
                        print(f"Added relationship: {predecessor} → {to_activity}")
                        # Also add the reverse relationship
                        df.at[to_activity, predecessor] = '←'
                else:
                    print(f"No predecessors found for '{from_activity}'.")

                if len(successorsOfToActivity) > 0:
                    for successor in successorsOfToActivity:
                        df.at[from_activity, successor] = '→'
                        print(f"Added relationship: {from_activity} → {successor}")
                        # Also add the reverse relationship
                        df.at[successor, from_activity] = '←'
                else:
                    print(f"No successors found for '{to_activity}'.")
                # Change the relationship from direct (→) to concurrent (||)
                df.at[from_activity, to_activity] = '||'
                #Also change the reverse relationship
                df.at[to_activity, from_activity] = '||'
                print(f"Changed relationship from {from_activity} → {to_activity} to {from_activity} || {to_activity}\n")
            else:
                print(f"No direct relationship from {from_activity} to {to_activity} to change.\n")                        
        else:
                print(f"Same activities detected. No change made.\n")
    else:
        print("Invalid activities provided.\n")

    return df