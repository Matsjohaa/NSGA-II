# NSGA-II
NSGA2 implementation of the ZDT1 problem

	•	Objectives:

$$
f_1(x) = x_1
$$

$$
f_2(x) = g(x) \cdot \left(1 - \sqrt{\frac{f_1(x)}{g(x)}}\right)
$$

where

$$
g(x) = 1 + \frac{9}{n-1} \sum_{i=2}^n x_i
$$

Pareto front:

$$
{ (f_1, f_2) \mid f_1 \in [0,1], ; f_2 = 1 - \sqrt{f_1} }
$$
