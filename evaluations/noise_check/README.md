# Noise Sensitivity Evaluation

**This experiment is in-progress and was not finished at time of publication**


We test not only the performance of the KE tools, but their sensitivity to extraneous noise in the data. This is an important step in our process, since maintenance data will often include added noise such as extra spaces or characters due to a lack of proofreading or peculiarities of the system the logs are saved to.

We select 20 entries from our data and add the following variations:
| Column Name | Example |
|-------------------------------|-------------------------------|
| c119 | "BATTERY COMPARTMENT DOOR CAME OPEN. ANTENNA CRACKED WINDSHIELD.                                                    " |
| c119_strip | "BATTERY COMPARTMENT DOOR CAME OPEN. ANTENNA CRACKED WINDSHIELD." |
| c119_spaceafter | "BATTERY COMPARTMENT DOOR CAME OPEN. ANTENNA CRACKED WINDSHIELD.                                                        " |
| c119_leadapost | "'BATTERY COMPARTMENT DOOR CAME OPEN. ANTENNA CRACKED WINDSHIELD.                                                    " |
| c119_leadtrailapost | "'BATTERY COMPARTMENT DOOR CAME OPEN. ANTENNA CRACKED WINDSHIELD.                                                    '" |
| c119_lowerletter | "bATTERY COMPARTMENT DOOR CAME OPEN. ANTENNA CRACKED WINDSHIELD.                                                    " |
| c119_lowerword | "battery COMPARTMENT DOOR CAME OPEN. ANTENNA CRACKED WINDSHIELD.                                                    " |
| c119_lower | "battery compartment door came open. antenna cracked windshield.                                                    " |

This data is saved to sampled_noisy.csv in this folder.

We then run sammpled_noisy.csv through each tool and save the results to noisy_results.

See diff.csv in each folder for a summary of differences. Blank entries show that the output for the noisy data is the same as the original data.