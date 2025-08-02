def relationship_exists(df, from_activity, to_activity):
    """
    Check if a direct relationship exists between two activities in the Matrix.
    """
    if from_activity in df.columns and to_activity in df.index:
        return df.at[from_activity, to_activity] == '→' or df.at[from_activity, to_activity] == '||'
    else:
        print(f"Activities '{from_activity}' or '{to_activity}' not found in Matrix.\n")
        return False

def remove_direct_relationship_function(df, from_activity, to_activity):
    """
    Remove a direct relationship between two activities in the Matrix.
    """
    if from_activity in df.columns and to_activity in df.index:
            # Check if a path exists from from_activity to to_activity
            if not relationship_exists(df, from_activity, to_activity):
                print(f"No direct relationship from {from_activity} to {to_activity}.\n")
                return df
            # If a path exists, remove the relationship
            print(f"Removing relationship from {from_activity} to {to_activity}.")
            #print(f"Predecessors of '{from_activity}': {predecessorsOfFromActivtiy}")
            successorOfToActivity = [row for row in df.index if (df.at[to_activity, row] == '→' or df.at[to_activity, row] == '||')]
            print(f"Successors of '{to_activity}': {successorOfToActivity}")
            for successor in successorOfToActivity:
                    df.at[from_activity, successor] = '≺'
                    print(f"Added indirect relationship: {to_activity} ≺ {successor}")
                    # Also remove the reverse relationship
                    df.at[successor, from_activity] = '≻'
                    # Add direct from successor to to_activity
                    if (from_activity!=to_activity):  # skip if both activities are the same
                        df.at[successor, to_activity] = '||'
                        print(f"Added direct relationship: {successor} -> {to_activity}")
                        # Also remove the reverse relationship
                        df.at[to_activity, successor] = '||'
            # Turn directly relationship into indirectly relationship from from_activity to to_activity
            df.at[from_activity, to_activity] = '≺'
            # Also remove the reverse relationship if both activities are different
            if to_activity!= from_activity:
                df.at[to_activity, from_activity] = '≻'
            print(f"Removed a direct relationship: {from_activity} -> {to_activity} and added indirect relationship: {from_activity} ≺ {to_activity}")
        #else:
            #print(f"Cannot remove relationship from {from_activity} to itself.")
    else:
        print(f"Activities '{from_activity}' or '{to_activity}' not found in Matrix.")
    return df