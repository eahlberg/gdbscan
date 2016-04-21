import copy

UNCLASSIFIED = -2
NOISE = -1


def GDBSCAN(objects, n_pred, min_card, w_card):
    objects = copy.deepcopy(objects)
    cluster_id = 0
    for obj in objects:
        if obj.cluster_id == UNCLASSIFIED:
            if _expand_cluster(objects, obj, cluster_id, n_pred, min_card,
                               w_card):
                cluster_id = cluster_id + 1
    clusters = {}
    for obj in objects:
        key = obj.cluster_id
        if key in clusters:
            clusters[key].append(obj)
        else:
            clusters[key] = [obj]
    return list(clusters.itervalues())


def _expand_cluster(objects, obj, cluster_id, n_pred, min_card, w_card):
    if not _in_selection(w_card, obj):
        objects.change_cluster_id(obj, UNCLASSIFIED)
        return False

    seeds = objects.neighborhood(obj, n_pred)
    if not _core_object(w_card, min_card, seeds):
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


def _in_selection(w_card, obj):
    return w_card([obj]) > 0


def _core_object(w_card, min_card, objects):
    return w_card(objects) >= min_card


class Objects:
    def __init__(self, objects):
        self.objects = objects

    def __iter__(self):
        for obj in self.objects:
            yield obj

    def __repr__(self):
        return str(self.objects)

    def get(self, index):
        return self.objects[index]

    def neighborhood(self, obj, n_pred):
        return filter(lambda x: n_pred(obj, x), self.objects)

    def change_cluster_ids(self, objs, value):
        for obj in objs:
            self.change_cluster_id(obj, value)

    def change_cluster_id(self, obj, value):
        index = (self.objects).index(obj)
        self.objects[index].cluster_id = value

    def labels(self):
        return set(map(lambda x: x.cluster_id, self.objects))
