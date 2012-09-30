####...with aspirations of becoming an API for searching NAICS industry classification codes.

#####Currently it only supports querying for a specific code a specific year. All 2007 and 2012 NAICS codes are available.

GET /naics to fetch all documents:

http://stark-fjord-5272.herokuapp.com/naics

Or query for a specific year and code:

http://stark-fjord-5272.herokuapp.com/naics?code=72&year=2007