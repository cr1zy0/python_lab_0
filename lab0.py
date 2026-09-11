
f = open('python_lab\\siege_log.txt')
logs = []
weapon_states = {
    'active': 1.5,
    'broken': 0.5,
    'overheated': 0.7,
    'destroyed': 0.1,
    'repairing':0.3
    
}
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def find_guild_and_name(s:str):
    name = ''
    cur_guild = ''
    c = 0
    temp = 0
    
    for i in range(len(s)):
        
        if s[i] == '[':
            c+=1
        if s[i] == ']':
            temp = i
            c-=1
        if c > 0:
            cur_guild += s[i]
        if cur_guild and c == 0:
            name = s[i+1:]
            break
    else: 
        name = s
        if c > 0 and temp > 0:
            cur_guild = s[s.find('['):temp]
            name = s[temp+1:]
    if len(cur_guild)<=1:
        cur_guild = ' EMPTY GUILD'
    return [cur_guild[1:], name]

def split_log(s:str):
    buffs = []
    try:
        while is_number(s.rsplit('|',1)[1].strip()) or not s.rsplit('|',1)[1].strip() or s.rsplit('|',1)[1].strip() == 'N/A':
            
            parts = s.rsplit('|',1)
            right = parts[1].strip()
            
            if not right or right == 'N/A':
                buffs.append(0)
            else:
                buffs.append(right)
            s = parts[0]
    except IndexError:
        print('There were no weapon state so this log assumes as damaged')
        
        return ['[BrokenGuild]BrockenMan','0','Destroyed',0]
    
    return [*list(map(lambda x: x.strip(), s.rsplit('|',2))),sum(map(lambda x: abs(float(x)),buffs))]

def is_damage_normal(dmg:str):
    dmg = dmg.replace(' ','').replace(',','.')
    if dmg == 'inf':
        return 0
    try: 
        float(dmg)
        return float(dmg)
    except ValueError:
        print('damage was broken')
        return 0
    
def calculate_damage(damage:str,state:str,buffs:float) -> list:
    dmg = is_damage_normal(damage)
    state_mult = weapon_states[state.lower()]
    return round(dmg*state_mult*(1+0.15*buffs),2)


for i in f:
    if not i.isspace():
        splitted_log = split_log(i)
        log = [*find_guild_and_name(splitted_log[0]),*splitted_log[1:]]
        if len(log)>4:
            logs.append(log)
for i in logs:
    guild = i[0]
    name = i[1]
    damage = calculate_damage(*i[2:])
    print(f'Игрок {name} из гильдии {guild} нанес {damage} по воротам')

    
