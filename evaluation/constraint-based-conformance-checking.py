import pm4py
from pm4py.objects.bpmn.importer import importer as bpmn_importer
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.conformance.alignments.petri_net import algorithm as align_algorithm
from pm4py.objects.conversion.bpmn import converter as bpmn_converter
from pm4py.algo.filtering.log.attributes import attributes_filter

#-------------------------------------------------------
def chain_response(trace,A,B):
    isTraceAffected=False
    violations_in_trace=0
    for i in range(len(trace)):
            
            #if trace[i] in A:
            if trace[i] == A:
                #total_A_occurrences += 1

                # Check if next event exists and is in B
                if i + 1 >= len(trace) or trace[i + 1] not in B:
                    violations_in_trace += 1
                    #total_violations += 1

            if violations_in_trace > 0:
                isTraceAffected=True
    
    return isTraceAffected
#---------------------------------------------------------------
def alternate_response(trace,A,B):
    violations_in_trace = 0
    isTraceAffected=False
    i = 0
    while i < len(trace):
        if trace[i] == A:
        
        #if trace[i] in A:
            #total_A_occurrences += 1
            found_B = False
            j = i + 1
            while j < len(trace):
                if trace[j] in B:
                    found_B = True
                    break
                elif trace[j] == A:
                    break  # next A found before B → violation
                j += 1
            if not found_B:
                violations_in_trace += 1
            i = j  # continue from where we left off
        else:
            i += 1

    # if there are violations, then the trace is being affected        
    if violations_in_trace > 0:
            isTraceAffected=True
    
    return isTraceAffected
#--------------------------------------------------------------------
def not_cooccurance(trace,A,B):
    
    violations_in_trace=0
    isTraceAffected=False
    if A == B:
            # Violation if the same activity occurs more than once
            violations_in_trace = 1 if trace.count(A) > 1 else 0
    else:
        # Violation if both A and B occur together
        violations_in_trace = 1 if (A in trace and B in trace) else 0

    if violations_in_trace > 0:
            isTraceAffected=True
    return isTraceAffected
#-------------------------------------------------------------
def init_violation(trace, A):

    violations_in_trace=0
    isTraceAffected=False
    
    if not trace or trace[0] not in A:
        violations_in_trace += 1
        isTraceAffected=True
        #print(trace)

    return isTraceAffected
#-----------------------------------------------------------
def end_violation(trace, A):
 
    
    violations_in_trace=0
    isTraceAffected=False
    
    if not trace or trace[-1] not in A:
        violations_in_trace += 1
        isTraceAffected=True
        

    return isTraceAffected
