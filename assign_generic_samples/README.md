Data sample assignment for generic MC
---

Sample Key
---
The following is a mapping from the sample type to a unique integer key. 
+ exploratory sample => 1 
+ training sample => 2 
+ validation sample => 3
+ testing sample => 4 
+ data emulation sample => 5
+ KDE sample => 6

Sample Proportions
---
+ 2% of all generic monte carlo is assigned to each of `explore`, `train`, `validate`, and `test` samples. 
+ The `data emulation` sample is obtained by weighted undersampling of all generic modes such that the obtained sample has, approximately, the correct proportion as well as the size of the real data. 
+ Data records that were not assigned to any of the previous samples are assigned to the `KDE sample`. 
