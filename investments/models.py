from django.db import models


NAME_MAX_LENGTH = 100


class Asset(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)

    def __str__(self):
        return self.name


class Portfolio(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    assets = models.ManyToManyField(Asset, through='PortfolioAssets')

    def __str__(self):
        return self.name


class PortfolioAssets(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    quantity = models.FloatField()
    date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["portfolio", "asset"], name="unique_portfolio_asset"
            )
        ]


class AssetPrice(models.Model):
    price = models.FloatField()
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    date = models.DateField()
