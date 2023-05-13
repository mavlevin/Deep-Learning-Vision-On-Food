import json
import csv
import numpy as np

def get_buisness_id_to_stars(buisness_json_file_path):
    buisness_id_to_stars = {}
    with open(buisness_json_file_path, "r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            biz_raw_data = json.loads(line)
            buisness_id_to_stars[biz_raw_data["business_id"]] = biz_raw_data["stars"]
    return buisness_id_to_stars

def get_pic_label_stars_list(photos_json_file_path, buisness_id_to_stars, wanted_label=None):
    pic_label_stars_list = []
    with open(photos_json_file_path, "r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            photo_raw_data = json.loads(line)
            if wanted_label and photo_raw_data["label"] != wanted_label:
                continue
            photo_data = (photo_raw_data["photo_id"], photo_raw_data["label"], buisness_id_to_stars[photo_raw_data["business_id"]])
            pic_label_stars_list.append(photo_data)

    return pic_label_stars_list

def dump_photo_data(output_path, pic_label_stars_list):
    with open(output_path, mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(["img_name", "img_label", "rating"])
        writer.writerows(pic_label_stars_list)
    print(f"wrote {len(pic_label_stars_list)} entries to '{output_path}'")


def main():
    print("starting")
    buisness_id_to_stars = get_buisness_id_to_stars("yelp_dataset/yelp_academic_dataset_business.json")
    pic_label_stars_list = get_pic_label_stars_list("yelp_photos/photos.json", buisness_id_to_stars, wanted_label="food")

    dump_photo_data("all_photo_data.csv", pic_label_stars_list)

    # shuffle and split into training, validation, and test set
    np.random.seed(0x1234) # to ensure same results each time
    np.random.shuffle(pic_label_stars_list)
    dl = len(pic_label_stars_list)

    divider1 = int(len(pic_label_stars_list)*0.60)
    divider2 = divider1 + int(len(pic_label_stars_list)*0.20)
    divider3 = divider2 + int(len(pic_label_stars_list)*0.20)
    training, validation, testing = \
        pic_label_stars_list[:divider1], pic_label_stars_list[divider1:divider2], pic_label_stars_list[divider2:divider3]
    
    dump_photo_data("training_photo_data.csv", training)
    dump_photo_data("validation_photo_data.csv", validation)
    dump_photo_data("testing_photo_data.csv", testing)

if __name__ == "__main__":
    main()
