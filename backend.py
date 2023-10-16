import json
import boto3
import difflib

nutrients = {'kcal' : 2650 , 'protein' : 65, 'calcium' : 800, 'vegetable' : 21}

menu_list = [
    ['バンバンジー豆腐', 'bang bang chicken with tofu',132,134,10.2,7.4,7.8,1.2,3,30,'副菜'],
    ['冷奴', 'cold tofu',66,54,4.4,3.1,2.1,0.1,1,3,'副菜'],
    ['ポテト&コーンサラダ', 'potato and corn salad',110,74,1.7,3.8,9.3,0.6,12,45,'副菜'],
    ['豚汁', 'miso soup with pork and vegetables',88,72,4.3,2.7,7.2,1.4,11,41,'副菜'],
    ['味噌汁(豆腐・わかめ)', 'miso soup',44,22,1.2,0.5,2.8,1.5,0,0,'副菜'],
    ['照り焼きソースカツ丼(小)', 'pork cutlets with teriyaki sauce bowl (small)',407,531,13.7,13.1,84.2,1.4,5,10,'主食(ご飯)'],
    ['照り焼きソースカツ丼(中)', 'pork cutlets with teriyaki sauce bowl (medium)',473,760,20,19.7,118.5,2,8,15,'主食(ご飯)'],
    ['照り焼きソースカツ丼(大)', 'pork cutlets with teriyaki sauce bowl (large)',561,994,26.2,26.3,153.5,2.8,10,20,'主食(ご飯)'],
    ['マジカレー監修カレー(小)', 'curry rice topped with hamburger steak (small)',462,739,23.2,28.1,92.7,3.5,99,41,'主食(ご飯)'],
    ['マジカレー監修カレー(中)', 'curry rice topped with hamburger steak (medium)',528,917,26.2,32.1,123.5,4.2,99,48,'主食(ご飯)'],
    ['マジカレー監修カレー(大)', 'curry rice topped with hamburger steak (large)',616,1185,30.5,42.2,161.8,5.9,99,65,'主食(ご飯)'],
    ['カレーライス(小)', 'curry rice(small)',253,440,8.2,7.8,81.7,3.6,30,23,'主食(ご飯)'],
    ['カレーライス(中)', 'curry rice(medium)',286,579,10.7,9,109.8,4,34,24,'主食(ご飯)'],
    ['カレーライス(大)', 'curry rice(large)',374,738,13.6,11.4,140.1,4.8,42,26,'主食(ご飯)'],
    ['味噌カツ', 'pork cutlets with miso sauce',363,481,17.6,27.8,38.8,2,24,35,'主菜'],
    ['豚肉ガリバタ醤油炒め', 'stir-fried pork, onion, and shimeji mashroom with garlic butter and soy sauce',319,300,20.9,16.6,13.8,1.2,7,60,'主菜'],
    ['さば生姜煮', 'mackerel stewed with ginger',209,208,9.5,14.2,5.6,0.8,5,0,'主菜'],
    ['チキンカツ', 'chicken cutlets',187,231,12.9,14.6,12.2,0.4,0,0,'主菜'],
    ['かき揚げうどん(中)', 'udon noodles with mixed tempure (medium)',374,446,10.1,3.6,93.6,5.5,47,41,'主食(麺)'],
    ['かき揚げうどん(大)', 'udon noodles with mixed tempure (large)',440,599,13.4,4.2,127.4,5.8,57,41,'主食(麺)'],
    ['かけそば(中)', 'plain soba noodles (medium)',275,333,14.1,2,65.2,4.5,23,10,'主食(麺)'],
    ['かけそば(大)', 'plain soba noodles (large)',341,482,20.4,3,94,4.5,33,10,'主食(麺)'],
    ['かけうどん(中)', 'plain udon noodles (medium)',275,332,7.3,1.3,72.8,4.2,23,10,'主食(麺)'],
    ['かけうどん(大)', 'plain udon noodles (large)',341,485,10.6,1.9,106.6,4.5,33,10,'主食(麺)'],
    ['味噌ラーメン(中)', 'miso ramen (medium)',418,499,21.5,10.1,81,9.5,21,26,'主食(麺)'],
    ['味噌ラーメン(大)', 'miso ramen (large)',484,665,27.4,10.9,114.7,9.8,31,26,'主食(麺)'],
    ['辛味噌ラーメン(中)', 'ramen in hot-miso based soup (mediim)',418,577,21.5,17.9,81.6,8.9,21,26,'主食(麺)'],
    ['辛味噌ラーメン(大)', 'ramen in hot-miso based soup (large)',484,743,27.4,18.7,115.3,9.2,31,26,'主食(麺)'],
    ['濃厚とんこつ醤油ラーメン(中)', 'ramen in pork bone and soy-souse flavored rich soup (medium)',517,516,19.9,14.3,77.5,7.8,60,56,'主食(麺)'],
    ['濃厚とんこつ醤油ラーメン(大)', 'ramen in pork bone and soy-souse flavored rich soup (large)',583,682,25.8,15.1,111.2,8.1,70,56,'主食(麺)'],
    ['豚汁そば(中)', 'soba noodles topped with root vegetables and japanese mushrooms in miso soup (medium)',473,455,22.4,8.5,70.6,3.4,47,58,'主食(麺)'],
    ['豚汁そば(大)', 'soba noodles topped with root vegetables and japanese mushrooms in miso soup (large)',539,604,28.7,9.5,99.4,3.4,57,58,'主食(麺)'],
    ['豚汁うどん(中)', 'udon noodles topped with root vegetables and japanese mushrooms in miso soup (medium)',473,465,16.3,7.8,80.5,4.2,47,58,'主食(麺)'],
    ['豚汁うどん(大)', 'udon noodles topped with root vegetables and japanese mushrooms in miso soup (large)',539,618,19.6,8.4,114.3,4.5,57,58,'主食(麺)'],
    ['牛肉コロッケ', 'beef croquette',110,237,3.2,15.8,20.6,0.6,9,1,'副菜'],
    ['ハムカツ', 'ham cutlet',132,294,8.9,18.9,21.3,2,26,0,'副菜'],
    ['白身フライオーロラソース', 'fried while fish with aurore sause (with shredded cabbage)',275,621,11.8,49.7,29.7,1.4,32,35,'主菜'],
    ['チーズメンチデミソース', 'minced meat cutlets filled with cream cheese with demiglace sause',319,476,13.1,34.3,28.1,1.9,74,54,'主菜'],
    ['辛みそ豚丼(小)', 'rice bowl topped with pork and spicy miso (small)',374,513,20.2,11.1,76.9,1.3,0,35,'主食(ご飯)'],
    ['辛みそ豚丼(中)', 'rice bowl topped with pork and spicy miso (medium)',440,720,28.5,16,107.1,1.8,0,50,'主食(ご飯)'],
    ['辛みそ豚丼(大)', 'rice bowl topped with pork and spicy miso (large)',528,958,39,22.4,138.8,2.5,0,70,'主食(ご飯)'],
    ['鮭丼(中)', 'samon rice bowl (medium)',528,554,18.4,7.1,97.7,2.5,4,0,'主食(ご飯)'],
    ['鮭丼(大)', 'samon rasice bowl (large)',561,673,20.5,7.1,123.6,2.5,4,0,'主食(ご飯)'],
    ['おからの色どりサラダ', 'colorful soy pulp salad',66,95,4,5.5,7.5,1,0,17,'副菜'],
    ['きんぴらごぼう', 'sauteed burdock kimpira style',66,40,0.8,0.8,7.6,0.8,16,31,'副菜'],
    ['薩摩ハーブ鶏のレバー煮', 'stewed liver of satsuma herb chiken',88,81,9.4,1.3,8.1,0.3,0,0,'副菜'],
    ['惣菜コンビ', 'sweet potato glace & spinach dressed with sesame seeds',110,61,1.4,0.6,13,0.2,43,25,'副菜'],
    ['オクラのお浸し', 'ohitashi chopped okra',66,20,1.3,0.1,4.4,0.3,45,50,'副菜'],
    ['パンプキンサラダ', 'punpukin salad',66,100,1.5,7,8,0.5,0,33,'副菜'],
    ['ほうれん草のごまあえ', 'boiled spinach with sesame paste',66,28,2.1,1,3.3,0.5,84,50,'副菜']
]

