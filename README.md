####...with aspirations of becoming an API for searching NAICS industry classification codes.

#####Currently it only supports querying for a specific code or year. All 2007 and 2012 NAICS codes are available.

GET /naics to fetch all documents:

http://industries.herokuapp.com/naics

Or query for a specific year and code:

http://industries.herokuapp.com/naics?year=2007&code=72