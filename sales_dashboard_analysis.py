import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

OUTPUT_DIR = "Dashboard"
IMAGES_DIR = "Images"
CSV_CANDIDATES = ["data set.csv", "data.csv", "superstore_clean.csv", "superstore.csv"]

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

sns.set(style="whitegrid")


def find_dataset():
    for candidate in CSV_CANDIDATES:
        if os.path.exists(candidate):
            print(f"Using dataset file: {candidate}")
            return candidate
    raise FileNotFoundError(
        f"Dataset not found. Place one of these files in the project root: {CSV_CANDIDATES}"
    )


def load_data(path):
    df = pd.read_csv(path, encoding='latin1', parse_dates=['Order Date', 'Ship Date'], dayfirst=False)
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.month
    df['MonthYear'] = df['Order Date'].dt.to_period('M').astype(str)
    df['Profit Margin'] = df['Profit'] / df['Sales']
    df['Profit Margin'] = df['Profit Margin'].fillna(0)
    return df


def save_plot(fig, filename):
    filepath = os.path.join(IMAGES_DIR, filename)
    fig.savefig(filepath, bbox_inches='tight', dpi=200)
    plt.close(fig)
    print(f"Saved {filepath}")


def create_plots(df):
    # Monthly sales and profit trend
    monthly = df.groupby('MonthYear').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    monthly = monthly.sort_values('MonthYear')

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(monthly['MonthYear'], monthly['Sales'], marker='o', label='Sales')
    ax.plot(monthly['MonthYear'], monthly['Profit'], marker='o', label='Profit')
    ax.set_title('Monthly Sales and Profit Trend')
    ax.set_xlabel('Month')
    ax.set_ylabel('USD')
    ax.tick_params(axis='x', rotation=45)
    ax.legend()
    save_plot(fig, 'monthly_sales_profit.png')

    # Sales and profit by region
    region = df.groupby('Region').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index().sort_values('Sales', ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=region.melt(id_vars=['Region'], value_vars=['Sales', 'Profit']), x='Region', y='value', hue='variable', ax=ax)
    ax.set_title('Sales and Profit by Region')
    ax.set_ylabel('USD')
    save_plot(fig, 'region_sales_profit.png')

    # Category profit margin
    category = df.groupby('Category').agg({'Sales': 'sum', 'Profit': 'sum'})
    category['Profit Margin'] = category['Profit'] / category['Sales']
    category = category.sort_values('Profit Margin', ascending=False).reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=category, x='Profit Margin', y='Category', palette='viridis', ax=ax)
    ax.set_title('Profit Margin by Category')
    ax.set_xlabel('Profit Margin')
    save_plot(fig, 'category_profit_margin.png')

    # Ship mode profit
    ship = df.groupby('Ship Mode').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=ship, x='Ship Mode', y='Profit', palette='mako', ax=ax)
    ax.set_title('Profit by Ship Mode')
    ax.set_ylabel('Profit')
    save_plot(fig, 'ship_mode_profit.png')

    # Segment profit margin
    segment = df.groupby('Segment').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    segment['Profit Margin'] = segment['Profit'] / segment['Sales']
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=segment, x='Profit Margin', y='Segment', palette='rocket', ax=ax)
    ax.set_title('Profit Margin by Customer Segment')
    ax.set_xlabel('Profit Margin')
    save_plot(fig, 'segment_profit_margin.png')

    # Top 10 products by profit
    product = df.groupby('Product Name').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    top_products = product.sort_values('Profit', ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(data=top_products, x='Profit', y='Product Name', palette='crest', ax=ax)
    ax.set_title('Top 10 Products by Profit')
    save_plot(fig, 'top_products_profit.png')


def write_insights(df):
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    average_discount = df['Discount'].mean()
    overall_margin = total_profit / total_sales
    top_category = df.groupby('Category')['Profit'].sum().idxmax()
    worst_category = df.groupby('Category')['Profit'].sum().idxmin()
    best_region = df.groupby('Region')['Profit'].sum().idxmax()
    worst_region = df.groupby('Region')['Profit'].sum().idxmin()

    margins = df.groupby('Category').agg({'Sales': 'sum', 'Profit': 'sum'})
    margins['Profit Margin'] = margins['Profit'] / margins['Sales']
    low_margin_category = margins['Profit Margin'].idxmin()

    report_path = os.path.join(OUTPUT_DIR, 'Business_Insights_Report.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('# Business Insights Report\n\n')
        f.write('## Summary Metrics\n')
        f.write(f'- Total sales: ${total_sales:,.2f}\n')
        f.write(f'- Total profit: ${total_profit:,.2f}\n')
        f.write(f'- Average discount: {average_discount:.2%}\n')
        f.write(f'- Overall profit margin: {overall_margin:.2%}\n\n')
        f.write('## Key Findings\n')
        f.write(f'- Highest profit category: **{top_category}**\n')
        f.write(f'- Lowest profit category: **{worst_category}**\n')
        f.write(f'- Best region for profit: **{best_region}**\n')
        f.write(f'- Worst region for profit: **{worst_region}**\n')
        f.write(f'- Category with the lowest profit margin: **{low_margin_category}**\n\n')
        f.write('## Recommendations\n')
        f.write('- Focus marketing and inventory on high-margin categories and the highest-profit region.\n')
        f.write('- Re-evaluate discounting in low-margin categories, especially the one with the weakest margin.\n')
        f.write('- Review shipping practices for ship modes with the lowest profit contribution.\n')
        f.write('- Use the monthly sales/profit trend to identify slow months and plan promotional campaigns around them.\n')
        f.write('- Highlight top-performing products in sales campaigns and protect inventory levels for those items.\n\n')
        f.write('## Dashboard Files\n')
        f.write('- `Images/monthly_sales_profit.png`\n')
        f.write('- `Images/region_sales_profit.png`\n')
        f.write('- `Images/category_profit_margin.png`\n')
        f.write('- `Images/ship_mode_profit.png`\n')
        f.write('- `Images/segment_profit_margin.png`\n')
        f.write('- `Images/top_products_profit.png`\n')

    print(f"Written {report_path}")


def main():
    csv_path = find_dataset()
    df = load_data(csv_path)
    create_plots(df)
    write_insights(df)


if __name__ == '__main__':
    main()
