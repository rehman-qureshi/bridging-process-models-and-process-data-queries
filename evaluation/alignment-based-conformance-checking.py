import pm4py
from pm4py.objects.bpmn.importer import importer as bpmn_importer
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.conformance.alignments.petri_net import algorithm as align_algorithm
from pm4py.objects.conversion.bpmn import converter as bpmn_converter
from pm4py.algo.filtering.log.attributes import attributes_filter
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.visualization.petri_net import visualizer as pn_visualizer

# 1. Load BPMN model and convert to Petri net
bpmn_path = "3-way Match, Invoice before Goods Receipt - Standard and Framework Orders.bpmn"
bpmn_model = bpmn_importer.apply(bpmn_path)
net, initial_marking, final_marking = bpmn_converter.apply(bpmn_model)

# Workflow Net
# Visualize the net
gviz = pn_visualizer.apply(net, initial_marking, final_marking)
pn_visualizer.save(gviz,"BPIC19.png")  # Save as PNG image

# 2. Load the event log
log_path = "BPIC19_3way_IbeforeGR_standardPO_complete.xes"
log = xes_importer.apply(log_path)

# (Optional) Filter out non-model activities from the log

model_activities = [a.name for a in bpmn_model.get_nodes() if hasattr(a, 'name')]
alignments = align_algorithm.apply_log(log, net, initial_marking, final_marking)

# 4. Inspect results
total_violations = 0
total_affected_traces = 0
total_conform_traces=0
avg_fitness = 0.0
listOfAffectedTraces=[]
listOfConformTraces=[] 
for idx, alignment in enumerate(alignments):
    trace = [event["concept:name"] for event in log[idx]]
    affectedTrace=False
    for step in alignment["alignment"]:
        if '>>' in step and step[1] is not None:  # exclude ('>>', None)
            total_violations += 1
            affectedTrace=True
        elif step[0] is not None and step[1] == '>>':  # exclude (None,'>>')
            total_violations += 1
            affectedTrace=True
    if affectedTrace:
        total_affected_traces +=1
        listOfAffectedTraces.append(trace)       
    else:
        total_conform_traces+=1
        listOfConformTraces.append(trace)

print(f"Total number of violations (excluding silent transitions): {total_violations}")
print(f"Total number of traces: {len(alignments)}")
print(f"Total number of affected traces: {total_affected_traces}")
print(f"Total number of conformed traces: {total_conform_traces}")
print(f"GLobal trace fitness: {total_conform_traces / len(alignments)}")
print(f"Length of conform traces:",len(listOfConformTraces))
print(f"Length of affected traces:",len(listOfAffectedTraces))
