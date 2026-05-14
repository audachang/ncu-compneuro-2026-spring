import cudf
import pandas as pd
from IPython.display import display

print("Creating DataFrame with categorical data...")
pdf = pd.DataFrame({'county': ['A', 'B', 'A', 'C']})
gdf = cudf.from_pandas(pdf)
gdf['county'] = gdf['county'].astype('category')

print("\n--- TEST 1: Triggering Bug (Display cuDF Categorical Series) ---")
try:
    # This acts like df_sampled.county in the notebook
    # It triggers __repr__ -> concat -> distinct_count -> Crash on Blackwell
    print(gdf['county']) 
except RuntimeError as e:
    if "cuGetProcAddress" in str(e):
        print("✅ SUCCESS: Reproduced expected 'cuGetProcAddress' error on Blackwell.")
    else:
        print(f"❌ FAILED: Different error caught: {e}")
except Exception as e:
    print(f"❌ FAILED: Unexpected error type: {type(e)}")
else:
    print("⚠️ WARNING: Code ran without error (Issue not reproduced).")

print("\n--- TEST 2: Verifying Workaround (.to_pandas()) ---")
try:
    # Workaround: Convert to pandas for display
    print(gdf['county'].to_pandas())
    print("✅ SUCCESS: Workaround executed successfully.")
except Exception as e:
    print(f"❌ FAILED: Workaround failed: {e}")
