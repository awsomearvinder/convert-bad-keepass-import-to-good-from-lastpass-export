import csv
import sys


def get_contents(original_csv):
    contents = []
    for i, row in enumerate(original_csv):
        # the first row is the names.
        if i == 0:
            names = row
            continue
        contents.append(dict(zip(names, row)))
    return contents


def main():
    print("Starting script...")
    contents = []
    with open(sys.argv[1], newline="") as f:
        csv_file = csv.reader(f)
        contents = get_contents(csv_file)

    output = []
    for row in contents:
        if row["username"] != "":
            output.append(row)
            continue
        if row["extra"].strip().startswith("Username: "):
            username = row["extra"].strip()[len("Username: ") :]
            strip_newline = False
            if username.find("\n") != -1:
                username = username[: username.find("\n")]
                strip_newline = True

            row["username"] = username
            row["extra"] = row["extra"].strip()[len("Username: " + username + "\n" if strip_newline else "") :]
        if row["extra"].strip().startswith("Password: "):
            password = row["extra"].strip()[len("Password: ") :]
            if password == row["password"]:
                row["extra"] = row["extra"].strip()[len("Password: " + password) :]
        
        row["url"] = sys.argv[2]
        output.append(row)

    print('\n'.join(str(val) for val in output))
    with open("output.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(name for name in output[0])
        writer.writerows([[val for val in row.values()] for row in output])