
def list_split(listA, n):
    for x in range(0, len(listA), n):
        every_chunk = listA[x:n+x]

        if len(every_chunk) < n:
            every_chunk = every_chunk + \
                [None for y in range(n-len(every_chunk))]
        yield every_chunk


def move_list_item(list, original_index, new_index):
    list.insert(new_index, list.pop(original_index))


def find_track_index_from_list(list: list, uri):
    for index, track in enumerate(list):
        if track['track']['uri'] == uri:
            return index
    raise Exception('Track Index doesn\'t exist')