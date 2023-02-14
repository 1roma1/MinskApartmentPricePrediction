import os
import json
import pandas as pd 
from tqdm import tqdm


apartment_dict = {
    "code": [],
    "created_at": [], 
    "updated_at": [], 
    "price": [],
    "price_per_m2": [],
    "slides": [],
    "seller": [],
    "town_district_name": [],
    "town_sub_district_name": [], 
    "address": [], 
    "building_year": [], 
    "area_total": [], 
    "area_living": [], 
    "area_kitchen": [], 
    "area_snb": [], 
    "area_balcony": [], 
    "rooms": [], 
    "separate_rooms": [], 
    "storeys": [], 
    "storey": [], 
    "storey_type": [], 
    "repairs_state": [], 
    "furniture": [], 
    "toilet": [], 
    "balcony_type": [], 
    "house_type": [], 
    "levels": [], 
    "title": [], 
    "description": [],
    "comments": [], 
    "location": [], 
    "floor_type": [],
    "parking_place": [], 
    "nearest_metro_station": [], 
    "nearest_metro_station_distance": [], 
    "layout": [], 
    "neighbors": [], 
    "number_of_beds": [], 
    "term_of_sale": [], 
    "owner": [], 
    "ceiling_height": [], 
    "is_new_build": [],
}


data_path = "data/2022_12_23/"
json_files = os.listdir(data_path)

for json_file_name in tqdm(json_files):
    with open(os.path.join(data_path, json_file_name), "r", encoding="utf-8") as f:
        json_file = json.load(f)

    for apartment_desc in json_file:
        apartment_desc = apartment_desc["props"]["pageProps"]["initialState"]["objectView"]["object"]
        if apartment_desc is not None:
            apartment_dict["code"].append(apartment_desc["code"])
            apartment_dict["created_at"] .append(apartment_desc["createdAt"])
            apartment_dict["updated_at"].append(apartment_desc["updatedAt"])
            price = apartment_desc["priceRates"]["840"] \
                if apartment_desc["priceRates"] is not None else None
            apartment_dict["price"].append(price)
            price_per_m2 = apartment_desc["priceRatesPerM2"]["840"] \
                if apartment_desc["priceRatesPerM2"] is not None else None   
            apartment_dict["price_per_m2"].append(price_per_m2)   
            apartment_dict["slides"].append(apartment_desc["slides"])
            apartment_dict["seller"].append(apartment_desc["seller"])
            apartment_dict["town_district_name"].append(apartment_desc["townDistrictName"])
            apartment_dict["town_sub_district_name"].append(apartment_desc["townSubDistrictName"])
            apartment_dict["address"].append(apartment_desc["address"])
            apartment_dict["building_year"].append(apartment_desc["buildingYear"])
            apartment_dict["area_total"].append(apartment_desc["areaTotal"])
            apartment_dict["area_living"].append(apartment_desc["areaLiving"])
            apartment_dict["area_kitchen"].append(apartment_desc["areaKitchen"])
            apartment_dict["area_snb"].append(apartment_desc["areaSnb"])
            apartment_dict["area_balcony"].append(apartment_desc["areaBalcony"])
            apartment_dict["rooms"].append(apartment_desc["rooms"])
            apartment_dict["separate_rooms"].append(apartment_desc["separateRooms"])
            apartment_dict["storeys"].append(apartment_desc["storeys"])
            apartment_dict["storey"].append(apartment_desc["storey"])
            apartment_dict["storey_type"].append(apartment_desc["storeyType"])
            apartment_dict["repairs_state"].append(apartment_desc["repairState"])
            apartment_dict["furniture"].append(apartment_desc["furniture"])
            apartment_dict["toilet"].append(apartment_desc["toilet"])
            apartment_dict["balcony_type"].append(apartment_desc["balconyType"])
            apartment_dict["house_type"].append(apartment_desc["houseType"])
            apartment_dict["levels"].append(apartment_desc["levels"])
            apartment_dict["title"].append(apartment_desc["title"])
            apartment_dict["description"].append(apartment_desc["description"])
            apartment_dict["comments"].append(apartment_desc["comments"])
            apartment_dict["location"].append(apartment_desc["location"])
            apartment_dict["floor_type"].append(apartment_desc["floorType"])
            apartment_dict["parking_place"].append(apartment_desc["parkingPlace"])
            nearest_metro_station = apartment_desc["nearestMetroStations"][0]["stationName"] \
                if len(apartment_desc["nearestMetroStations"]) > 0 else None
            apartment_dict["nearest_metro_station"].append(nearest_metro_station)
            nearest_metro_station_distance = apartment_desc["nearestMetroStations"][0]["distance"] \
                if len(apartment_desc["nearestMetroStations"]) > 0 else None              
            apartment_dict["nearest_metro_station_distance"].append(nearest_metro_station_distance)
            apartment_dict["layout"].append(apartment_desc["layout"])
            apartment_dict["neighbors"].append(apartment_desc["neighbors"])
            apartment_dict["number_of_beds"].append(apartment_desc["numberOfBeds"])
            apartment_dict["term_of_sale"].append(apartment_desc["termsOfSale"])
            apartment_dict["owner"].append(apartment_desc["owner"])
            apartment_dict["ceiling_height"].append(apartment_desc["ceilingHeight"])
            apartment_dict["is_new_build"].append(apartment_desc["isNewBuild"])

df = pd.DataFrame(apartment_dict)
df.to_csv("data/2022_12_23/apartment_data.csv", index=False)