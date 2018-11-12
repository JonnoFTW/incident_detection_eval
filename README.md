# Automatic Incident Detection via Anomalies

This projects runs several anomaly detection methods
and checks if those anomalies align with real world
incident data for select locations in the Adelaide Metro area.

## Methods

Currently we only test two methods:

1. HTM: Hierarchical Temporal Memory, implemented by nupic
2. SHESD: Twitter's anomaly detection method "Seasonal Hybrid Extreme Studentized Deviate Test"

## Process
Essentially, we calculate anonamalies using each method for each datapoint
at at each strategic input of each intersection.

These anomalies are then compared to real world incident data to
determine the confusion matrix of each algorithm.
 
```
for intersection in intersections:
    for si in intersection.strategic_inputs:
        for datatype in vs,sm:
            for method in htm, shesd:
                anomalies = find_anomalies(intersection.name, si, datatype, method)
                store_anomalies(anomalies, intersection.name, si, datatype, method)
                
for method in htm, shesd:
    confusion_matrix = {
        m: {'tp':0, 'fp':0, 'tn':0, 'fn':0} for m in 'vs','sm'
    }
    for incident in incidents:
        for datatype in vs, sm:
            # fetch anomalies, if any near the incident within 15minutes
            anomalies = fetch_anomalies_near(incident.position, method, datatype)  
            update_confusion_matrix(readings, datatype)
    print(confusion_matrix)
```