import multidict as multidict
from textblob import TextBlob
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import math
from wordcloud import WordCloud

image_mask_path = "usa_map.png"
text_file_path = "diary.txt"


def get_cleaned_noun_string(text):
    text_nouns_converter_blob = TextBlob(text)
    noun_phrases = text_nouns_converter_blob.noun_phrases
    noun_string = ""
    for noun in noun_phrases:
        if "'" in noun:
            temp_arr = noun.split()
            for element in temp_arr:
                if "'" not in element:
                    noun_string += element + " "
        else:
            noun_string += noun + " "
    return noun_string


def get_frequency_dict_from_text(sentence):
    full_terms_dict = multidict.MultiDict()
    tmp_dict = {}

    # making dict for counting frequencies
    for text in sentence.split(" "):
        val = tmp_dict.get(text, 0)
        tmp_dict[text] = val + 1
    for key in tmp_dict:
        full_terms_dict.add(key, math.ceil(10 * math.log(10 + tmp_dict[key])))
    return full_terms_dict


def get_mask_from_image(image_mask_path):
    return np.array(Image.open(image_mask_path))


def get_circle_mask():
    x, y = np.ogrid[:600, :600]

    mask = (x - 300) ** 2 + (y - 300) ** 2 > 260 ** 2
    mask = 255 * mask.astype(int)
    return mask


def make_image(text, bg_color, max_words, mask, image_save):
    wc = WordCloud(background_color=bg_color, max_words=max_words, mask=mask, relative_scaling=0)
    # generate word cloud
    wc.generate_from_frequencies(text)

    # show
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()

    if image_save is not None:
        # Save image
        pass


def main():
    print("Starting main..")

    text_file = open(text_file_path, encoding='utf-8')
    text = text_file.read()
    cleaned_noun_string = get_cleaned_noun_string(text)
    full_terms_dict = get_frequency_dict_from_text(cleaned_noun_string)
    print(full_terms_dict)

    # mask = get_mask_from_image(image_mask_path)
    mask = get_circle_mask()

    make_image(full_terms_dict, "white", 200, mask, None)


if __name__ == '__main__':
    main()