def search_menu(input, menu_list):
    text_list = []
    idx_list = []
    for text in input:
        text_list.append(text.lower())
    for text in text_list:
        for idx in range(0,49):
            rate = difflib.SequenceMatcher(None, text, menu_list[idx][1]).ratio()
            #print(rate)
            if rate > 0.92:
                #print(rate)
                idx_list.append(idx)
    return idx_list
    
def create_dict(idx_list, menu_list):
    sum_price = 0
    sum_kcal = 0
    sum_protein = 0
    sum_fat = 0
    sum_carbohydrate = 0
    sum_salt = 0
    sum_calcium = 0
    sum_vegetable = 0
    menus = []
    for idx in idx_list:
        menu = {}
        menu['name'] = menu_list[idx][0]
        menu['price'] = menu_list[idx][2]
        menu['kcal'] = menu_list[idx][3]
        menu['protein'] = menu_list[idx][4]
        menu['fat'] = menu_list[idx][5]
        menu['carbohydrate'] = menu_list[idx][6]
        menu['salt'] = menu_list[idx][7]
        menu['calcium'] = menu_list[idx][8]
        menu['vegetable'] = menu_list[idx][9]
        menus.append(menu)
        sum_price += int(menu_list[idx][2])
        sum_kcal += int(menu_list[idx][3])
        sum_protein += float(menu_list[idx][4])
        sum_fat += float(menu_list[idx][5])
        sum_carbohydrate += float(menu_list[idx][6])
        sum_salt += float(menu_list[idx][7])
        sum_calcium += float(menu_list[idx][8])
        sum_vegetable += float(menu_list[idx][9])
    sum = {}
    sum['price'] = sum_price
    sum['kcal'] = sum_kcal
    sum['protein'] = sum_protein
    sum['fat'] = sum_fat
    sum['carbohydrate'] = sum_carbohydrate
    sum['salt'] = sum_salt
    sum['calcium'] = sum_calcium
    sum['vegetable'] = sum_vegetable
    dict = {}
    dict['menus'] = menus
    dict['sum'] = sum
    return dict
    
