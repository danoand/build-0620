## Operating Commands

Listed below are the common commands to start the modeling recommendations microservice (Flask app) which currently runs
on a Digital Ocean server.

**Start Flask App in the Background and Log to File**

`sudo nohup python3 app.py > log.txt 2>&1 &`

**Tail the Log File**

`tail -f log.txt`

**Pull the Latest Code from GitHub (remote git repo)**

`git pull https://github.com/danoand/build-0620.git`

**List the Process Id of the App Running on Port 5000**

`lsof -i :5000`

**Reload with an Updated Caddyfile to Allow CORS Requests**

```
cd /app/caddy
caddy reload --config Caddyfile
```

----

## Microservice Documentation

Here are the details on a Flask app running on a Digital Ocean server that serves recommendations based on a Nearest Neighbors model

----
### Code

You can find the code here:

* **Latest Colab Notebook**: [link|(https://colab.research.google.com/drive/11eBBDI2Od1n9Lhj3HseKsnulpbdsxk9u?usp=sharing)]
* **Flask App**: https://github.com/danoand/build-0620

----
### Server

* URL: `https://medcab2.dananderson.dev` (only use `https`)

----
### Routes & Requests

#### SIMPLE STATUS ROUTE

* **Route**: `/status`
* **Method**: `GET`

```
{
  "msg": "app.py is up and running",
  "note": "the number of strains in the dataset is: 2350"
}
```

#### PRIMARY ROUTE:

* **Route**: `/get_recommendation` 
* **Method**: `POST`

The endpoint parses a simple json document such as:

```
{
  "text": "Big White is an indica-dominant hybrid that combines The White with Big Bud genetics. Bred by La Plata Labs this strain began as an F1 hybrid created by Eclectic Genetics.¬¨‚Ä†La Plata Labs then refined and stabilized the genetics through generations of breeding and phenotype selection. This strain is known to produce large yields of sweet sugary buds that express themselves in a variety of colors and carry a unique maple syrup flavor. There is another known hybrid by the name of Big White. It is bred by Breeder‚Äö√Ñ√¥s Choice and its lineage is a combination of Power Plant and Chronic genetics."
}
```

Response

* The model returns `8` recommendations that seem to be similar to the language in the underlying dataset based on the text submitted in the request
* Note, at this time the recommendations are of any type (currently no filtering on the strain type)
* The recommendations are sorted in closest "similarity" first 

Here's an example:

```
{
  "length": 8,
  "msg": "your recommendations",
  "recommendations": [
    {
      "description": "Big White is an indica-dominant hybrid that combines The White with Big Bud genetics. Bred by La Plata Labs  this strain began as an F1 hybrid created by Eclectic Genetics.¬†La Plata Labs then refined and stabilized the genetics through generations of breeding and phenotype selection. This strain is known to produce large yields of sweet  sugary buds that express themselves in a variety of colors and carry a unique maple syrup flavor.There is another known hybrid by the name of Big White. It is bred by Breeder‚Äôs Choice and its lineage is a combination of Power Plant and Chronic genetics.",
      "df_index": 209,
      "effects": "Relaxed, Uplifted, Happy, Sleepy, Euphoric",
      "flavor": "Flowery, Diesel, Sweet",
      "rating": 4.2,
      "score": 0.153,
      "strain": "Big-White",
      "symptoms_diseases": "ms, spasticity, ",
      "type": "indica"
    },
    {
      "description": "New from La Plata Labs  Colorado Clementines is a 70% indica-dominant ¬†hybrid with odor and yields that are off the charts. By combining their own Big White with TGA Genetics‚Äô Agent Orange  La Plata has created an orange-citrus scented monster with yields as high as 1 gram per watt and an odor that ranks at 11 on a 1-to-10 scale of intensity. With a THC content as high as 24%  beginners should take great care not to over imbibe on this potent strain.¬†",
      "df_index": 569,
      "effects": "Relaxed, Happy, Sleepy, Euphoric, Hungry",
      "flavor": "Citrus, Earthy, Orange",
      "rating": 4.5,
      "score": 1.231,
      "strain": "Colorado-Clementines",
      "symptoms_diseases": "spasticity, ",
      "type": "indica"
    },
    {
      "description": "Spawn from Afghani¬†and Big Bud  Afghan Big Bud (or Big Bud Afghani) is characterized as a large plant with broad leaves and thick stems. It has a dense appearance  similar to Big Bud  and maintains the taste of Afghani  resulting in¬†the best of both worlds. The effects come¬†relatively quick but¬†usually dissipate¬†under two hours.¬†",
      "df_index": 34,
      "effects": "Euphoric, Happy, Relaxed, Sleepy, Talkative",
      "flavor": "Pungent, Lemon, Peach",
      "rating": 4.0,
      "score": 1.267,
      "strain": "Afghan-Big-Bud",
      "symptoms_diseases": "ms, spasticity, ",
      "type": "indica"
    },
    {
      "description": "A cousin to the indica-dominant Big Bud cannabis strain from Amsterdam  BC Big Bud is a mostly sativa hybrid with potent cerebral effects. This fruity  citrus-smelling strain hailing from British Columbia delivers a balanced combination of indica and sativa sensations as well as relief to pain and nausea. As its name suggests  BC Big Bud plants produce colossal harvests after its 8 to 9 week flowering period that have both growers and consumers swooning.",
      "df_index": 154,
      "effects": "Relaxed, Euphoric, Happy, Creative, Sleepy",
      "flavor": "Earthy, Pungent, Tropical",
      "rating": 4.5,
      "score": 1.268,
      "strain": "Bc-Big-Bud",
      "symptoms_diseases": "nausea, ms, pain, pain, spasticity, ",
      "type": "hybrid"
    },
    {
      "description": "Mangolicious is an indica-dominant cross of Big Bud and White Widow. This cut expresses a tropical aroma and robust bud structure. It has a relatively speedy flowering time and a generous yield thanks to its Big Bud genetics. Mangolicious‚Äôs full-body effects and pleasant mango smell speak to potentially high levels of myrcene  a terpene known for its weighted ‚Äúcouchlocking‚Äù effect.",
      "df_index": 1344,
      "effects": "Uplifted, Focused, Relaxed, Giggly, Happy",
      "flavor": "Sweet, Tropical, Pineapple",
      "rating": 5.0,
      "score": 1.281,
      "strain": "Mangolicious",
      "symptoms_diseases": "spasticity, ",
      "type": "indica"
    },
    {
      "description": "Quin-N-Tonic is a high-CBD strain bred by La Plata Labs  who combines genetics from Harlequin and Cannatonic. Led by indica genetics  Quin-N-Tonic produces high yields of frosted purple-tipped buds that carry a sweet  dessert-like blueberry aroma. Its CBD-rich profile makes this strain an excellent choice for patients dealing with pain or inflammation  or for those made uncomfortable by THC‚Äôs psychoactive effects.",
      "df_index": 1739,
      "effects": "Relaxed, Happy, Focused, Hungry, Sleepy",
      "flavor": "Sweet, Blueberry, Pungent",
      "rating": 4.6,
      "score": 1.288,
      "strain": "Quin-N-Tonic",
      "symptoms_diseases": "inflammation, pain, pain, spasticity, ",
      "type": "indica"
    },
    {
      "description": "Big Mac by Federation Seeds is an indica-dominant strain with unique sativa fan leaves and an accelerated grow cycle. This generous cut of Mikado and BC Big Bud develops quickly indoors  growing upwards of six feet tall over its speedy seven week maturation. The large plant produces a healthy yield of fruity mid-sized buds that reek of berry and citrus peel. Big Mac‚Äôs effects elevate the mind and relax the body  offering a creative bent to a satisfying sedation. Enjoy Big Mac to stimulate the mind and the appetite while infusing the limbs with a relaxing weighted warmth. ¬†¬†",
      "df_index": 204,
      "effects": "Relaxed, Aroused, Sleepy, Talkative, Tingly",
      "flavor": "Sweet, Berry, Blueberry",
      "rating": 5.0,
      "score": 1.292,
      "strain": "Big-Mac",
      "symptoms_diseases": "appetite, appetite, spasticity, ",
      "type": "indica"
    },
    {
      "description": "Big Wreck is the ndica-dominant cross of Big Bud and Trainwreck. This chunky combination offers functional relaxation with an uplifted mental buzz that some might describe as creative. This strain becomes very sedative with continuous use and may also stimulate your appetite.¬†",
      "df_index": 210,
      "effects": "Relaxed, Tingly, Euphoric, Happy, Uplifted",
      "flavor": "Earthy, Pungent, Nutty",
      "rating": 4.1,
      "score": 1.299,
      "strain": "Big-Wreck",
      "symptoms_diseases": "appetite, appetite, spasticity, ",
      "type": "indica"
    }
  ],
  "text": "Big White is an indica-dominant hybrid that combines The White with Big Bud genetics. Bred by La Plata Labs  this strain began as an F1 hybrid created by Eclectic Genetics.¬¨‚Ä†La Plata Labs then refined and stabilized the genetics through generations of breeding and phenotype selection. This strain is known to produce large yields of sweet  sugary buds that express themselves in a variety of colors and carry a unique maple syrup flavor.There is another known hybrid by the name of Big White. It is bred by Breeder‚Äö√Ñ√¥s Choice and its lineage is a combination of Power Plant and Chronic genetics."
}
```
