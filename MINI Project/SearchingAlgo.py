import pandas as pd

def search_by_filter(data, column_indices, search_value, selected_filter):

    filtered_data = pd.DataFrame()
    search_value_lower = search_value.strip().lower()

    for index, row in data.iterrows():
        values = [str(row.iloc[col]).strip().lower() if pd.notna(row.iloc[col]) else '' for col in column_indices]

        if selected_filter == "AND":
            if all(search_value_lower in value for value in values):
                filtered_data = pd.concat([filtered_data, row.to_frame().T])

        elif selected_filter == "OR":
            if any(search_value_lower in value for value in values):
                filtered_data = pd.concat([filtered_data, row.to_frame().T])

        elif selected_filter == "NOT":
            if not any(search_value_lower in value for value in values):
                filtered_data = pd.concat([filtered_data, row.to_frame().T])

        elif selected_filter == "Starts With":
            if any(value.startswith(search_value_lower) for value in values):
                filtered_data = pd.concat([filtered_data, row.to_frame().T])

        elif selected_filter == "Ends With":
            if any(value.endswith(search_value_lower) for value in values):
                filtered_data = pd.concat([filtered_data, row.to_frame().T])

        elif selected_filter == "Contains":
            if any(search_value_lower in value for value in values):
                filtered_data = pd.concat([filtered_data, row.to_frame().T])

    return filtered_data.reset_index(drop=True)


def linearSearch(data: pd.DataFrame, search_value: str):
    """Perform a linear search across all rows and columns."""
    filtered_data = []
    
    for index, row in data.iterrows():
        if row.astype(str).str.contains(search_value, case=False).any():
            filtered_data.append(row)

    return pd.DataFrame(filtered_data).reset_index(drop=True) 

def binarySearch(data: pd.DataFrame, search_value: str, column_index: int) -> pd.DataFrame:
    """Perform a binary search on a specific column and return all matching rows."""
    low = 0
    high = len(data) - 1
    results = pd.DataFrame()

    search_value_lower = search_value.lower()

    while low <= high:
        mid = (low + high) // 2

        mid_value = str(data.iloc[mid, column_index]).lower()

        if mid_value == search_value_lower:
            results = pd.concat([results, data.iloc[[mid]]])

            left = mid - 1
            while left >= low:
                left_value = str(data.iloc[left, column_index]).lower()
                if left_value == search_value_lower:
                    results = pd.concat([results, data.iloc[[left]]])
                else:
                    break
                left -= 1

            right = mid + 1
            while right <= high:
                right_value = str(data.iloc[right, column_index]).lower()
                if right_value == search_value_lower:
                    results = pd.concat([results, data.iloc[[right]]])
                else:
                    break
                right += 1

            return results.reset_index(drop=True)

        elif mid_value < search_value_lower:
            low = mid + 1
        else:
            high = mid - 1

    return results.reset_index(drop=True)