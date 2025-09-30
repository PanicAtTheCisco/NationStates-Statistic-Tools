## NationStates Statistic Tools
* A collection of tools I made for [NationStates](https://www.nationstates.net/) to keep track of and monitor the statistics of both my nation and that of the nations in my region

### nation-regional-rankings.py
* Returns the current statistic rankings of a single nation in their region

#### Usage
* Make sure you have python installed
* You will need the `requests` and `matplotlib` libraries
* Clone the repository
* In the directory for the tools, create a config.json file with the following format for the user-agent
* A user-agent with an email or nation name is required to access the API in case issues arise
```json
{
    "user-agent": "<your email/nation name>"
}
```
* Run program and enter nation name

## TODO
* Create tool for getting historical trends for a single nation
* Create tools for pulling stats and historical trends for all nations in a region (with rate limiting to avoid API issues)
* Continue adding graphing features to tools for visual comparisons
* Update usage documentation to be more comprehensive and organized