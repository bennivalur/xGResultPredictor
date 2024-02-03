from PIL import Image, ImageDraw
from PIL import ImageFont
import json
from predictCS import getNextGameWeek

from teams import teams

width = 850
height = 1050

header = 50
table_header_height = 50


def getTeam(team):
    return list(filter(lambda d: d['title'] == team, teams))[0]['team']

def getTitle(team):
    if(team == "Nott'm Forest"):
        return teams[15]['title']
    return list(filter(lambda d: d['team'] == team, teams))[0]['title']

def getIMGName(team):
    if(team == "Nott'm Forest" ):
        return teams[15]['img']
    return list(filter(lambda d: d['title'] == team, teams))[0]['img']



def drawWinOdds(week):
    im = Image.new('RGB', (width, header + height+table_header_height), (0, 0, 0))
    draw = ImageDraw.Draw(im)
    background_color = (46, 162, 219)
    outline_color = (0, 0, 0)

    #background and border
    draw.rectangle((0,0, width,header + height+table_header_height), fill=background_color, outline=outline_color,width=10)

    with open('epl/' + str(week) + '_clean_sheet_odds.json','r') as cs:
        clean_sheets = json.load(cs)
    
    player_height = (height - header - table_header_height ) / (len(clean_sheets)/2)
    font = ImageFont.truetype("Roboto-Black.ttf", 45)
    smallfont = ImageFont.truetype("Roboto-Light.ttf", 22)

    draw.text((width/2,header/2+30),'Week ' + str(week) + '| Chances of Winning',(0, 0, 0),anchor='ms',font=font)

    

    logos = []
    for index, cs in enumerate(clean_sheets):
        if(index%2 == 0):
            #print(clean_sheets[index])
            #print(clean_sheets[index+1])
            font = ImageFont.truetype("Roboto-Black.ttf", 30)
            logos.append(Image.open('logos/'+ getIMGName(clean_sheets[index]['team']) +'.PNG', 'r'))
            logos.append(Image.open('logos/'+ getIMGName(clean_sheets[index+1]['team']) +'.PNG', 'r'))
            #Draw image and credits
            l_offset =100 - logos[index].size[0]*0.5
            h_offset = ((logos[index].size[1]*index/2)*1.3)+header+table_header_height + 20
            offset = (l_offset,h_offset)
            offset = (int(offset[0]),int(offset[1]))
            im.paste(logos[index], offset,mask=logos[index])
            r_offset = width-140 - logos[index].size[0] +40
            offset = (r_offset,h_offset)
            offset = (int(offset[0]),int(offset[1]))
            im.paste(logos[index+1], offset,mask=logos[index+1])
            l_offset = l_offset+logos[index].size[0]
            space_between_logos = r_offset - l_offset

            home_odds = str(100*clean_sheets[index]['winOdds']).split(".")[0]+'%'
            if home_odds == '0%':
                home_odds = '0.1%'
            elif home_odds == '100%':
                home_odds = '0.99%'
            away_odds = str(100*clean_sheets[index+1]['winOdds']).split(".")[0]+'%'
            if away_odds == '0%':
                away_odds = '0.1%'
            elif away_odds == '100%':
                away_odds = '0.99%'

            #TODO needs to be cleaned up. is very unreadable at the moment
            draw.rectangle((l_offset,h_offset+10,l_offset+space_between_logos*clean_sheets[index]['winOdds'],h_offset+70),outline='black',width=3)
            draw.rectangle((l_offset+space_between_logos*clean_sheets[index]['winOdds'],h_offset+10,l_offset+space_between_logos*round((1-clean_sheets[index+1]['winOdds']),2),h_offset+70),outline='black',width=3)
            draw.rectangle((l_offset+space_between_logos*round((1-clean_sheets[index+1]['winOdds']),2),h_offset+10,r_offset,h_offset+70),outline='black',width=3)
            tie_odds = str(100*round((1-clean_sheets[index]['winOdds']-clean_sheets[index+1]['winOdds']),2)).split(".")[0]+'%'

            draw.text((l_offset + 10,h_offset+(logos[index+1].size[1])/1.25),home_odds,(0, 0, 0),anchor='ls',font=font)
            draw.text((r_offset -30,h_offset+(logos[index+1].size[1])/1.25),away_odds,(0, 0, 0),anchor='ms',font=font)

            a = l_offset+space_between_logos*clean_sheets[index]['winOdds']
            b = l_offset+space_between_logos*round((1-clean_sheets[index+1]['winOdds']),2)
            c = ((b - a)/2) + a

            draw.text((c,h_offset+(logos[index+1].size[1])/1.25),tie_odds,(0, 0, 0),anchor='ms',font=font)
    
    
    

    
    font = ImageFont.truetype("Roboto-Black.ttf", 30)
    draw.text((width/2,height),'Made by @bennivaluR_ for @theFPLBot',(0,0,0),anchor='ms',font=font)

    im.save('winOdds/week_' + str(week) + '_odds' + '.png', quality=95)


drawWinOdds(getNextGameWeek())