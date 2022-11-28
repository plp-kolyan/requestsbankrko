

def up_version(version_list, index=None):
    if index is None:
        last_index = len(version_list) - 1
    else:
        last_index = index
    version_list[last_index] = str(int(version_list[last_index]) + 1)

    if last_index == 0:
        return '.'.join(version_list)
    else:
        last_chr = int(version_list[last_index])
        last_chr_10 = last_chr / 10
        if last_chr_10 > 9.9:
            version_list[last_index] = str(0)
            last_index -= 1
            return up_version(version_list, last_index)
        return '.'.join(version_list)


def update_version(path_to_file="pyproject.toml"):
    import toml
    data = {}

    with open(path_to_file, "r", encoding="UTF-8") as file:
        data = toml.load(file)
        version_list = data['project']['version'].split('.')
        data['project']['version'] = up_version(version_list)
    with open(path_to_file, "w", encoding="UTF-8") as file:
        toml.dump(data, file).encode('utf-8')


if __name__ == '__main__':
    update_version()
