from copy import deepcopy



dicts = [
    {"name":"dict1","x":0,"y":0,"subdicts":[
        {"name":"dict1-1","x":0,"y":0,"subdicts":[
            {"name":"dict1-1-1","x":0,"y":0,"subdicts":[]},
            {"name":"dict1-1-2","x":0,"y":0,"subdicts":[
                {"name":"dict1-1-2-1","x":0,"y":0,"subdicts":[]}]},
            {"name":"dict1-1-3","x":0,"y":0,"subdicts":[]}]},
        {"name":"dict1-2","x":0,"y":0,"subdicts":[
            {"name":"dict1-2-1","x":0,"y":0,"subdicts":[]},
            {"name":"dict1-2-2","x":0,"y":0,"subdicts":[]}]}]},
    {"name":"dict2","x":0,"y":0,"subdicts":[
        {"name":"dict2-1","x":0,"y":0,"subdicts":[]}]},
    {"name":"dict3","x":1,"y":0,"subdicts":[]}
]



other_dict = [
    {"name":"dict1","subdicts":[]},
    {"name":"dict1-1","subdicts":[]},
    {"name":"dict1-1-1","subdicts":[]},
    {"name":"dict1-1-2","subdicts":[]},
    {"name":"dict1-1-2-1","subdicts":[]},
    {"name":"dict1-1-3","subdicts":[]},
    {"name":"dict1-2","subdicts":[]},
    {"name":"dict1-2-1","subdicts":[]},
    {"name":"dict1-2-2","subdicts":[]},
    {"name":"dict2","subdicts":[]},
    {"name":"dict2-1","subdicts":[]},
    {"name":"dict3","subdicts":[]}
]

count = 0




tasks = [
    {"task":"","sublevel":0},
    {"task":"","sublevel":1},
    {"task":"","sublevel":2},
    {"task":"","sublevel":2},
    {"task":"","sublevel":3},
    {"task":"","sublevel":2},
    {"task":"","sublevel":1},
    {"task":"","sublevel":2},
    {"task":"","sublevel":2},
    {"task":"","sublevel":0},
    {"task":"","sublevel":1},
    {"task":"","sublevel":0}
]

tasks = [
    {"task":"","sublevel":0,"subdicts":[
        {"task":"","sublevel":1,"subdicts":[
            {"task":"","sublevel":2,"subdicts":[]},
            {"task":"","sublevel":2,"subdicts":[
                {"task":"","sublevel":3,"subdicts":[]}]},
            {"task":"","sublevel":2,"subdicts":[]}]},
        {"task":"","sublevel":1,"subdicts":[
            {"task":"","sublevel":2,"subdicts":[]},
            {"task":"","sublevel":2,"subdicts":[]}]}]},
    {"task":"","sublevel":0,"subdicts":[
        {"task":"","sublevel":1,"subdicts":[]}]},
    {"task":"","sublevel":0,"subdicts":[]}
]




def extract_subdicts(all_dicts):
    global count
    count += 1
    done = True
    new_dict = all_dicts

    for l in all_dicts:
        if l["subdicts"] != []:
            done = False
            for x in l["subdicts"]:
                x_index = l["subdicts"].index(x)
                del l["subdicts"][x_index]
                new_dict.insert(all_dicts.index(l)+1, x)

    if done or count > 5:
        return deepcopy(new_dict)
    else:
        #print(count)
        return extract_subdicts(new_dict)


def search(all_dicts, x_id, parameter, value):
    for x in all_dicts:
        if x["x"] == x_id:
            if parameter == "delete":
                del all_dicts[all_dicts.index(x)]
            else:
                x[parameter] = value
            return
        if len(x["subdicts"]) > 0:
            search(x["subdicts"], x_id, parameter, value)
            



sorted_dict = extract_subdicts(deepcopy(dicts))

for i in sorted_dict:
    print(i)
print("-----------------")

for a in range(2):
    for i in dicts:
        pass
        print(i)
    search(dicts, 1, "delete", 2)
    print("_______________")