#!/usr/bin/env python3
"""
Test script to verify merchant name formatting works correctly.
"""

# Test the merchant name post-processing function
def test_merchant_formatting():
    # Simulate the post-processing logic from ai_agent.py
    def post_process_merchant_names(result):
        if not result.get("success") or not result.get("data"):
            return result

        data = result["data"]
        columns = result.get("columns", [])

        # Check if we have merchant-related columns
        merchant_columns = []
        for col in columns:
            col_lower = col.lower()
            if 'merchant' in col_lower or col == 'merchant_id':
                merchant_columns.append(col)

        if not merchant_columns:
            return result

        # Process each row to format merchant names
        formatted_data = []
        for row in data:
            formatted_row = {}
            for col in columns:
                value = row.get(col)
                if col in merchant_columns and value and isinstance(value, str):
                    # Format merchant name by replacing underscores with spaces
                    # and applying title case
                    formatted_name = value.replace('_', ' ').title()
                    formatted_row[col] = formatted_name
                else:
                    formatted_row[col] = value
            formatted_data.append(formatted_row)

        # Update column names if needed
        updated_columns = []
        for col in columns:
            if col == 'merchant_id' and any(row.get(col) for row in data):
                # Rename merchant_id to merchant_name for better display
                updated_columns.append('merchant_name')
            else:
                updated_columns.append(col)

        result["data"] = formatted_data
        result["columns"] = updated_columns

        return result

    # Test data - simulate the corrected post-processing logic
    def post_process_merchant_names(result):
        if not result.get("success") or not result.get("data"):
            return result

        data = result["data"]
        columns = result.get("columns", [])

        # Check if we have merchant-related columns
        merchant_columns = []
        for col in columns:
            col_lower = col.lower()
            if 'merchant' in col_lower or col == 'merchant_id':
                merchant_columns.append(col)

        if not merchant_columns:
            return result

        # Process each row to format merchant names
        formatted_data = []
        column_mapping = {}  # Track old -> new column names

        for row in data:
            formatted_row = {}
            for col in columns:
                value = row.get(col)
                if col in merchant_columns and value and isinstance(value, str):
                    # Format merchant name by replacing underscores with spaces
                    # and applying title case
                    formatted_name = value.replace('_', ' ').title()
                    # Use merchant_name as the key if this was merchant_id
                    new_col_name = 'merchant_name' if col == 'merchant_id' else col
                    formatted_row[new_col_name] = formatted_name
                    column_mapping[col] = new_col_name
                else:
                    formatted_row[col] = value
            formatted_data.append(formatted_row)

        # Update column names based on mapping
        updated_columns = []
        for col in columns:
            updated_columns.append(column_mapping.get(col, col))

        result["data"] = formatted_data
        result["columns"] = updated_columns

        return result

    # Test data
    test_result = {
        "success": True,
        "data": [
            {"payment_id": "10000636248", "merchant_id": "Crossfit_Hanna", "transaction_amount": 58.66},
            {"payment_id": "10001482390", "merchant_id": "Belles_cookbook_store", "transaction_amount": 36.62},
            {"payment_id": "10001579064", "merchant_id": "Golfclub_Baron_Friso", "transaction_amount": 130.67}
        ],
        "columns": ["payment_id", "merchant_id", "transaction_amount"],
        "row_count": 3
    }

    print("Before formatting:")
    print(f"Columns: {test_result['columns']}")
    for row in test_result['data']:
        print(f"  {row}")

    # Apply formatting
    formatted_result = post_process_merchant_names(test_result)

    print("\nAfter formatting:")
    print(f"Columns: {formatted_result['columns']}")
    for row in formatted_result['data']:
        print(f"  {row}")

if __name__ == "__main__":
    test_merchant_formatting()