from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for, make_response
)
import pandas

app = Flask(__name__)


def get_rushing_dataframe():
    ''' Parses the provided JSON file and cashes the dataframe for repeated access '''
    try:
        rushing_data = pandas.read_pickle('cached_rushing_dataframe.pk1')
    except FileNotFoundError:
        rushing_data = pandas.read_json('rushing.json', dtype={'Yds': str, 'Lng': str})
        rushing_data['Yds'] = rushing_data['Yds'].str.replace(',', '').astype(int)

        # Remove and store all 'T' values for better sorting and styling
        rushing_data['Lng Touchdown'] = False
        rushing_data['Lng Touchdown'] = rushing_data['Lng Touchdown'].mask(rushing_data.Lng.str.contains('T'), True)
        rushing_data['Lng'] = rushing_data['Lng'].str.replace('T', '').astype(int)

        rushing_data.to_pickle('cached_rushing_dataframe.pk1')

    return rushing_data


def highlight_touchdown_rush(x):
    ''' Apply a material green background to longest rush touchdowns to make them stand out '''
    mask = x['Lng Touchdown'] == 1
    style_dataframe = pandas.DataFrame('', index=x.index, columns=x.columns)
    style_dataframe.loc[mask, 'Lng'] = 'background-color: #5efc82;'
    return style_dataframe


def filter_rushing_data(player_name=None, category_sort=None):
    rushing_data = get_rushing_dataframe()

    if player_name:
        rushing_data = rushing_data[rushing_data['Player'].str.contains(player_name)]

    if category_sort:
        category_sort = category_sort.split(' - ')
        rushing_data = rushing_data.sort_values(by=[category_sort[0]], ascending=[category_sort[1] == 'ASC'])

    return rushing_data


def get_rushing_html(player_name=None, category_sort=None):
    ''' Style the dataframe to render in the expected format '''
    rushing_data = filter_rushing_data(player_name, category_sort)

    rushing_data = rushing_data.style.format(
        precision=1, thousands=''
    ).hide_index().hide_columns(['Lng Touchdown'])
    rushing_data.apply(highlight_touchdown_rush, axis=None)
    return rushing_data.render()


@app.route('/')
def rushing_table():
    rushing_data = get_rushing_html()
    return render_template('index.html', data=rushing_data)


@app.route('/filter_data', methods=['GET'])
def filter_data():
    player_name = request.args.get('player_name')
    category_sort = request.args.get('category_sort')

    return get_rushing_html(player_name, category_sort)


@app.route('/download_data', methods=['GET'])
def download_data():
    player_name = request.args.get('player_name')
    category_sort = request.args.get('category_sort')

    rushing_data = filter_rushing_data(player_name, category_sort)

    response = make_response(rushing_data.to_csv(index=False))
    response.headers["Content-Disposition"] = "attachment;"
    response.headers["Content-Type"] = "text/csv"
    return response


if __name__ == "__main__":
    app.run(debug=True)
