from PIL import Image, ImageDraw
from PIL import ImageFont
import json
from graphWinOdds import getTeam, getIMGName, getTitle
from datetime import date



from teams import teams

def graphResultsOfSimulation(league):
    
    width = 2275
    height = 1750
    header = 50
    table_header_height = 50

    im = Image.new('RGB', (width, header + height+table_header_height), (0, 0, 0))
    draw = ImageDraw.Draw(im)
    background_color = (46, 162, 219)
    #background_color = (255, 255, 255)
    outline_color = (0, 0, 0)

    #background and border
    draw.rectangle((0,0, width,header + height+table_header_height), fill=background_color, outline=outline_color,width=10)
    #player_height = (height - header - table_header_height ) / (len(clean_sheets)/2)
    font = ImageFont.truetype("Roboto-Black.ttf", 45)
    smallfont = ImageFont.truetype("Roboto-Light.ttf", 32)



    with open('simResults/'+ league + '_resultOfSimulations.json','r') as results:
        results = json.load(results)

    numberOfSimulations = results['numberOfSimulations']

    draw.text((width/2,header/2+30),'Simulating the Rest of the ' + league + ' Season (' + str(numberOfSimulations) + ' times)',(0, 0, 0),anchor='ms',font=font)

    #We need to find the average finishing position of each team
    avgPosition = {}



    del results['numberOfSimulations']

    for index,team in enumerate(results):
        avgPos = 0
        for position in results[team]:
            
            avgPos += float(position) * float(results[team][position])
        avgPos = avgPos / numberOfSimulations
        avgPosition[team] = avgPos

    avgPosition = dict(sorted(avgPosition.items(), key=lambda item: item[1]))

    logos = []
    l_offset = 100
    h_space_offset = 75
    l_space_offset = 100
    h_offset = 125

    for index,team in enumerate(avgPosition):
        
        temp_h_offset = h_offset + h_space_offset*index
        temp_l_offset = 75 + l_offset + l_space_offset*index
        offset = (l_offset,temp_h_offset)
        if(league == 'EPL'):
        #Print team logos
            logos.append(Image.open('logos/'+ getIMGName(team) +'.PNG', 'r'))
            im.paste(logos[index], offset,mask=logos[index])
        else:
            offset = (80,temp_h_offset+20)
            draw.text(offset,team[0:3],(0, 0, 0),font=font)
        
        l_offset = 100
        #print table header
        draw.text((temp_l_offset + (l_offset/2),h_offset-10),str(index+1),(0, 0, 0),anchor='ms',font=font)
        temp_h_offset = h_offset + h_space_offset*index
        
        #Draw percentage of each position for each team
        for position in results[team]:
            
            percentage = round(results[team][position]/numberOfSimulations*100,1)
            c = int(255*percentage/100)
            color = (c*2+100,c*2+100,c*2+100)
            if(percentage == 0):
                color = background_color
            temp_h_offset = h_offset + h_space_offset*(index)
            temp_l_offset = 75 + l_offset + l_space_offset*(int(position)-1)
            draw.rectangle((temp_l_offset,temp_h_offset -3,temp_l_offset+l_space_offset,temp_h_offset+h_space_offset-3),color,outline='black',width=3)
            
            if(percentage > 0):
                temp_l_offset = l_offset + l_space_offset * int(position)
                draw.text((temp_l_offset + (l_offset/4),temp_h_offset-20 + h_space_offset),str(percentage)+'%',(0,0, 0),anchor='ms',font=smallfont)


    font = ImageFont.truetype("Roboto-Black.ttf", 30)
    today = date.today()
    draw.text((width/2,height),'Model and Visual by @bennivaluR_ (' + str(today) + ')',(0,0,0),anchor='ms',font=font)

    im.save('simResults/' + league + '_resultsOfSeasonSimulation' + '.png', quality=95)

