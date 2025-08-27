import pandas as pd


from .models import Asset, Portfolio, PortfolioAssets, AssetPrice


def load_excel(starting_value):
    df = pd.read_excel('data/datos.xlsx', 'weights')
    assets = {}
    portfolios = {}
    weights = {}
    quantities = {}
    weights_time = {}
    total_values = {}

    # store assets
    for asset_name in df['activos']:
        assets[asset_name] = Asset.objects.create(name=asset_name)
        assets[asset_name] = asset_name

    # store portfolios
    for portfolio_name in df.columns[2:]:
        portfolios[portfolio_name] = Portfolio.objects.create(
            name=portfolio_name
        )
        portfolios[portfolio_name] = portfolio_name
        weights[portfolio_name] = {}
        quantities[portfolio_name] = {}
        weights_time[portfolio_name] = {}
        total_values[portfolio_name] = {}

    # store weights
    for idx, row in df.iterrows():
        asset_name = row['activos']
        for portfolio_name in portfolios:
            weights[portfolio_name][asset_name] = row[portfolio_name]

    # ------------------------------------------------------------------------
    # Prices

    df = pd.read_excel('data/datos.xlsx', 'Precios')
    prices = {}
    start_date = df.iloc[0]['Dates']

    # Get starting prices
    for asset_name in assets:
        p0 = df.iloc[0][asset_name]
        prices[asset_name] = p0

    # Calculate starting quantities
    for portfolio_name in weights:
        for asset_name in weights[portfolio_name]:
            w = weights[portfolio_name][asset_name]
            p = prices[asset_name]
            if p == 0:
                raise ValueError(f"Price for {asset_name} shouldn't 0")
            q = (w / p) * starting_value
            quantities[portfolio_name][asset_name] = q
            PortfolioAssets.objects.create(
                portfolio=portfolios[portfolio_name],
                asset=assets[asset_name],
                quantity=q,
                date=start_date
            )

    # Calculate weights and values in time
    for idx, row in df.iterrows():
        date = row['Dates']

        for asset_name in assets:
            p = row[asset_name]
            AssetPrice.objects.create(
                price=p,
                asset=Asset.objects.filter(name=asset_name).first(),
                date=date
            )


def load_excel_without_db(starting_value):
    df = pd.read_excel('data/datos.xlsx', 'weights')
    assets = {}
    portfolios = {}
    weights = {}
    quantities = {}
    weights_time = {}
    total_values = {}

    # store assets
    for asset_name in df['activos']:
        assets[asset_name] = asset_name

    # store portfolios
    for portfolio_name in df.columns[2:]:
        portfolios[portfolio_name] = portfolio_name
        weights[portfolio_name] = {}
        quantities[portfolio_name] = {}
        weights_time[portfolio_name] = {}
        total_values[portfolio_name] = {}

    # store weights
    for idx, row in df.iterrows():
        asset_name = row['activos']
        for portfolio_name in portfolios:
            weights[portfolio_name][asset_name] = row[portfolio_name]

    # ------------------------------------------------------------------------
    # Prices

    df = pd.read_excel('data/datos.xlsx', 'Precios')
    prices = {}
    start_date = df.iloc[0]['Dates']

    # Get starting prices
    for asset_name in assets:
        p0 = df.iloc[0][asset_name]
        prices[asset_name] = p0

    # Calculate starting quantities
    for portfolio_name in weights:
        for asset_name in weights[portfolio_name]:
            w = weights[portfolio_name][asset_name]
            p = prices[asset_name]
            if p == 0:
                raise ValueError(f"Price for {asset_name} shouldn't 0")
            q = (w / p) * starting_value
            quantities[portfolio_name][asset_name] = q

    # Calculate weights and values in time

    for idx, row in df.iterrows():
        date = row['Dates']
        for portfolio_name in portfolios:
            weights_time[portfolio_name][date] = {}
            total_values[portfolio_name][date] = 0.0

        for asset_name in assets:
            p = row[asset_name]
            for portfolio_name in portfolios:
                x = quantities[portfolio_name][asset_name] * p
                weights_time[portfolio_name][date][asset_name] = x
                total_values[portfolio_name][date] += x

        for portfolio_name in portfolios:
            # divide the total value for all the weights
            vt = total_values[portfolio_name][date]
            for asset_name in assets:
                weights_time[portfolio_name][date][asset_name] /= vt

    return weights_time, total_values




if __name__ == '__main__':
    load_excel_without_db(1_000_000_000.0)
