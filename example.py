lists = [
    {"name":"list1","sublists":[
        {"name":"list1-1","sublists":[
            {"name":"list1-1-1","sublists":[]},{"name":"list1-1-2","sublists":[{"name":"list1-1-2-1","sublists":[]}]},{"name":"list1-1-3","sublists":[]}
        ]},
        {"name":"list1-2","sublists":[
            {"name":"list1-2-1","sublists":[]},{"name":"list1-2-2","sublists":[]}
        ]}
    ]},
    {"name":"list2","sublists":[
        {"name":"list2-1","sublists":[]}
    ]},
    {"name":"list3","sublists":[]}
]


other_list = [
    {"name":"list1","sublists":[]},
    {"name":"list1-1","sublists":[]},
    {"name":"list1-1-1","sublists":[]},
    {"name":"list1-1-2","sublists":[]},
    {"name":"list1-1-2-1","sublists":[]},
    {"name":"list1-1-3","sublists":[]},
    {"name":"list1-2","sublists":[]},
    {"name":"list1-2-1","sublists":[]},
    {"name":"list1-2-2","sublists":[]},
    {"name":"list2","sublists":[]},
    {"name":"list2-1","sublists":[]},
    {"name":"list3","sublists":[]}
]
count = 0

def extract_sublists(all_lists):
    global count
    count += 1
    done = True
    new_list = all_lists

    for l in all_lists:
        if l["sublists"] != []:
            done = False
            for x in l["sublists"]:
                x_index = l["sublists"].index(x)
                del l["sublists"][x_index]
                new_list.insert(all_lists.index(l)+1, x)

    if done or count > 5:
        return new_list
    else:
        #print(count)
        return extract_sublists(new_list)



sorted_list = extract_sublists(lists)

for i in sorted_list:
    print(i)