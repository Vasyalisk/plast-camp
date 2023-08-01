import os


def main():
    req_path = "/requirements"
    file_names = os.listdir(req_path)
    file_names = [os.path.join(req_path, one) for one in file_names if one.endswith(".in")]
    [sort_file(one) for one in file_names]
    print(f"Sorted files: {', '.join(file_names)}")


def sort_file(file_name):
    with open(file_name, "r") as f:
        lines = f.readlines()

    lines = (one for one in lines if one.strip())
    spec_lines = []
    req_lines = []
    for line in lines:
        if not line.endswith("\n"):
            line += "\n"

        if line[0].isalpha():
            req_lines.append(line)
        else:
            spec_lines.append(line)

    lines = [*spec_lines, *sorted(req_lines)]
    with open(file_name, "w+") as f:
        f.writelines(lines)


if __name__ == "__main__":
    main()
