from datetime import date, timedelta

from django.http import JsonResponse


from  .models import AssetPrice, Portfolio, PortfolioAssets


def index(request):
    # start_date = datetime.date(2022, 2, 15)
    # end_date = datetime.date(2023, 2, 16)

    # Get start date and end date from GET request
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    start_date = date.fromisoformat(start_date_str)
    end_date = date.fromisoformat(end_date_str)

    # Collect all data in a dictionary
    data = {}
    for portfolio in Portfolio.objects.all():
        # Each portfolio has a dictionary
        portfolio_data = {}
        data[portfolio.name] = portfolio_data

        time_delta = timedelta(days=1)
        curr_date = start_date

        while curr_date <= end_date:
            # Iterate on each date from start date to end date
            date_key = curr_date.isoformat()
            weights = {}
            value = 0.0

            for asset_price in AssetPrice.objects.filter(date=curr_date):
                asset = asset_price.asset
                p = asset_price.price
                q = PortfolioAssets.objects.filter(
                    asset=asset, portfolio=portfolio
                ).first().quantity
                x = p * q
                weights[asset.name] = x
                value += x

            # Divide all weights by the total value
            for asset_name in weights:
                weights[asset_name] /= value

            data[portfolio.name][date_key] = {
                'weights': weights, 'value': value
            }
            curr_date += time_delta

    return JsonResponse(data)
