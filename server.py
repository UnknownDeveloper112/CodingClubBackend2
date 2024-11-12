from http.server import BaseHTTPRequestHandler, HTTPServer
import json

FILE_PATH="data.txt"

class SimpleJSONServer(BaseHTTPRequestHandler):

    BRANCH={"cs":"A7","ece":"AA","eee":"A3","eni":"A8","mech":"A4","civil":"A2","phy":"B5","chem":"B2","chemical":"A1","math":"B4","bio":"B1","eco":"B3","pharma":"A5","manu":"AB","genstudies":"D2"}
    CAMPUS={"G":"goa","P":"pilani","H":"hyderabad"}
    ID=[]

    with open(FILE_PATH, 'r') as f:
        ID=f.read().split("\n")[:-1]


    def to_json(self,ls):
        st='{{"ID": {}}}'.format(str(ls).replace("'",'"'))
        return st

    def to_text(self,ls):
        return "<br>".join(ls)



    def json_data(self,ls):

        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(self.to_json(ls).encode("utf-8"))

    def text_data(self,ls):

        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(self.to_text(ls).encode("utf-8"))



    
    def branch_data(self,branch):
        ls=[]
        for i in self.ID:
            if i[4:6]==branch:
                ls.append(i)
        self.json_data(ls)


    def year_data(self,year):
        ls=[]
        for i in self.ID:
            if int(i[:4])==2025-year:
                ls.append(i)
        self.json_data(ls)


    def id_data(self,id_str):
        ID_entire=""
        for i in self.ID:
            if i[8:12]==id_str:
                ID_entire=i
        if ID_entire=='':
            self.invalid_URL("ID")
            return
        year=int(ID_entire[:4])
        branch=''
        for i in self.BRANCH:
            if self.BRANCH[i]==ID_entire[4:6]:
                branch=i
        uid=int(ID_entire[8:12])
        email="f{}{}@{}.bits-pilani.ac.in".format(year,uid,self.CAMPUS[ID_entire[-1]])

        st='{{"id":{{"year":{},"branch":"{}","campus":"{}","email":"{}","id":"{}","uid":{}}}}}'.format(2025-year,branch,self.CAMPUS[ID_entire[-1]],email,ID_entire,uid)

        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(st.encode("utf-8"))




    def invalid_URL(self,context):

        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        text='{{"error":"invalid {}"}}'.format(context)
        self.wfile.write(text.encode("utf-8"))



    def do_GET(self):

        self.send_response(200)

        PATH=self.path[1:].split(",")

        if PATH[0]=="":
            self.json_data(self.ID)


        elif PATH[0][:8]=="?format=":
            if PATH[0][8:]=="json":
                self.json_data(self.ID)

            elif PATH[0][8:]=="text":
                self.text_data(self.ID)

            else:
                self.invalid_URL("Format")


        elif PATH[0][:8]=="?branch=":
            if PATH[0][8:] in self.BRANCH.keys():
                self.branch_data(self.BRANCH[PATH[0][8:]])
            else:
                self.invalid_URL("Branch")

        elif PATH[0][:6]=="?year=":
            try:
                x=int(PATH[0][6:])
            except ValueError:
                self.invalid_URL("year")
                return

            if x>=1 and x<=6:
                self.year_data(x)
            else:
                self.invalid_URL("year")

        elif len(PATH[0])==4 and PATH[0].isdigit():
            self.id_data(PATH[0])

        else:
            self.invalid_URL("Path")



httpd = HTTPServer(('',8000), SimpleJSONServer)
print("Server running...")
httpd.serve_forever()
