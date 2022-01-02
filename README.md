# theScore
My implementation of the "the Rush" Interview Challenge

## Design decisions
I chose Python and Flask because that's what I'm comfortable with at this point in time.

The only library I'm using is pandas. I specifically chose to use it for two reasons:
  1. It's designed to be efficient at handling data, so scalability is built in.
  2. It's a newly acquired skill for me and I want to continue using and learning it whenever possible.

The parsed pandas dataframe is cached so the original JSON doesn't have to be read and parsed on every subsequent user action. This was only necessary since I'm not processing the data on the front-end in order to focus on the back-end.

Longest rush touchdown cells are hightlighted in green in order to differentiate them and not display the 'T'. A new column that is not displayed was added to track this, but is available upon downloading to CSV. The table colours were also taken directly from the theScore logo present in emails with my contact.

I opted to keep the shortform column names as I would expect anyone viewing this data to be familiar with what they mean, and official NFL statistic tables have similar column names.

Filtering/sorting/downloading is handled in pure javascript in order to behave like a single page application. Player names are filtered on whether the input provided is a substring, rather than an exact search.

## Deficiencies
There are a list of things I didn't implement since I spent more time than I wanted to on this challenge getting the functionality exactly how I wanted it.
  * Unit testing.
  * Error checking when parsing the provided data.
  * The original file name is hard-coded into the data load. Typically speaking, I would have liked to load it into a sql-lite instance and pull the data from there instead.
  * The front-end is extremely bare bones. Unfortunately, I'm not well versed in front-end frameworks or design.
  * Sorting options present in the select element are separated into ASC/DESC, which I'm not really a fan of. Historically I've done front-end sorting with the `datatables` plug-in, or something similar, but since I'm rebuilding the table on a Filter button click with data from Flask it worked better this way.
  * Downloading returns new data based on the current player name filter and selected sorting category, which doesn't necessarily match the data currently shown. Really I should have fixed this as it wouldn't be too difficult to adjust the javascript.
  * There is no pagination option.

## Installation and running this solution
This solution has been dockerized, at least as much as I know how. To run have port `5000` available and execute the following from the base directory:
```
docker build --tag python-docker .
docker run -d -p 5000:5000 python-docker
```
The app can then be accessed at `http://127.0.0.1:5000/`.
