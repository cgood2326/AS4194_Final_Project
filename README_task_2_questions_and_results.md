# Group Studies: Practical Programming and Data Analysis for Atmospheric Science: Final Project

## "When and where are ensemble statistics non-normal? An investigation with a 1000-member SPEEDY ensemble."

Welcome to the repository for the AU 24 ATMOSSC 4194 final project. Within this repository, there are two Python files that contain the code used to complete this project as well as two markdown files. The first markdown file contains the answers to questions posed in task #2. The second markdown file contains links to the Chat GPT transcripts. This repository has two contributors, Cole Good and Max Max Abrecht. 

## Task 2: Where & Where are Statistics Significantly Non-Normal?
__-----Question 1-----__

_For each model variable in the perturbed ensemble, how does the number of null hypothesis rejections (i.e., non-Gaussian data) vary with latitude, model level and time?_

__T variable:__
![null_hypothesis_rejections_by_time_t_perturbed_ens](https://github.com/user-attachments/assets/963ebfc4-77a9-4a9c-b815-93208b4b4a32)

For the T variable with time, there is an initial spike in rejections from the start until just after February. The lowest number of rejections occurs between February and the middle of March before settling out between 30% and 60% through November. 

![null_hypothesis_rejections_by_level_t_perturbed_ens](https://github.com/user-attachments/assets/84d310bb-25bc-4005-bc28-7d26d1af1820)

Similar to rejections with time, rejections by pressure levels spike across all pressure levels in the first month. After January, there is just under a two-month period where rejections are below 30% across all pressure levels. After March, there is an increase in rejections above 400 hPa.

![null_hypothesis_rejections_by_latitiude_t_perturbed_ens](https://github.com/user-attachments/assets/c69a458e-ace8-4c2b-b092-75a29401a2a1)

For the T variable by latitude, there is an initial period within January where there is a large percentage of rejections followed by a period from February to mid-March where rejections are at their lowest. However, a pattern forms after March where there is a high percentage of rejections over the equator.


__Q variable:__
![null_hypothesis_rejections_by_time_q_perturbed_ens](https://github.com/user-attachments/assets/180115c0-0ba3-4cc8-b9b9-7eb7c4646eb2)

For the Q variable with time, there is a high percentage of rejections in January followed by a lower percentage of rejections from February to March. Unlike the T variable, there is little to no increase in the percentage of rejections after March.

![null_hypothesis_rejections_by_level_q_perturbed_ens](https://github.com/user-attachments/assets/97d11e5d-070b-47ea-ab8b-ff641e1d13fb)

Rejections by pressure level for the Q variable shows an initial spike in the first 25 days followed by a low percentage of rejections to about 200 hPa. From day 75 onward, the percentage of rejections increases above 300 hPa.  

![null_hypothesis_rejections_by_latitiude_q_perturbed_ens](https://github.com/user-attachments/assets/26e320ae-6ef7-4ea9-a2e9-37be27c8c893)

As seen with the other variables, the rejections with latitude have the characteristic spike in the first month. This is followed by a pattern of a high percentage of rejections near the equator with a lower percentage of rejections around the middle latitudes.


__U variable:__
![null_hypothesis_rejections_by_time_u_perturbed_ens](https://github.com/user-attachments/assets/1cd88f9e-5eeb-4fae-b595-ecd1170e8fdd)

The U variable rejection by time graph is similar to the same graph for all the other variables. A high percentage of rejections in January followed a period in February to March with a lower percentage of rejections.

![null_hypothesis_rejections_by_level_u_perturbed_ens](https://github.com/user-attachments/assets/d5a0ba5a-871c-4e0c-b48f-d08ca31bfcdc)

The graph for rejections by pressure level graph for the U variable differs from the other variables after the month of March. Initially, there is a spike in rejections in January followed by a dip between February and March. After March the lowest percentage of rejections is contained mostly at pressures above 800 hPa.

![null_hypothesis_rejections_by_latitiude_u_perturbed_ens](https://github.com/user-attachments/assets/1c766cd4-52b6-4037-9e97-d278ec061a66)

The U variable’s rejection by latitude graph has three distinct regions the first occurs in January where there is a high percentage of rejections across all latitudes. The second region occurs between February and March where the percentage of rejections is below 45% across all latitudes except near the equator. The third region is a pattern that forms after March where there is an increased percentage of rejections near the equator. 


__V variable:__
![null_hypothesis_rejections_by_level_v_perturbed_ens](https://github.com/user-attachments/assets/eb0c3d3d-c427-4c08-9270-13a8aed6ad04)

The graph for rejections by pressure level for the V variable contains a spike in rejections for the month of January across all pressure levels. Between February and March, the percentage of rejections falls to 30% across all pressure levels. After March, the percentage of rejections increases as the pressure decreases.

![null_hypothesis_rejections_by_latitiude_v_perturbed_ens](https://github.com/user-attachments/assets/4894f090-af2f-4f3d-a901-abbcaafffbde)

Like the other variables, the graph for rejections by latitude sees a spike in the percentage of rejections across all latitudes in January followed by a pattern that sees a higher percentage of rejections near the equator. 

![null_hypothesis_rejections_by_time_v_perturbed_ens](https://github.com/user-attachments/assets/f5358c97-7d6d-42a9-bdb1-8b2546c98dbf)

As seen in the same graphs for the other variables, the rejections by time graph for the V variable has a spike in the number of rejections in January, a dip between February and March before settling around 50% through November.


__-----Question 2------__

_For each model variable, do the patterns in the perturbed ensemble’s null hypothesis rejections become visually indistinguishable from those of the reference ensemble? If yes, when does that happen?_

As evident by the graphs below, the trend is nearly identical for all variables. To answer this question the graphs of rejections by latitude for each variable both perturbed and reference ensembles are shown. After the month of April, the graph for the perturbed and reference ensembles for each variable becomes nearly indistinguishable.

T variable:
![null_hypothesis_rejections_by_latitiude_t_perturbed_ens](https://github.com/user-attachments/assets/c69a458e-ace8-4c2b-b092-75a29401a2a1)
![null_hypothesis_rejections_by_latitiude_t_reference_ens](https://github.com/user-attachments/assets/01dd6603-c3ec-426a-a4f0-18e52554040c)


Q variable:
![null_hypothesis_rejections_by_latitiude_q_perturbed_ens](https://github.com/user-attachments/assets/26e320ae-6ef7-4ea9-a2e9-37be27c8c893)
![null_hypothesis_rejections_by_latitiude_q_reference_ens](https://github.com/user-attachments/assets/d2c18239-44bd-4002-9be0-1b81f5242470)

U variable:
![null_hypothesis_rejections_by_latitiude_u_perturbed_ens](https://github.com/user-attachments/assets/1c766cd4-52b6-4037-9e97-d278ec061a66)
![null_hypothesis_rejections_by_latitiude_u_reference_ens](https://github.com/user-attachments/assets/faa8508f-cd4e-402e-97c0-543f52568a83)

V variable:
![null_hypothesis_rejections_by_latitiude_v_perturbed_ens](https://github.com/user-attachments/assets/4894f090-af2f-4f3d-a901-abbcaafffbde)
![null_hypothesis_rejections_by_latitiude_v_reference_ens](https://github.com/user-attachments/assets/c64e47c8-eaa3-4496-8839-5f730e1ae254)






