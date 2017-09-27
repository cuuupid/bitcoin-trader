import os,json
def findkey(key_denotation):
    keyname, folder = key_denotation.split('-')
    for file in os.listdir('./static/'+folder):
        if file[:file.rfind('.')]==key_denotation:
            return 'static/'+folder+'/'+file
    return None
def parsekey(key_file):
    json_data = json.load(open(key_file))
    return { 'key':json_data['key'] }