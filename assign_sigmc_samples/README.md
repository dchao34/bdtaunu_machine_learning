Data sample assignment for signal MC
---

This is necessary since we need to distinguish, roughly, between training and testing samples for machine learning. 

Sample Key
---
The following is a mapping from the sample type to a unique integer key. 
+ exploratory sample => 1 
+ training sample => 2 
+ validation sample => 3
+ testing sample => 4 
+ unassigned => 0

Sample Proportions
---
The following are the initial proportions assigned to the various samples. 

    explore : train : validate : test : unassigned = 1 : 0.5 : 0.5 : 1 : 2