def cover_menu(kind, menu_list):
    max = 0
    menu_idx = 0
    for i in range(0,49):
        value = menu_list[i][kind] / menu_list[i][2]
        if value >= 0 and value > max:
            max = value
            menu_idx = i
    return menu_idx

def suggestion(dict, nutrients):
    rate_kcal = (nutrients['kcal'] - dict['sum']['kcal']) / nutrients['kcal']
    rate_protein = (nutrients['protein'] - dict['sum']['protein']) / nutrients['protein']
    rate_vegetable = ((nutrients['vegetable'] - dict['sum']['vegetable']) / nutrients['vegetable']) * 0.05
    if rate_kcal == max(rate_kcal, rate_protein, rate_vegetable):
        menu_idx = cover_menu(3, menu_list)
        return 'エネルギーが' + str(nutrients['kcal'] - dict['sum']['kcal']) + '不足しています．' + menu_list[menu_idx][0] + 'を提案します．また，カルシウムが' + str(nutrients['calcium'] - dict['sum']['calcium']) + '不足しています．ほうれん草のごまあえを提案します．'
    elif rate_protein == max(rate_kcal, rate_protein, rate_vegetable):
        menu_idx = cover_menu(4, menu_list)
        return 'タンパク質が' + str(nutrients['protein'] - dict['sum']['protein']) + '不足しています．' + menu_list[menu_idx][0] + 'を提案します．また，カルシウムが' + str(nutrients['calcium'] - dict['sum']['calcium']) + '不足しています．ほうれん草のごまあえを提案します．'
    else:
        menu_idx = cover_menu(9, menu_list)
        return '野菜が' + str(nutrients['vegetable'] - dict['sum']['vegetable']) + '不足しています．' + menu_list[menu_idx][0] + 'を提案します．また，カルシウムが' + str(nutrients['calcium'] - dict['sum']['calcium']) + '不足しています．ほうれん草のごまあえを提案します．'
    
def lambda_handler(event, context):
    
    bucket="suzuka-testbucket"
    document="S__61128775.jpg"
    client = boto3.client('textract')

    #process using S3 object
    response = client.detect_document_text(
        Document={'S3Object': {'Bucket': bucket, 'Name': document}})

    #Get the text blocks
    blocks=response['Blocks']
    input = []
    for block in blocks:
        if "Text" in block:
            input.append(block["Text"])
    
    d = create_dict(search_menu(input, menu_list), menu_list)
    d['suggest'] = suggestion(d, nutrients)
    
    return {
        'statusCode': 200,
        'body': json.dumps(d)
    }                
