config = {
    'ducks': ['https://images-na.ssl-images-amazon.com/images/I/51Hv7fTTaLL._SX425_.jpg',
              'https://i.pinimg.com/originals/8b/e8/41/8be841dbba8e6c633728ffe1580a930f.jpg'],
    'serious_ducks': ['https://images-na.ssl-images-amazon.com/images/I/31g29UpRHQL._SX450_.jpg',
                      'https://images-na.ssl-images-amazon.com/images/I/31p4yBHv7OL.jpg',
                      'https://images-na.ssl-images-amazon.com/images/I/610WVKNC0OL._SL1024_.jpg'],
    'sad_ducks': ['http://rs162.pbsrc.com/albums/t260/punkyrooster_2007/untitled1.jpg?w=280&h=210&fit=crop',
                  'https://images.cdn4.stockunlimited.net/preview1300/sad-duckling_1487314.jpg',
                  'https://vignette.wikia.nocookie.net/uncyclopedia/images/6/60/Sad_duck.jpg/revision/latest?cb=20090621212341'],
    'default_user_image': 'https://is2-ssl.mzstatic.com/image/thumb/Purple71/v4/c9/f9/d1/c9f9d1e4-b9f1-6bf2-5846-199528ddab8e/source/512x512bb.jpg',
    'DATABASE_URL': 'postgres://helscbcaevmlbw:f939ac997bed11ed53595d047c2bf64be9a280a7c3c8356fed0f87ea4d3aee2e@ec2-79-125-117-53.eu-west-1.compute.amazonaws.com:5432/d52ujvjg2sig3',
}

if __name__ == "__main__":
    import json
    print(json.dumps(config))
