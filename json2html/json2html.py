import json
import pdb


def json2html(data, size):
    # pdb.set_trace()
    
    result = ''
    loop = 0
    
    if type(data) == list:
        loop = len(data)
        
        for i in range(loop):
            tmp = data[i]
    
            for k in tmp.keys():
                html = "<div class='list' style='margin: 5px 0px 5px {}px;'>{}</div>\n"
                
                if len(tmp[k]) != 0:
                    html = html.format(15*size, k + json2html(tmp[k], size+1))
                else:
                    html = html.format(15*size, k)
                # pdb.set_trace()
                result += html
    else:
        for k in data.keys():
            html = "<div class='list' style='margin: 5px 0px 5px {}px;'>{}</div>\n"
            
            if len(data[k]) != 0:
                html = html.format(15*size, k + json2html(data[k], size+1))
            else:
                html = html.format(15*size, k)
            # pdb.set_trace()
            result += html
    return result
    


if __name__ == "__main__":
    f = open("result.html")
    data = json.load(f)
    f.close()
    result = json2html(data, 1)
    
    f = open("test.html", "w")
    f.write(result)
    f.close()