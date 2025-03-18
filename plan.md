# Plan for Visualizing Quarter Theory on GBPJPY Chart

**Goal:** Create a Python script that fetches GBPJPY price data, calculates Quarter Theory levels, and visualizes them on a Matplotlib chart.

**Plan:**

1.  **Analyze `app.py`:**
    *   Use `read_file` to re-examine the `app.py` file to pinpoint the exact lines of code where the GBPJPY chart is created. This is crucial for inserting the Quarter Theory visualization code in the correct location.

2.  **Implement Quarter Theory Calculation and Overlay:**
    *   Within the GBPJPY chart creation block, add code to:
        *   Calculate the nearest .250 price level to the current GBPJPY price.  I will assume the current price is the last closing price in the dataframe.
        *   Calculate the Quarter Theory levels (.250 above and below the nearest .250 level).
        *   Overlay the Quarter Theory levels as horizontal lines on the chart using `ax_gbpjpy.axhline()`.
        *   Ensure the lines are visually distinct (e.g., different colors, line styles).

3.  **Error Handling and Comments:**
    *   Add comments to explain the Quarter Theory calculation and overlay logic.
    *   Implement basic error handling (e.g., check if the GBPJPY data is available before performing calculations).

4.  **Refactor and Optimize:**
    *   Refactor the code for readability and maintainability.
    *   Optimize the Quarter Theory calculation for performance (if necessary).

5.  **Testing:**
    *   Run the `app.py` script to verify that the Quarter Theory levels are correctly displayed on the GBPJPY chart.

6.  **Apply Changes:**
    *   Use `apply_diff` to apply the changes to `app.py`.

**Mermaid Diagram:**

```mermaid
graph LR
    A[Re-examine app.py] --> B[Implement Quarter Theory Calculation];
    B --> C[Overlay Quarter Theory Levels on Chart];
    C --> D[Add Comments and Error Handling];
    D --> E[Refactor and Optimize];
    E --> F[Testing];
    F --> G[Apply Changes with apply_diff];