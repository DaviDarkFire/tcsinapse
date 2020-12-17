import json
import datetime
import requests

class Item:
    def __init__(self, json_entry):
        self.name = json_entry['item']
        self.amount = json_entry['quantidade']
        self.total = json_entry['total']


class Itens:
    def __init__(self, json_filename, tresh_minimum_date, tresh_maximum_date):
        self.json_dict = self.load_json(json_filename)
        self.item_list = []
        self.tresh_minimum_date = tresh_minimum_date
        self.tresh_maximum_date = tresh_maximum_date

        for json_entry in self.json_dict:

            #print(json_entry['dia'], self.tresh_minimum_date)
            if(self.selled_in_a_valid_date(json_entry['dia'])): #optei por adicionar os itens na lista criada ja filtrando os que não estavam na data especificada
                item = Item(json_entry)
                item_position = self.is_this_item_in_the_list(item)
                if(item_position == -1):
                    self.item_list.append(item)
                else:
                    self.item_list[item_position].amount += item.amount
                    self.item_list[item_position].total += item.total

    def is_this_item_in_the_list(self,item): #se o tem estiver na lista retorna a posição dele, se não estiver retorna -1
        i = 0
        for it in self.item_list:
            if it.name == item.name:
                return i
            i += 1
        return -1

    def load_json(self, filename):
        f = open(filename)
        json_dict = json.load(f)
        return json_dict

    def selled_in_a_valid_date(self, entry_date):
        entry_date = self.parse_date(entry_date)
        #print(entry_date,self.tresh_minimum_date)
        if (entry_date >= self.tresh_minimum_date and entry_date <= self.tresh_maximum_date):
            return True
        else:
            return False

    def parse_date(self, date):
        date = date.split('/')
        return datetime.date(int(date[2]), int(date[1]), int(date[0]))

    def most_selled(self):
        most_selled = self.item_list[0]
        for item in self.item_list:
            if (item.amount > most_selled.amount):
                most_selled = item
            if (item.amount == most_selled.amount):
                if(item.name < most_selled.name):
                    most_selled = item
        return most_selled





def main():
    itens = Itens("recrutamento.json",datetime.date(2018, 12, 1),datetime.date(2018, 12, 31))
    print(itens.item_list)
    for item in itens.item_list:
        print(item.name,item.amount,item.total)
    print("***************************")
    most_selled = itens.most_selled()

    text = f"{most_selled.name}#{most_selled.total}"
    url = 'https://eventsync.portaltecsinapse.com.br/public/recrutamento/finalizar?email=daviferreirasantog@gmail.com'
    x = requests.post(url, data = text)
    print(x.text)

if __name__ == "__main__":
    main()

