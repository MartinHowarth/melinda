config = {
    'ducks': ['https://images-na.ssl-images-amazon.com/images/I/51Hv7fTTaLL._SX425_.jpg',
              'https://i.pinimg.com/originals/8b/e8/41/8be841dbba8e6c633728ffe1580a930f.jpg'],
    'serious_ducks': ['https://images-na.ssl-images-amazon.com/images/I/31g29UpRHQL._SX450_.jpg',
                      'https://images-na.ssl-images-amazon.com/images/I/31p4yBHv7OL.jpg',
                      'https://images-na.ssl-images-amazon.com/images/I/610WVKNC0OL._SL1024_.jpg'],
    'DATABASE_URL': 'postgres://helscbcaevmlbw:f939ac997bed11ed53595d047c2bf64be9a280a7c3c8356fed0f87ea4d3aee2e@ec2-79-125-117-53.eu-west-1.compute.amazonaws.com:5432/d52ujvjg2sig3',
}

if __name__ == "__main__":
    import json
    print(json.dumps(config))
