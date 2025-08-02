def remove_activity_function(df, activity):
    """I don't care about B.
    Remove "A -> B", "B -> C".
    Add "A ~> C"."""
    if activity in df.index:
        print(f"Remove activity '{activity}' in Matrix.")
        if activity == df.index[0] or activity == df.index[-1]:
            print(f"Activity '{activity}' is at the start or end of the Matrix, cannot remove.\n")
        else: 
            predecessorsOfActivity=[col for col in df.columns if df.at[col,activity] == '→' or df.at[col,activity] == '≺' or df.at[col,activity] == '||']
            successorsOfActivity=[col for col in df.columns if df.at[activity,col] == '→' or df.at[activity,col] == '≺' or df.at[activity,col] == '||']
            print(f"Predecessors of '{activity}': {predecessorsOfActivity}")
            print(f"Successors of '{activity}': {successorsOfActivity}")
            for predecessor in predecessorsOfActivity:
                for successor in successorsOfActivity:
                    if predecessor != successor:
                        # Add a new relationship between predecessor and successor
                        df.at[predecessor, successor] = '≺'
                        print(f"Added relationship: {predecessor} ≺ {successor}")
                        # Add the reverse relationship
                        df.at[successor, predecessor] = '≻'
            #Remove relationships involving the activity"
            for predecessor in predecessorsOfActivity:
                if predecessor in df.columns:
                    df.at[predecessor, activity] = '-'
                    print(f"Removed relationship from {predecessor} to {activity}")
                    # Also remove the reverse relationship
                    df.at[activity, predecessor] = '-'
                        
            for successor in successorsOfActivity:
                if successor in df.index:
                    df.at[activity, successor] = '-'
                    print(f"Removed relationship from {activity} to {successor}")
                    # Also remove the reverse relationship
                    df.at[successor, activity] = '-'
            
    else:
        print(f"Activity '{activity}' not found in Matrix.\n")
    
    return df