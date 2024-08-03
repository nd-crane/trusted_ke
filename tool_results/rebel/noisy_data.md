**REBEL's Sensitivity to Noise**

REBEL is very sensitive to noise; for example, adding blank spaces or characters like `'` can provide different outputs. See the example:

1. **Original Text with Extra Spaces:**
    ```
    "AFTER TAKEOFF, ENGINE QUIT. WING FUEL TANK SUMPS WERE NOT DRAINED DURING PREFLIGHT BECAUSE THEY WERE FROZEN.  "
    ```
    Output:
    ```
    ['<s><triplet> TAKEOFF <subj> FROZEN <obj> has cause <triplet> FROZEN <subj> TAKEOFF <obj> has effect</s>']
    ```

2. **Original Text:**
    ```
    "AFTER TAKEOFF, ENGINE QUIT. WING FUEL TANK SUMPS WERE NOT DRAINED DURING PREFLIGHT BECAUSE THEY WERE FROZEN."
    ```
    Output:
    ```
    ['<s><triplet> FUEL TANK <subj> ENGINE <obj> subclass of</s>']
    ```

3. **Text with Multiple Spaces at the End:**
    ```
    'AFTER TAKEOFF, ENGINE QUIT. WING FUEL TANK SUMPS WERE NOT DRAINED DURING PREFLIGHT BECAUSE THEY WERE FROZEN.       '
    ```
    Output:
    ```
    ['<s><triplet> TAKEOFF <subj> FROZEN <obj> has effect <triplet> FROZEN <subj> TAKEOFF <obj> has cause</s>']
    ```

4. **Text with a Leading Apostrophe:**
    ```
    "'AFTER TAKEOFF, ENGINE QUIT. WING FUEL TANK SUMPS WERE NOT DRAINED DURING PREFLIGHT BECAUSE THEY WERE FROZEN."
    ```
    Output:
    ```
    ['<s><triplet> WING FUEL TANK <subj> FROZEN <obj> has part <triplet> FROZEN <subj> WING FUEL TANK <obj> part of</s>']
    ```

5. **Text with Leading and Trailing Apostrophes:**
    ```
    "'AFTER TAKEOFF, ENGINE QUIT. WING FUEL TANK SUMPS WERE NOT DRAINED DURING PREFLIGHT BECAUSE THEY WERE FROZEN.'"
    ```
    Output:
    ```
    ['<s><triplet> FUEL <subj> TANK <obj> part of <triplet> TANK <subj> FUEL <obj> has part</s>']
    ```

6. **Text with Lowercase 'a' in 'AFTER':**
    ```
    aFTER TAKEOFF, ENGINE QUIT. WING FUEL TANK SUMPS WERE NOT DRAINED DURING PREFLIGHT BECAUSE THEY WERE FROZEN.
    ```
    Output:
    ```
    ['<s><triplet> FUEL <subj> TANK <obj> part of <triplet> TANK <subj> FUEL <obj> has part</s>']
    ```

7. **Text with Lowercase 'after':**
    ```
    after TAKEOFF, ENGINE QUIT. WING FUEL TANK SUMPS WERE NOT DRAINED DURING PREFLIGHT BECAUSE THEY WERE FROZEN.
    ```
    Output:
    ```
    ['<s><triplet> TAKEOFF <subj> FROZEN <obj> significant event</s>']
    ```
