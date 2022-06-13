import os
import requests
import random
import shutil

class Pokemon:

    def __init__(self):
        self.pkmn_list = self.get_pokemon_list()
        self.pkmn_data = self.get_random_pkmn()
        self.pkmn_name = self.pkmn_data["species"]["name"].title()
        self.pkmn_img_url = self.pkmn_data["sprites"]["other"]["official-artwork"]["front_default"]


    def get_pokemon_list(self):
        
        # Get the list of pokemon from the API
        response = requests.get(url="https://pokeapi.co/api/v2/pokemon/?limit=1126")
        pkmn_list = response.json()["results"]
        return pkmn_list

    def get_random_pkmn(self):
        # Select a random pokemon from the list, and make the api request for that specific pokemon
        random_pkmn = random.choice(self.pkmn_list)
        response = requests.get(url=random_pkmn["url"])
        pkmn_data = response.json()
        # Check if the Pokemon is the "default version" of the Pokemon.
        # AKA, not a weird variant. Return the first default pokemon.
        if pkmn_data["is_default"]:
            print(pkmn_data["species"]["name"])
            print("Is default")
            return pkmn_data
        else:
            print(pkmn_data["species"]["name"])
            print("rerolling...")
            return self.get_random_pkmn()

    def download_pkmn_img(self):
        response = requests.get(url=self.pkmn_img_url, stream=True)
        response.raise_for_status()
        if response.status_code == 200:
            response.raw.decode_content = True

            try:
                with open(f"./output/{self.pkmn_name}.png", "wb") as f:
                    shutil.copyfileobj(response.raw,f)
            except FileNotFoundError:
                os.mkdir(path="./output")
                with open(f"./output/{self.pkmn_name}.png", "wb") as f:
                    shutil.copyfileobj(response.raw,f)

            print("img downlaoded")

        
            
        


def main():
    random_pokemon = Pokemon()
    print(random_pokemon.pkmn_name)
    print(random_pokemon.pkmn_img_url)
    random_pokemon.download_pkmn_img()

if __name__ == "__main__":
    main()