# Docker API - Outlier Detection

This project demonstrates the creation and implementation of a simple REST API in Python using Docker and Flask to deploy a model for detecting outlying data in a time series.

The method for detecting outlying data relies upon some assumptions for financial data. The model was written and tested and three different series detailing roughly five years worth of data for three different metrics relating to BTC. As such the assumptions of the model are three fold:
the first is for the STL where the period is set to 365, second is a rolling mean and stdev over a 20wk period, and third it is assumed that to get the truly anomalous data the model looks for those points which are more than three stdevs away from the rolling mean.


## Usage

### JSON Format
The method assumes that the format of the json data being sent to it is as follows:

```bash
{
        "t": "2016-01-01",
        "v": "316489"
    },
    {
        "t": "2016-01-02",
        "v": "419389"
    },
    {
        "t": "2016-01-03",
        "v": "394047"
    },
    {
        "t": "2016-01-04",
        "v": "418253"
    },...
```
Where the date information is labeled 't' and the value information is labeled 'v'.

### Shell
```bash
curl -X POST\
  -H 'Content-Type: application/json'\
  -d @<filename>.json\
  http://0.0.0.0:5000/events 
```

