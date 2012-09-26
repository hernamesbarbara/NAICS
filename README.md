...with aspirations of becoming an API for getting industry classification NAICS codes.

Fire up your local mongo server

```bash

mongod
```

Save the 2007 and 2012 NAICS codes into MongoDb

```bash

python flatfiles.py
```

You should now have all NAICS codes on your local mongo instance

```javascript

use industries

db.naics_codes.find().forEach(printjson);

```

You can now fire up the Flask API

```bash

python api.py
```