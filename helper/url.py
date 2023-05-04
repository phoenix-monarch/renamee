from config import Config

if os.path.exists('shorteners.txt'):
    with open('shorteners.txt', 'r+') as f:
        lines = f.readlines()
        for line in lines:
            temp = line.strip().split()
            if len(temp) == 2:
                Config.shortener_list.append({'domain': temp[0],'api_key': temp[1]})
