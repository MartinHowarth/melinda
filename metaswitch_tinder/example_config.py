config = {
    'ducks': ['https://images-na.ssl-images-amazon.com/images/I/51Hv7fTTaLL._SX425_.jpg',
              'https://i.pinimg.com/originals/8b/e8/41/8be841dbba8e6c633728ffe1580a930f.jpg'],
    'DATABASE_URL': 'postgres://helscbcaevmlbw:f939ac997bed11ed53595d047c2bf64be9a280a7c3c8356fed0f87ea4d3aee2e@ec2-79-125-117-53.eu-west-1.compute.amazonaws.com:5432/d52ujvjg2sig3',
}

if __name__ == "__main__":
    import json
    print(json.dumps(config))
