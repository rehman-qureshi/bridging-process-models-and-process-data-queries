import csv
from itertools import product
def isOptionalActivity(activity,df):
    predecessorsOfActivity = [col for col in df.columns if (df.at[col, activity] == '→' or df.at[col, activity] == '||' or df.at[col, activity] == '≺')]
    successorOfActivity=[row for row in df.index if (df.at[activity, row] == '→' or df.at[activity, row] == '||' or df.at[activity, row] == '≺')]
    # All possible pairs (first from predecessors, second from successors)
    all_pairs = list(product(predecessorsOfActivity, successorOfActivity))
    isOptionalFlag=False

    for pair in all_pairs:
        if pair[0] in df.columns and pair[1] in df.index:
            if df.at[activity,pair[0]]!='||' and df.at[pair[1],activity]!='||' and df.at[pair[1],pair[0]]!='||': 
                if df.at[pair[0],pair[1]]=='→':
                    isOptionalFlag=True  
                       
                 
    return isOptionalFlag

def generate_declarative_constraints_function(df):
    directlyFollowsSet = set()
    eventuallyFollowsSet = set()
    exclusiveSet = set()
    declarativeConstraints=[]
    # Iterate through the DataFrame to find relations
    for i in df.index:
        for j in df.columns:
            if df.at[i, j] == '→' or df.at[i, j] == '||':
                directlyFollowsSet.add((i, j))
            elif df.at[i, j] == '≺':
                eventuallyFollowsSet.add((i, j))
                #directlyFollowsSet.add((i, j))
            elif df.at[i, j] == '#':
                if (i, j) not in exclusiveSet and (j, i) not in exclusiveSet:
                    # Ensure that the exclusive relationship is only added once
                    exclusiveSet.add((i, j))
    print("Generating binary constraints...")    
    # Get unique source activities for directly follows         
    firstElementMatchingDF=set()
    for tuple in directlyFollowsSet:
        findSimilarFirstElement = {t[1] for t in directlyFollowsSet if t[0] == tuple[0]}
        firstElementMatchingDF.add((tuple[0], frozenset(findSimilarFirstElement)))  
    for value in firstElementMatchingDF:
        formatted_elements = ", ".join(value[1])  # Convert frozenset to a comma-separated string
        constraint=f"ChainResponse({value[0]}, {{{formatted_elements}}})"
        declarativeConstraints.append(constraint)
        fs=value[1] # It is frozenset
        all_pairs = list(product(fs, fs))
        
        for pair in all_pairs:
            if pair[0] in df.columns and pair[1] in df.index:
                if df.at[pair[0],pair[1]]=='||' and df.at[pair[1],pair[0]]=='||':
                    
                    pairFirstValueFlag=isOptionalActivity(pair[0],df)
                    
                    if pairFirstValueFlag==False and df.at[value[0],pair[0]]!='||':
                        constraint=f"AlternateResponse({value[0]},{pair[0]})"
                             
                        if constraint not in declarativeConstraints:
                            declarativeConstraints.append(constraint) 
                    
                    
                    pairSecondValueFlag=isOptionalActivity(pair[1],df,directlyFollowsSet)
                    if pairSecondValueFlag==False and df.at[value[0],pair[1]]!='||':
                        constraint=f"AlternateResponse({value[0]},{pair[1]})"     
                        if constraint not in declarativeConstraints:
                            declarativeConstraints.append(constraint)
                    
        #declarativeConstraints.append(constraint)
    
    # Get unique source activities for eventually follows
    firstElementMatchingEF=set()
    for tuple in eventuallyFollowsSet:
        findSimilarFirstElement = {t[1] for t in eventuallyFollowsSet if t[0] == tuple[0]}
        firstElementMatchingEF.add((tuple[0], frozenset(findSimilarFirstElement)))  
    for value in firstElementMatchingEF:
        formatted_elements = ", ".join(value[1])  # Convert frozenset to a comma-separated string
        constraint=f"AlternateResponse({value[0]}, {{{formatted_elements}}})"
        declarativeConstraints.append(constraint)
   
   # Process exclusive relationships
    for tuple in exclusiveSet:
        constraint=f"NotCooccurance({tuple[0]}, {tuple[1]})"
        declarativeConstraints.append(constraint)

    print("Declarative Constraints generated:")

    for constraint in declarativeConstraints:
        print(constraint)
    # Save declarativeConstraints to a CSV file
    with open("output\\declarative-constraints.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Declarative Constraints"])  # Header row

        # Write rows for each constraint 
        for constraint in declarativeConstraints:
            writer.writerow([constraint])

    print("Declarative Constraints saved to 'output\\declarative-constraints.csv'")

    
