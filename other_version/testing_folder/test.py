array = []
with open(r"C:\Users\arcan\OneDrive\Ambiente de Trabalho\My apps\python\connect4Project\other_version\AI_vs_AI_statistics\noReset_vs_Reset.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            array.append(line.strip())

count = 0

for i in array:
    if i == "1":
        count += 1

print(count)
        