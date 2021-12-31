from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for
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
        rushing_data['Lng'] = rushing_data['Lng'].apply(highlight_touchdown_rush)

        # rushing_data = rushing_data.style.applymap(highlight_touchdown_rush, subset=pandas.IndexSlice[:, ['Lng']])

        rushing_data.to_pickle('cached_rushing_dataframe.pk1')

    return rushing_data


def highlight_touchdown_rush(rush):
    if 'T' in rush:
        return f'<div class="touchdown-highlight" title="Touchdown Scored">{rush[:-1]}*</div>'
    return rush


def get_rushing_html(player_name=None, category_sort=None):
    rushing_data = get_rushing_dataframe()

    if player_name:
        rushing_data = rushing_data[rushing_data['Player'].str.contains(player_name)]

    if category_sort:
        rushing_data = rushing_data.sort_values(by=[category_sort])

    return rushing_data.to_html(escape=False)


@app.route('/')
def hello_geek():
    rushing_data = get_rushing_html()
    return render_template('index.html', data=rushing_data)


@app.route('/filter_data', methods=['POST'])
def filter_data():
    player_name = request.form.get('player_name')
    category_sort = request.form.get('category_sort')

    return get_rushing_html(player_name, category_sort)


if __name__ == "__main__":
    app.run(debug=True)
