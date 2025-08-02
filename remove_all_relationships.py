def path_exists(df, from_activity, to_activity):
    """
    Check if there is a path from from_activity to to_activity following '→' or '≺' in the Matrix.
    """
    visited = set()
    stack = [from_activity]
    while stack:
        current = stack.pop()
        if current == to_activity:
            return True
        visited.add(current)
        for col in df.columns:
            if (df.at[current, col] == '→' or df.at[current, col] == '≺' or df.at[current,col]=='||') and col not in visited:
                stack.append(col)
    return False
        
def remove_all_relationships_function(df, from_activity,to_activity):
    """
    Remove all relationships from a specific activity to another in the Matrix.
    """
    if from_activity in df.columns and to_activity in df.index:
        if from_activity != to_activity:
            # Check if a path exists from from_activity to to_activity
            if not path_exists(df, from_activity, to_activity):
                print(f"No path exists from {from_activity} to {to_activity}.\n")
                return df
            # If a path exists, remove all relationships along the path
            successorOfToActivity = [row for row in df.index if (df.at[to_activity, row] == '→' or df.at[to_activity, row] == '||' )]
            print(f"Successors of '{to_activity}': {successorOfToActivity}")
            predecessorsOfToActivity = [col for col in df.columns if (df.at[col, to_activity] == '→' or df.at[col, to_activity] == '||')]
            print(f"Predecessors of '{to_activity}': {predecessorsOfToActivity}")
            # Check if the direct arc exist or not
            if df.at[from_activity, to_activity] == '→' or df.at[from_activity, to_activity] == '≺' or df.at[from_activity, to_activity] == '||':
                print(f"Found direct arc between {from_activity} and {to_activity}.")
                 
                for successor in successorOfToActivity:
                    if successor != from_activity:
                        # Check if already exist direct relationship, then do not do anything
                            df.at[from_activity, successor] = '≺'
                            print(f"Added indirect relationship: {from_activity} ≺ {successor}")
                            # Also add the reverse relationship
                            df.at[successor, from_activity] = '≻'
                
                # Remove the path between from_activity and to_activity
                df.at[from_activity, to_activity] = '-'
                df.at[to_activity,from_activity] = '-'
                
                
            else:
                print(f"No direct arc found between {from_activity} and {to_activity}.")
                # Add precedessors of to_activty to successors of to_activity
                for predecessor in predecessorsOfToActivity:
                    # check if the predecessor has concurrent relationship with to activtiy
                    if df.at[predecessor,to_activity]=='||':
                        otherSuccessorsOfPredecessor=[row for row in df.index if (df.at[predecessor, row] == '→')]
                        for othersuccessor in otherSuccessorsOfPredecessor:
                            df.at[predecessor, othersuccessor] = '≺'
                            print(f"Added indirect relationship: {predecessor} ≺ {othersuccessor}")
                            # Also add the reverse relationship
                            df.at[othersuccessor,predecessor] = '≻'
                        print(f"Added direct relationship: {to_activity} → {predecessor}")
                        df.at[to_activity,predecessor]='→'
                        df.at[predecessor,to_activity]='←'
                    else:
                        df.at[predecessor, to_activity] = '-'
                        df.at[to_activity, predecessor] = '-'
                        print(f"Removed relationship: {predecessor} -> {to_activity}")
                        for successor in successorOfToActivity:
                            if predecessor != successor:
                                df.at[predecessor, successor] = '≺'
                                print(f"Added indirect relationship: {predecessor} ≺ {successor}")
                                # Also add the reverse relationship
                                df.at[successor, predecessor] = '≻'
                
        else:
            print(f"Cannot remove relationship from {from_activity} to itself.")
            
    else:
        print(f"Activities '{from_activity}' or '{to_activity}' not found in Matrix.")
    
    return df