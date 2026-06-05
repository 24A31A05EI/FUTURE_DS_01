# Power BI Dashboard Instructions

This guide helps you turn the generated analysis into an interactive Power BI dashboard. Building this dashboard is also valuable for a data analytics or data science internship portfolio, because it demonstrates reporting, business insights, and visualization skills.

1. Install Power BI Desktop (Windows) from Microsoft Store or the Power BI website.

2. Open Power BI Desktop and click `Get data` → `Text/CSV`.

3. Select `superstore_clean.csv` from the project root and click `Load`.

4. In Power Query Editor (if opened):
   - Ensure `Order Date` and `Ship Date` are Date/Time types.
   - Make sure `Sales`, `Profit`, `Discount`, and `Quantity` are numeric.
   - Click `Close & Apply`.

5. Build these visuals on the `Report` canvas:
   - Card visuals: `Total Sales`, `Total Profit`, `Average Discount`, `Overall Profit Margin`.
   - Line chart: `MonthYear` (axis) vs `Sales` and `Profit` (values) — set `MonthYear` to categorical or use a proper date hierarchy.
   - Bar chart: `Region` vs `Sales` and `Profit` (use clustered bar or stacked as preferred).
   - Bar chart: `Category` sorted by `Profit Margin`.
   - Table: `Top 10 Products` by `Profit` (use Top N filter on the product table)
   - Slicer: `Year`, `Region`, `Segment` (to make dashboard interactive).

6. Formatting tips:
   - Use consistent color palette for categories and regions.
   - Add titles and axis labels. Set data labels for cards and top product chart.
   - Add a text box with the recommendations from `Dashboard/Business_Insights_Report.md`.

7. Save the report as `Superstore_Analytics.pbix`.

8. (Optional) Publish to `app.powerbi.com` if you have a Power BI account and want to share it.

If you want, I can create a step-by-step recorded script or generate a PBIX template (requires Power BI Desktop installed locally).