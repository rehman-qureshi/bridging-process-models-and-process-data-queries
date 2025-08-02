# ≺ equal to ~> 
# ≻ equal to <~
def path_exists(df, from_activity, to_activity):
    """
    Check if there is a path from from_activity to to_activity following '→' or '≺'  or '||' in the Matrix.
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

 
def add_true_exclusion_relationships_function(df):
    
    for activity in df.index:
        for other_activity in df.columns:
            if not (df.at[activity, other_activity] == '→' or df.at[activity, other_activity] == '≺' or df.at[activity, other_activity] == '||'): 
                    # Check if a path exists from activity to other_activity
                    if activity==other_activity:
                        df.at[activity, other_activity] = '#'
                    elif not path_exists(df, activity, other_activity):   # check if there is no path from activity to other_activity             
                        if not path_exists(df, other_activity,activity): # also check if there is no path from other_activity to activity
                            # If no path exists both way, add a true exclusion relationship
                            df.at[activity, other_activity] = '#'
                            

    # Return the modified DataFrame with true exclusion relationships added
    return df