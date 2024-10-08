import json
import copy
import base64
import sys

def topic_smt_extends(fake_topics): # extend fakepolicy
    """
    To extend IoT Synonyms
    """
    def get_sub_set(nums):
        sub_sets = [[]]
        for x in nums:
            sub_sets.extend([item + [x] for item in sub_sets])
        return sub_sets

    def extend_topic(topic):
        if topic.startswith("topic/"):
            topic = topic[6:]
        topic = topic.split("/")
        sets = range(len(topic))
        sub_sets = get_sub_set(sets)
        cache = []
        for sub in sub_sets:
            topic_cache = copy.deepcopy(topic)
            for point in sub:
                topic_cache[point] = "+"
            cache.append("/".join(topic_cache))

        slash_sets = copy.deepcopy(cache)
        slash_sets = map(lambda x: x.split("/"), slash_sets)
        slash_sets = list(slash_sets)
        slash_cache = set()
        for i in sets:
            for cell in slash_sets:
                new_cell = copy.deepcopy(cell)
                new_cell[i] = '#'
                slash_cache.add("/".join(new_cell))

        for cell in slash_cache:
            cell = cell[0: cell.index("#") + 1]
            cache.append(cell)
        return cache
    if type(fake_topics) == str:
        fake_topics = [fake_topics]
    subscribe_topics = []
    for topic in fake_topics:
        if type(topic) == list:
            if topic[1] == 'iot:subscribe':
                subscribe_topics.append(topic[0])
        else:
            subscribe_topics.append(topic)
    e_topics = []
    for topic in subscribe_topics:
        cache = extend_topic(topic)
        e_topics = e_topics + cache
    e_topics = list(set(e_topics))
    return e_topics

if __name__ == "__main__":
    # 从命令行读取 rawtopic
    if len(sys.argv) > 1:
        rawtopic = sys.argv[1]
        print(topic_smt_extends(rawtopic))
    else:
        print("No topic provided")
