data = {
    "employee" : [
        {"id":"ID001","nama": "Julius", "image": "muka1.jpg"},
        {"id":"ID002","nama": "daffa", "image": "muka2.jpg"},
        {"id":"ID003","nama": "ipul", "image": "muka3.jpeg"},
        {"id":"ID004","nama": "maemunah", "image": "muka4.jpeg"}
    ]
}

for employee in data["employee"]:
    # print(employee["nama"])
    #looping semua data dan menampilkan nama

    if employee["nama"] == "ipul":
        print(employee["nama"])
        #mengambil value nama = ipul
