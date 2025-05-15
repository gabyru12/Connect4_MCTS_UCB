import pandas as pd

def calculate_move_differences(dataset):
    # Extract the last 5 columns (best moves for 10,000 to 50,000 iterations)
    moves = dataset.iloc[:, -5:]

    # Get the best move for 50,000 iterations
    best_move_50000 = moves.iloc[:, -1]

    # Compare each of the prior iterations to the 50,000 iteration move
    differences = {
        10000: (moves.iloc[:, 0] != best_move_50000).sum(),
        20000: (moves.iloc[:, 1] != best_move_50000).sum(),
        30000: (moves.iloc[:, 2] != best_move_50000).sum(),
        40000: (moves.iloc[:, 3] != best_move_50000).sum(),
    }

    return differences

# Load the dataset
df = pd.read_csv(r"C:\Users\arcan\OneDrive\Ambiente de Trabalho\My apps\python\connect4Project\other_version\datasets\MCTSGeneratedDatasetSoftmax.csv", header=None)
df = df.iloc[:, :-5]
# Remove duplicate rows
print(len(df))
df = df.drop_duplicates()
print(len(df))

# Calculate differences
#differences = calculate_move_differences(df)

# Output the result
#print(differences)