#--------------------- Main Function -----------------------
if __name__ == "__main__":
    
    # 1. Load the event log
    log_path = "BPIC19_3way_IbeforeGR_standardPO_complete.xes"
    log = xes_importer.apply(log_path)

    # No Relaxation
    #ChainResponse(ROC, {RGR, RIR, VCI, CQ})
    #ChainResponse(CP, {RGR, RIR, VCI, CQ})
    #ChainResponse(RGR, {RPB, RIR, VCI, CI})
    #ChainResponse(VCI, {RPB, RGR, RIR, CQ, CI})
    #ChainResponse(CPOI, {ROC, RGR, RIR, CQ, VCI, CP})
    #ChainResponse(CPRI, {CPOI})
    #ChainResponse(CQ, {RGR, RIR, VCI})
    #ChainResponse(RPB, {CI})
    #ChainResponse(RIR, {RPB, RGR, VCI, CI})
    #NotCooccurance(CI, CI)
    #NotCooccurance(RPB, RPB)
    #NotCooccurance(RGR, RGR)
    #NotCooccurance(CPOI, CPOI)
    #NotCooccurance(RIR, RIR)
    #NotCooccurance(ROC, ROC)
    #NotCooccurance(CP, CP)
    #NotCooccurance(CPRI, CPRI)
    #NotCooccurance(VCI, VCI)
    #NotCooccurance(CQ, CQ)
    #NotCooccurance(ROC, CP)
    """constraints = [
    {"type": "ChainResponse", "A": "ROC", "B": ["RGR", "RIR", "VCI", "CQ"]},
    {"type": "ChainResponse", "A": "CP", "B": ["RGR", "RIR", "VCI", "CQ"]},
    {"type": "ChainResponse", "A": "RGR", "B": ["RPB", "RIR", "VCI", "CI"]},
    {"type": "ChainResponse", "A": "VCI", "B": ["RPB", "RGR", "RIR", "CQ", "CI"]},
    {"type": "ChainResponse", "A": "CPOI", "B": ["ROC", "RGR", "RIR", "CQ", "VCI", "CP"]},
    {"type": "ChainResponse", "A": "CPRI", "B": ["CPOI"]},
    {"type": "ChainResponse", "A": "CQ", "B": ["RGR", "RIR", "VCI"]},
    {"type": "ChainResponse", "A": "RPB", "B": ["CI"]},
    {"type": "ChainResponse", "A": "RIR", "B": ["RPB", "RGR", "VCI", "CI"]},
    {"type": "NotCooccurance", "A": "CI", "B": "CI"},
    {"type": "NotCooccurance", "A": "RPB", "B": "RPB"},
    {"type": "NotCooccurance", "A": "RGR", "B": "RGR"},
    {"type": "NotCooccurance", "A": "CPOI", "B": "CPOI"},
    {"type": "NotCooccurance", "A": "RIR", "B": "RIR"},
    {"type": "NotCooccurance", "A": "ROC", "B": "ROC"},
    {"type": "NotCooccurance", "A": "CP", "B": "CP"},
    {"type": "NotCooccurance", "A": "CPRI", "B": "CPRI"},
    {"type": "NotCooccurance", "A": "VCI", "B": "VCI"},
    {"type": "NotCooccurance", "A": "CQ", "B": "CQ"},
    {"type": "NotCooccurance", "A": "ROC", "B": "CP"},
]"""
    
    #After relaxation

    constraints = [
    {"type": "ChainResponse", "A": "Change Quantity", "B": ["Vendor creates invoice", "Record Goods Receipt", "Record Invoice Receipt"]},
    {"type": "ChainResponse", "A": "Create Purchase Requisition Item", "B": ["Create Purchase Order Item"]},
    {"type": "ChainResponse", "A": "Remove Payment Block", "B": ["Clear Invoice"]},
    {"type": "AlternateResponse", "A": "Record Goods Receipt", "B": ["Vendor creates invoice", "Remove Payment Block", "Record Goods Receipt", "Clear Invoice"]},
    {"type": "AlternateResponse", "A": "Record Invoice Receipt", "B": ["Vendor creates invoice", "Record Invoice Receipt", "Remove Payment Block", "Record Goods Receipt", "Clear Invoice"]},
    {"type": "AlternateResponse", "A": "Create Purchase Order Item", "B": ["Vendor creates invoice", "Record Goods Receipt", "Record Invoice Receipt"]},
    {"type": "AlternateResponse", "A": "Receive Order Confirmation", "B": ["Vendor creates invoice", "Record Goods Receipt", "Record Invoice Receipt"]},
    {"type": "AlternateResponse", "A": "Vendor creates invoice", "B": ["Remove Payment Block", "Clear Invoice"]},
    {"type": "AlternateResponse", "A": "Change Price", "B": ["Vendor creates invoice", "Record Goods Receipt", "Record Invoice Receipt"]},
    {"type": "NotCooccurance", "A": "Change Quantity", "B": "Change Quantity"},
    {"type": "NotCooccurance", "A": "Clear Invoice", "B": "Clear Invoice"},
    {"type": "NotCooccurance", "A": "Receive Order Confirmation", "B": "Change Price"},
    {"type": "NotCooccurance", "A": "Create Purchase Requisition Item", "B": "Create Purchase Requisition Item"},
    {"type": "NotCooccurance", "A": "Vendor creates invoice", "B": "Vendor creates invoice"},
    {"type": "NotCooccurance", "A": "Create Purchase Order Item", "B": "Create Purchase Order Item"},
    {"type": "NotCooccurance", "A": "Change Price", "B": "Change Price"},
    {"type": "NotCooccurance", "A": "Receive Order Confirmation", "B": "Receive Order Confirmation"},
    {"type": "NotCooccurance", "A": "Remove Payment Block", "B": "Remove Payment Block"},
    # Init Constraint
    {"type": "Init", "A": ["Create Purchase Requisition Item","Create Purchase Order Item"], "B": ""},
    # End Constraint
    {"type": "End", "A": ["Clear Invoice"], "B": ""}
]

    chain_response_violations=0
    alternate_response_violations=0
    not_cooccurance_volations=0
    listOfConformTraces=[]
    listOfAfftectedTraces=[]
    for trace_idx, trace in enumerate(log):
        trace = [event["concept:name"] for event in log[trace_idx]]
        #trace=["Create Purchase Order Item","Record Goods Receipt","Vendor creates invoice","Change Quantity","Record Invoice Receipt","Clear Invoice"]
        violations_in_trace = 0
        isTraceAffected=False
        for constraint in constraints:
            constraint_type = constraint["type"]
            A = constraint["A"]
            B = constraint["B"]
            if constraint_type=="ChainResponse":
                isTraceAffected=chain_response(trace,A,B)
                if isTraceAffected==True:
                    listOfAfftectedTraces.append(trace)
                    chain_response_violations+=1
                    break
            elif constraint_type=="AlternateResponse":
                isTraceAffected=alternate_response(trace,A,B)
                if isTraceAffected==True:
                    alternate_response_violations+=1
                    listOfAfftectedTraces.append(trace)
                    break
            elif constraint_type=="NotCooccurance":
                isTraceAffected=not_cooccurance(trace,A,B)
                if isTraceAffected==True:
                    not_cooccurance_volations+=1
                    listOfAfftectedTraces.append(trace)
                    break
            elif constraint_type=="Init":
                isTraceAffected=init_violation(trace,A)
                if isTraceAffected==True:
                    listOfAfftectedTraces.append(trace)
                    break
            elif constraint_type=="End":
                isTraceAffected=end_violation(trace,A)
                if isTraceAffected==True:
                    listOfAfftectedTraces.append(trace)
                    break

        if isTraceAffected==False:
            listOfConformTraces.append(trace)
        
    print(f"Length of listOfConformTraces: ",len(listOfConformTraces))
    print(f"Length of listOfAfftectedTraces: ",len(listOfAfftectedTraces))
    print(f"chain_response_violations: {chain_response_violations}")    
    print(f"alternate_response_violations: {alternate_response_violations}")
    print(f"not_cooccurance_volations: {not_cooccurance_volations}")
    