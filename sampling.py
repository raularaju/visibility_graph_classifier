import pandas as pd

# Load your CSV data
df = pd.read_csv('exams.csv')

# Define the columns representing the 6 classes
class_columns = ['SB','1dAVb','LBBB','ST','AF', 'RBBB',]

# Create a DataFrame for instances not belonging to any class
no_class_df = df[df[class_columns].sum(axis=1) == 0]

# Calculate the minimum number of instances in any group
min_group_size = min(no_class_df.shape[0], df[class_columns].sum().min())
print(df[class_columns].sum())
# Create DataFrames for each class group and sample instances without repetition
class_groups = {}
assigned_instances = set()
count_class = {'1dAVb': 0,'RBBB': 0,'LBBB': 0,'SB': 0,'ST': 0,'AF': 0}


for class_col in class_columns:
    class_df = df[df[class_col] == True]
    class_df = class_df[~class_df.index.isin(assigned_instances)]
    # Sample instances without repetition
    print(class_col, class_df.shape[0])
    if class_df.shape[0] >= min_group_size - count_class[class_col]:
        print(f"vrau {class_col}")
        sampled_instances = class_df.sample(n=min_group_size - count_class[class_col])
        for _, samp_instance in sampled_instances.iterrows():
            for c in class_columns:
                if samp_instance[c] == True:
                    count_class[c] += 1
            
        assigned_instances.update(sampled_instances.index)
        class_groups[class_col] = sampled_instances

# Sample instances from the no_class_df without repetition
no_class_group = no_class_df[~no_class_df.index.isin(assigned_instances)]
no_class_group = no_class_group.sample(n=min_group_size)
assigned_instances.update(no_class_group.index)

# Combine all the groups into one DataFrame


stratified_sample = pd.concat([no_class_group] + list(class_groups.values()))

# Shuffle the rows to ensure randomness
stratified_sample = stratified_sample.sample(frac=1).reset_index(drop=True)
stratified_sample= stratified_sample[  ['exam_id', 'trace_file'] + class_columns ] 
# Save the stratified sample to a new CSV file
stratified_sample.to_csv('stratified_sample.csv', index=False)

df = pd.read_csv('stratified_sample.csv')



for c in class_columns:
    print(f'{c}: {df[c].sum()/ df.shape[0]}')
no_class_df = df[df[class_columns].sum(axis=1) == 0]