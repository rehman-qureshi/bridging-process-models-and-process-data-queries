def exclusive_to_direct_relationship_function(df, from_activity, to_activity):
    
    if from_activity in df.columns and to_activity in df.index:
                if to_activity != from_activity:
                    if df.at[from_activity, to_activity] == '#':
                        df.at[from_activity, to_activity] = '→'
                        print(f"Changed relationship from {from_activity} - {to_activity} to {from_activity} → {to_activity}\n")
                        # Also change the reverse relationship
                        df.at[to_activity, from_activity] = '←'
                    else:
                        print(f"No exclusive relationship from {from_activity} to {to_activity} to change.\n")
                else:
                    print(f"Same activities detected. No change made.\n")
    else:
        print("Invalid activities provided.\n")
    
    return df