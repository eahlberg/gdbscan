UNCLASSIFIED = -2
NOISE = -1


def GDBSCAN(objects, n_pred, min_card, w_card):
    cluster_id = NOISE + 1
    for i in range(len(objects) - 1):
        obj = objects.get(i)
        if obj.cluster_id == UNCLASSIFIED:
            if expand_cluster(objects, obj, cluster_id, n_pred, min_card,
                              w_card):
                cluster_id = cluster_id + 1
    return objects


def expand_cluster(objects, obj, cluster_id, n_pred, min_card, w_card):
    if not in_selection(w_card, obj):
        objects.change_cluster_id(obj, UNCLASSIFIED)
        return False

    seeds = objects.neighborhood(obj, n_pred)
    if not core_object(w_card, min_card, seeds):
        objects.change_cluster_id(obj, NOISE)
        return False

    objects.change_cluster_ids(seeds, cluster_id)
    seeds.remove(obj)

    while len(seeds) > 0:
        current_obj = seeds[0]
        result = objects.neighborhood(current_obj, n_pred)
        if w_card(result) >= min_card:
            for p in result:
                if w_card([p]) > 0 and p.cluster_id in [UNCLASSIFIED, NOISE]:
                    if p.cluster_id == UNCLASSIFIED:
                        seeds.append(p)
                    objects.change_cluster_id(p, cluster_id)
        seeds.remove(current_obj)
    return True


def in_selection(w_card, obj):
    return w_card([obj]) > 0


def core_object(w_card, min_card, objects):
    return w_card(objects) >= min_card


def w_card(objects):
    return len(objects)


class Objects:
    def __init__(self, objects):
        self.objects = objects

    def get(self, index):
        return self.objects[index]

    def __len__(self):
        return len(self.objects)

    def __repr__(self):
        return str(self.objects)

    def neighborhood(self, obj, n_pred):
        return filter(lambda x: n_pred(obj, x), self.objects)

    def change_cluster_ids(self, objs, value):
        for obj in objs:
            self.change_cluster_id(obj, value)

    def change_cluster_id(self, obj, value):
        index = self.objects.index(obj)
        self.objects[index].cluster_id = value
